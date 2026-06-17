"""
Resume Data Model
================

Data class representing a resume with all extracted information.
Provides structured access to resume content and analysis results.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from datetime import datetime
from pathlib import Path


@dataclass
class Contact:
    """Contact information extracted from resume"""
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None


@dataclass
class Education:
    """Education entry"""
    degree: str
    institution: str
    year: Optional[str] = None
    gpa: Optional[str] = None
    location: Optional[str] = None
    details: List[str] = field(default_factory=list)


@dataclass
class Experience:
    """Work experience entry"""
    title: str
    company: str
    duration: Optional[str] = None
    location: Optional[str] = None
    description: List[str] = field(default_factory=list)
    skills_used: List[str] = field(default_factory=list)


@dataclass
class Project:
    """Project entry"""
    name: str
    description: str
    technologies: List[str] = field(default_factory=list)
    duration: Optional[str] = None
    url: Optional[str] = None


@dataclass
class Certification:
    """Certification or award entry"""
    name: str
    issuer: Optional[str] = None
    date: Optional[str] = None
    expiry: Optional[str] = None
    credential_id: Optional[str] = None


@dataclass
class SkillCategory:
    """Skills organized by category"""
    technical: List[str] = field(default_factory=list)
    programming: List[str] = field(default_factory=list)
    frameworks: List[str] = field(default_factory=list)
    databases: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    cloud: List[str] = field(default_factory=list)
    soft_skills: List[str] = field(default_factory=list)
    languages: List[str] = field(default_factory=list)
    other: List[str] = field(default_factory=list)


@dataclass
class Resume:
    """Complete resume data model"""
    
    # File information
    file_path: str
    file_name: str = field(init=False)
    file_format: str = field(init=False)
    file_size: int = 0
    processing_date: datetime = field(default_factory=datetime.now)
    
    # Personal information
    name: Optional[str] = None
    contact: Contact = field(default_factory=Contact)
    summary: Optional[str] = None
    objective: Optional[str] = None
    
    # Main sections
    education: List[Education] = field(default_factory=list)
    experience: List[Experience] = field(default_factory=list)
    projects: List[Project] = field(default_factory=list)
    certifications: List[Certification] = field(default_factory=list)
    
    # Skills
    skills: SkillCategory = field(default_factory=SkillCategory)
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
        
        # Update all_skills set when skills are modified
        self._update_all_skills()
    
    def _update_all_skills(self):
        """Update the combined skills set"""
        self.all_skills.clear()
        
        # Add all skills from categories
        for skill_list in [
            self.skills.technical, self.skills.programming, 
            self.skills.frameworks, self.skills.databases,
            self.skills.tools, self.skills.cloud, 
            self.skills.soft_skills, self.skills.languages,
            self.skills.other
        ]:
            self.all_skills.update(skill_list)
    
    def add_skill(self, skill: str, category: str = 'other'):
        """Add a skill to the appropriate category"""
        skill = skill.strip()
        if not skill:
            return
        
        category_map = {
            'technical': self.skills.technical,
            'programming': self.skills.programming,
            'frameworks': self.skills.frameworks,
            'databases': self.skills.databases,
            'tools': self.skills.tools,
            'cloud': self.skills.cloud,
            'soft_skills': self.skills.soft_skills,
            'languages': self.skills.languages,
            'other': self.skills.other
        }
        
        if category in category_map:
            if skill not in category_map[category]:
                category_map[category].append(skill)
                self._update_all_skills()
    
    def get_total_experience_years(self) -> float:
        """Calculate total years of experience (rough estimate)"""
        if not self.experience:
            return 0.0
        
        total_years = 0.0
        
        for exp in self.experience:
            if exp.duration:
                # Simple parsing for common duration formats
                duration_lower = exp.duration.lower()
                
                # Look for year patterns
                if 'year' in duration_lower:
                    import re
                    year_matches = re.findall(r'(\d+(?:\.\d+)?)\s*year', duration_lower)
                    if year_matches:
                        total_years += float(year_matches[0])
                
                # Look for month patterns and convert to years
                elif 'month' in duration_lower:
                    import re
                    month_matches = re.findall(r'(\d+)\s*month', duration_lower)
                    if month_matches:
                        total_years += float(month_matches[0]) / 12
        
        return round(total_years, 1)
    
    def get_education_level(self) -> str:
        """Determine highest education level"""
        if not self.education:
            return "Not specified"
        
        education_hierarchy = {
            'phd': 5, 'doctorate': 5, 'ph.d': 5,
            'master': 4, 'masters': 4, 'mba': 4, 'ms': 4, 'ma': 4,
            'bachelor': 3, 'bachelors': 3, 'bs': 3, 'ba': 3, 'btech': 3, 'be': 3,
            'associate': 2, 'diploma': 1, 'certificate': 1
        }
        
        highest_level = 0
        highest_degree = ""
        
        for edu in self.education:
            degree_lower = edu.degree.lower()
            for key, level in education_hierarchy.items():
                if key in degree_lower and level > highest_level:
                    highest_level = level
                    highest_degree = edu.degree
        
        return highest_degree if highest_degree else self.education[0].degree
    
    def get_skill_summary(self) -> Dict[str, int]:
        """Get summary of skills by category"""
        return {
            'technical': len(self.skills.technical),
            'programming': len(self.skills.programming),
            'frameworks': len(self.skills.frameworks),
            'databases': len(self.skills.databases),
            'tools': len(self.skills.tools),
            'cloud': len(self.skills.cloud),
            'soft_skills': len(self.skills.soft_skills),
            'languages': len(self.skills.languages),
            'other': len(self.skills.other),
            'total': len(self.all_skills)
        }
    
    def search_skills(self, query: str) -> List[str]:
        """Search for skills matching a query"""
        query_lower = query.lower()
        matching_skills = []
        
        for skill in self.all_skills:
            if query_lower in skill.lower():
                matching_skills.append(skill)
        
        return sorted(matching_skills)
    
    def has_skill(self, skill: str) -> bool:
        """Check if resume contains a specific skill"""
        skill_lower = skill.lower()
        return any(skill_lower in s.lower() for s in self.all_skills)
    
    def get_matching_skills(self, required_skills: List[str]) -> Dict[str, bool]:
        """Check which required skills are present in the resume"""
        matches = {}
        
        for required_skill in required_skills:
            matches[required_skill] = self.has_skill(required_skill)
        
        return matches
    
    def calculate_completeness_score(self) -> float:
        """Calculate how complete the resume information is"""
        score = 0.0
        max_score = 100.0
        
        # Essential information (40 points)
        if self.name:
            score += 10
        if self.contact.email:
            score += 10
        if self.contact.phone:
            score += 10
        if self.experience:
            score += 10
        
        # Important sections (40 points)
        if self.education:
            score += 10
        if self.all_skills:
            score += 15
        if self.summary or self.objective:
            score += 10
        if self.text_metrics.get('word_count', 0) > 100:
            score += 5
        
        # Additional information (20 points)
        if self.projects:
            score += 5
        if self.certifications:
            score += 5
        if self.contact.linkedin or self.contact.github:
            score += 5
        if len(self.all_skills) >= 10:
            score += 5
        
        return round(score, 1)
    
    def to_dict(self) -> Dict[str, any]:
        """Convert resume to dictionary for serialization"""
        return {
            'file_info': {
                'path': self.file_path,
                'name': self.file_name,
                'format': self.file_format,
                'size': self.file_size,
                'processing_date': self.processing_date.isoformat()
            },
            'personal': {
                'name': self.name,
                'contact': {
                    'email': self.contact.email,
                    'phone': self.contact.phone,
                    'location': self.contact.location,
                    'linkedin': self.contact.linkedin,
                    'github': self.contact.github,
                    'website': self.contact.website
                },
                'summary': self.summary,
                'objective': self.objective
            },
            'sections': {
                'education': [
                    {
                        'degree': edu.degree,
                        'institution': edu.institution,
                        'year': edu.year,
                        'gpa': edu.gpa,
                        'location': edu.location,
                        'details': edu.details
                    } for edu in self.education
                ],
                'experience': [
                    {
                        'title': exp.title,
                        'company': exp.company,
                        'duration': exp.duration,
                        'location': exp.location,
                        'description': exp.description,
                        'skills_used': exp.skills_used
                    } for exp in self.experience
                ],
                'projects': [
                    {
                        'name': proj.name,
                        'description': proj.description,
                        'technologies': proj.technologies,
                        'duration': proj.duration,
                        'url': proj.url
                    } for proj in self.projects
                ],
                'certifications': [
                    {
                        'name': cert.name,
                        'issuer': cert.issuer,
                        'date': cert.date,
                        'expiry': cert.expiry,
                        'credential_id': cert.credential_id
                    } for cert in self.certifications
                ]
            },
            'skills': {
                'technical': self.skills.technical,
                'programming': self.skills.programming,
                'frameworks': self.skills.frameworks,
                'databases': self.skills.databases,
                'tools': self.skills.tools,
                'cloud': self.skills.cloud,
                'soft_skills': self.skills.soft_skills,
                'languages': self.skills.languages,
                'other': self.skills.other,
                'all_skills': list(self.all_skills)
            },
            'analysis': {
                'text_metrics': self.text_metrics,
                'keywords': self.keywords,
                'technical_terms': self.technical_terms,
                'total_experience_years': self.get_total_experience_years(),
                'education_level': self.get_education_level(),
                'skill_summary': self.get_skill_summary(),
                'completeness_score': self.calculate_completeness_score()
            },
            'processing': {
                'success': self.processing_success,
                'errors': self.processing_errors,
                'confidence': self.extraction_confidence
            }
        }
    
    def __str__(self) -> str:
        """String representation of the resume"""
        return f"Resume({self.name or 'Unknown'} - {self.file_name})"
    
    def __repr__(self) -> str:
        """Detailed representation of the resume"""
        return (f"Resume(name='{self.name}', file='{self.file_name}', "
                f"skills={len(self.all_skills)}, experience={len(self.experience)}, "
                f"education={len(self.education)})")