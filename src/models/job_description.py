"""
Job Description Data Model
=========================

Data class representing a job description with all extracted requirements.
Provides structured access to job requirements and matching criteria.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from datetime import datetime
from pathlib import Path
import re


@dataclass
class CompanyInfo:
    """Company information from job description"""
    name: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None


@dataclass
class JobRequirements:
    """Job requirements and qualifications"""
    education: List[str] = field(default_factory=list)
    experience_years: Optional[str] = None
    required_skills: List[str] = field(default_factory=list)
    preferred_skills: List[str] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    languages: List[str] = field(default_factory=list)


@dataclass
class JobBenefits:
    """Job benefits and compensation"""
    salary_range: Optional[str] = None
    benefits: List[str] = field(default_factory=list)
    work_arrangement: Optional[str] = None  # Remote, Hybrid, On-site
    schedule: Optional[str] = None


@dataclass
class SkillWeight:
    """Skill importance weighting"""
    critical: List[str] = field(default_factory=list)      # Must-have skills
    important: List[str] = field(default_factory=list)     # High priority
    preferred: List[str] = field(default_factory=list)     # Nice to have
    bonus: List[str] = field(default_factory=list)         # Additional advantage


@dataclass
class JobDescription:
    """Complete job description data model"""
    
    # File information
    file_path: str
    file_name: str = field(init=False)
    file_format: str = field(init=False)
    file_size: int = 0
    processing_date: datetime = field(default_factory=datetime.now)
    
    # Job information
    title: Optional[str] = None
    department: Optional[str] = None
    job_type: Optional[str] = None  # Full-time, Part-time, Contract, Internship
    level: Optional[str] = None     # Entry, Mid, Senior, Lead, Executive
    
    # Company information
    company: CompanyInfo = field(default_factory=CompanyInfo)
    
    # Job details
    summary: Optional[str] = None
    description: Optional[str] = None
    responsibilities: List[str] = field(default_factory=list)
    
    # Requirements
    requirements: JobRequirements = field(default_factory=JobRequirements)
    skill_weights: SkillWeight = field(default_factory=SkillWeight)
    
    # Benefits and compensation
    benefits: JobBenefits = field(default_factory=JobBenefits)
    
    # All skills combined
    all_skills: Set[str] = field(default_factory=set)
    
    # Raw content
    raw_text: str = ""
    cleaned_text: str = ""
    
    # Analysis results
    text_metrics: Dict[str, any] = field(default_factory=dict)
    keywords: List[tuple] = field(default_factory=list)  # (keyword, frequency)
    technical_terms: List[str] = field(default_factory=list)
    
    # Processing metadata
    processing_success: bool = True
    processing_errors: List[str] = field(default_factory=list)
    extraction_confidence: float = 0.0
    
    def __post_init__(self):
        """Initialize computed fields after creation"""
        path = Path(self.file_path)
        self.file_name = path.name
        self.file_format = path.suffix.lower()
        
        # Update all_skills set
        self._update_all_skills()
    
    def _update_all_skills(self):
        """Update the combined skills set"""
        self.all_skills.clear()
        
        # Add skills from requirements
        self.all_skills.update(self.requirements.required_skills)
        self.all_skills.update(self.requirements.preferred_skills)
        
        # Add skills from weights
        self.all_skills.update(self.skill_weights.critical)
        self.all_skills.update(self.skill_weights.important)
        self.all_skills.update(self.skill_weights.preferred)
        self.all_skills.update(self.skill_weights.bonus)
    
    def add_skill(self, skill: str, category: str = 'required', weight: str = 'important'):
        """Add a skill to the appropriate category and weight"""
        skill = skill.strip()
        if not skill:
            return
        
        # Add to requirements category
        if category == 'required':
            if skill not in self.requirements.required_skills:
                self.requirements.required_skills.append(skill)
        elif category == 'preferred':
            if skill not in self.requirements.preferred_skills:
                self.requirements.preferred_skills.append(skill)
        
        # Add to skill weights
        weight_map = {
            'critical': self.skill_weights.critical,
            'important': self.skill_weights.important,
            'preferred': self.skill_weights.preferred,
            'bonus': self.skill_weights.bonus
        }
        
        if weight in weight_map:
            if skill not in weight_map[weight]:
                weight_map[weight].append(skill)
        
        self._update_all_skills()
    
    def get_skill_weight(self, skill: str) -> str:
        """Get the weight category for a specific skill"""
        skill_lower = skill.lower()
        
        # Check in weight categories (highest priority first)
        if any(skill_lower in s.lower() for s in self.skill_weights.critical):
            return 'critical'
        elif any(skill_lower in s.lower() for s in self.skill_weights.important):
            return 'important'
        elif any(skill_lower in s.lower() for s in self.skill_weights.preferred):
            return 'preferred'
        elif any(skill_lower in s.lower() for s in self.skill_weights.bonus):
            return 'bonus'
        
        # Check in requirements
        if any(skill_lower in s.lower() for s in self.requirements.required_skills):
            return 'important'  # Default weight for required skills
        elif any(skill_lower in s.lower() for s in self.requirements.preferred_skills):
            return 'preferred'  # Default weight for preferred skills
        
        return 'unknown'
    
    def get_experience_years_required(self) -> tuple:
        """Extract minimum and maximum experience years"""
        if not self.requirements.experience_years:
            return (0, None)
        
        exp_text = self.requirements.experience_years.lower()
        
        # Look for common patterns
        year_patterns = [
            r'(\d+)[\-\s]*(\d+)?\s*years?',  # "3-5 years" or "3 years"
            r'(\d+)\+?\s*years?',            # "3+ years"
            r'minimum\s*(\d+)\s*years?',     # "minimum 3 years"
            r'at least\s*(\d+)\s*years?',    # "at least 3 years"
        ]
        
        for pattern in year_patterns:
            match = re.search(pattern, exp_text)
            if match:
                min_years = int(match.group(1))
                max_years = int(match.group(2)) if match.group(2) else None
                return (min_years, max_years)
        
        return (0, None)
    
    def categorize_job_level(self) -> str:
        """Determine job level based on title and requirements"""
        if self.level:
            return self.level
        
        title_lower = (self.title or "").lower()
        
        # Executive/Leadership levels
        if any(keyword in title_lower for keyword in 
               ['ceo', 'cto', 'cio', 'vp', 'vice president', 'director', 'head of']):
            return 'Executive'
        
        # Senior levels
        elif any(keyword in title_lower for keyword in 
                ['senior', 'lead', 'principal', 'architect', 'manager']):
            return 'Senior'
        
        # Entry levels
        elif any(keyword in title_lower for keyword in 
                ['junior', 'entry', 'associate', 'intern', 'trainee', 'graduate']):
            return 'Entry'
        
        # Check experience requirements
        min_years, _ = self.get_experience_years_required()
        if min_years == 0:
            return 'Entry'
        elif min_years >= 7:
            return 'Senior'
        elif min_years >= 3:
            return 'Mid'
        else:
            return 'Entry'
    
    def get_skill_distribution(self) -> Dict[str, int]:
        """Get distribution of skills by weight category"""
        return {
            'critical': len(self.skill_weights.critical),
            'important': len(self.skill_weights.important),
            'preferred': len(self.skill_weights.preferred),
            'bonus': len(self.skill_weights.bonus),
            'required': len(self.requirements.required_skills),
            'preferred_req': len(self.requirements.preferred_skills),
            'total': len(self.all_skills)
        }
    
    def search_requirements(self, query: str) -> List[str]:
        """Search for requirements matching a query"""
        query_lower = query.lower()
        matching_reqs = []
        
        # Search in responsibilities
        for resp in self.responsibilities:
            if query_lower in resp.lower():
                matching_reqs.append(f"Responsibility: {resp}")
        
        # Search in skills
        for skill in self.all_skills:
            if query_lower in skill.lower():
                weight = self.get_skill_weight(skill)
                matching_reqs.append(f"Skill ({weight}): {skill}")
        
        return matching_reqs
    
    def calculate_skill_score(self, candidate_skills: Set[str]) -> Dict[str, any]:
        """Calculate how well candidate skills match job requirements"""
        # Weight values for different skill categories
        weight_values = {
            'critical': 10,
            'important': 7,
            'preferred': 5,
            'bonus': 3
        }
        
        total_possible_score = 0
        achieved_score = 0
        skill_matches = {}
        
        # Calculate for each skill category
        for category, skills in [
            ('critical', self.skill_weights.critical),
            ('important', self.skill_weights.important),
            ('preferred', self.skill_weights.preferred),
            ('bonus', self.skill_weights.bonus)
        ]:
            category_matches = []
            category_score = 0
            category_possible = len(skills) * weight_values[category]
            
            for skill in skills:
                has_skill = any(skill.lower() in cs.lower() or cs.lower() in skill.lower() 
                              for cs in candidate_skills)
                if has_skill:
                    category_score += weight_values[category]
                    category_matches.append(skill)
            
            skill_matches[category] = {
                'matched': category_matches,
                'total': len(skills),
                'score': category_score,
                'possible': category_possible,
                'percentage': (category_score / category_possible * 100) if category_possible > 0 else 0
            }
            
            total_possible_score += category_possible
            achieved_score += category_score
        
        # Overall score
        overall_percentage = (achieved_score / total_possible_score * 100) if total_possible_score > 0 else 0
        
        return {
            'overall_score': achieved_score,
            'total_possible': total_possible_score,
            'percentage': round(overall_percentage, 2),
            'category_breakdown': skill_matches,
            'critical_skills_met': len(skill_matches['critical']['matched']),
            'total_critical_skills': len(self.skill_weights.critical),
            'meets_critical_requirements': (
                len(skill_matches['critical']['matched']) >= len(self.skill_weights.critical) * 0.8
            )
        }
    
    def get_missing_critical_skills(self, candidate_skills: Set[str]) -> List[str]:
        """Get list of critical skills that candidate is missing"""
        missing_skills = []
        
        for skill in self.skill_weights.critical:
            has_skill = any(skill.lower() in cs.lower() or cs.lower() in skill.lower() 
                          for cs in candidate_skills)
            if not has_skill:
                missing_skills.append(skill)
        
        return missing_skills
    
    def to_dict(self) -> Dict[str, any]:
        """Convert job description to dictionary for serialization"""
        return {
            'file_info': {
                'path': self.file_path,
                'name': self.file_name,
                'format': self.file_format,
                'size': self.file_size,
                'processing_date': self.processing_date.isoformat()
            },
            'job_info': {
                'title': self.title,
                'department': self.department,
                'job_type': self.job_type,
                'level': self.level,
                'categorized_level': self.categorize_job_level()
            },
            'company': {
                'name': self.company.name,
                'industry': self.company.industry,
                'size': self.company.size,
                'location': self.company.location,
                'website': self.company.website,
                'description': self.company.description
            },
            'content': {
                'summary': self.summary,
                'description': self.description,
                'responsibilities': self.responsibilities
            },
            'requirements': {
                'education': self.requirements.education,
                'experience_years': self.requirements.experience_years,
                'experience_range': self.get_experience_years_required(),
                'required_skills': self.requirements.required_skills,
                'preferred_skills': self.requirements.preferred_skills,
                'certifications': self.requirements.certifications,
                'languages': self.requirements.languages
            },
            'skill_weights': {
                'critical': self.skill_weights.critical,
                'important': self.skill_weights.important,
                'preferred': self.skill_weights.preferred,
                'bonus': self.skill_weights.bonus,
                'all_skills': list(self.all_skills)
            },
            'benefits': {
                'salary_range': self.benefits.salary_range,
                'benefits': self.benefits.benefits,
                'work_arrangement': self.benefits.work_arrangement,
                'schedule': self.benefits.schedule
            },
            'analysis': {
                'text_metrics': self.text_metrics,
                'keywords': self.keywords,
                'technical_terms': self.technical_terms,
                'skill_distribution': self.get_skill_distribution()
            },
            'processing': {
                'success': self.processing_success,
                'errors': self.processing_errors,
                'confidence': self.extraction_confidence
            }
        }
    
    def __str__(self) -> str:
        """String representation of the job description"""
        company_name = self.company.name or 'Unknown Company'
        return f"Job({self.title or 'Unknown Position'} at {company_name})"
    
    def __repr__(self) -> str:
        """Detailed representation of the job description"""
        return (f"JobDescription(title='{self.title}', company='{self.company.name}', "
                f"file='{self.file_name}', skills={len(self.all_skills)}, "
                f"level='{self.categorize_job_level()}')")