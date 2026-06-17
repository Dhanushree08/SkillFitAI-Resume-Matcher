"""
Skill Extraction Module
=======================

Advanced skill extraction and analysis for resumes and job descriptions.
Supports technical skills, soft skills, and domain-specific competencies.
"""

import re
from typing import List, Dict, Set, Tuple
from collections import Counter
from dataclasses import dataclass


@dataclass
class SkillMatch:
    """Represents a matched skill with context"""
    skill: str
    category: str
    confidence: float
    frequency: int
    context: List[str]


class SkillExtractor:
    """Advanced skill extraction engine"""
    
    def __init__(self):
        # Technical Skills Database
        self.technical_skills = {
            'programming_languages': [
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust',
                'swift', 'kotlin', 'scala', 'ruby', 'php', 'perl', 'r', 'matlab',
                'dart', 'elixir', 'clojure', 'haskell', 'f#', 'erlang', 'julia'
            ],
            'web_technologies': [
                'html', 'html5', 'css', 'css3', 'sass', 'scss', 'less', 'bootstrap',
                'tailwind css', 'material-ui', 'react', 'angular', 'vue', 'vue.js',
                'svelte', 'ember', 'backbone', 'jquery', 'node.js', 'express',
                'next.js', 'nuxt.js', 'gatsby', 'webpack', 'babel', 'parcel'
            ],
            'backend_frameworks': [
                'django', 'flask', 'fastapi', 'spring', 'spring boot', 'laravel',
                'symfony', 'rails', 'ruby on rails', 'asp.net', '.net core',
                'express.js', 'koa', 'nestjs', 'gin', 'fiber', 'echo'
            ],
            'databases': [
                'mysql', 'postgresql', 'sqlite', 'oracle', 'sql server', 'mongodb',
                'cassandra', 'redis', 'elasticsearch', 'neo4j', 'dynamodb',
                'firebase', 'couchdb', 'influxdb', 'clickhouse', 'snowflake'
            ],
            'cloud_platforms': [
                'aws', 'amazon web services', 'azure', 'google cloud', 'gcp',
                'digital ocean', 'heroku', 'vercel', 'netlify', 'cloudflare',
                'linode', 'vultr', 'oracle cloud', 'ibm cloud', 'alibaba cloud'
            ],
            'devops_tools': [
                'docker', 'kubernetes', 'jenkins', 'gitlab ci', 'github actions',
                'circleci', 'travis ci', 'ansible', 'terraform', 'chef', 'puppet',
                'vagrant', 'helm', 'istio', 'prometheus', 'grafana', 'elk stack'
            ],
            'ml_ai_tools': [
                'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy',
                'matplotlib', 'seaborn', 'plotly', 'jupyter', 'opencv', 'nltk',
                'spacy', 'transformers', 'hugging face', 'mlflow', 'kubeflow'
            ],
            'mobile_development': [
                'react native', 'flutter', 'ionic', 'xamarin', 'cordova',
                'swift ui', 'jetpack compose', 'android studio', 'xcode'
            ],
            'version_control': [
                'git', 'github', 'gitlab', 'bitbucket', 'svn', 'mercurial',
                'perforce', 'bazaar', 'git flow', 'github flow'
            ],
            'testing_tools': [
                'jest', 'mocha', 'jasmine', 'cypress', 'selenium', 'pytest',
                'unittest', 'junit', 'testng', 'karma', 'protractor', 'cucumber'
            ]
        }
        
        # Soft Skills Database
        self.soft_skills = {
            'communication': [
                'communication', 'verbal communication', 'written communication',
                'presentation', 'public speaking', 'negotiation', 'interpersonal'
            ],
            'leadership': [
                'leadership', 'team leadership', 'project management', 'mentoring',
                'coaching', 'delegation', 'decision making', 'strategic thinking'
            ],
            'analytical': [
                'analytical', 'problem solving', 'critical thinking', 'research',
                'data analysis', 'attention to detail', 'troubleshooting'
            ],
            'collaboration': [
                'teamwork', 'collaboration', 'cross-functional', 'stakeholder management',
                'conflict resolution', 'consensus building', 'cultural sensitivity'
            ],
            'adaptability': [
                'adaptability', 'flexibility', 'learning agility', 'resilience',
                'change management', 'innovation', 'creativity', 'continuous learning'
            ]
        }
        
        # Domain-specific skills
        self.domain_skills = {
            'fintech': [
                'financial modeling', 'risk management', 'compliance', 'trading',
                'blockchain', 'cryptocurrency', 'payment processing', 'regtech'
            ],
            'healthcare': [
                'hipaa', 'hl7', 'fhir', 'medical imaging', 'telemedicine',
                'clinical data', 'pharmaceutical', 'biomedical'
            ],
            'ecommerce': [
                'e-commerce', 'payment gateway', 'shopping cart', 'inventory management',
                'order management', 'customer analytics', 'conversion optimization'
            ],
            'gaming': [
                'game development', 'unity', 'unreal engine', 'game design',
                'graphics programming', 'shader programming', 'physics engine'
            ]
        }
        
        # Compile all skills into searchable patterns
        self._compile_skill_patterns()
    
    def _compile_skill_patterns(self):
        """Compile all skills into regex patterns for efficient matching"""
        self.skill_patterns = {}
        self.skill_categories = {}
        
        # Technical skills
        for category, skills in self.technical_skills.items():
            for skill in skills:
                pattern = self._create_skill_pattern(skill)
                self.skill_patterns[skill] = pattern
                self.skill_categories[skill] = f"technical_{category}"
        
        # Soft skills
        for category, skills in self.soft_skills.items():
            for skill in skills:
                pattern = self._create_skill_pattern(skill)
                self.skill_patterns[skill] = pattern
                self.skill_categories[skill] = f"soft_{category}"
        
        # Domain skills
        for category, skills in self.domain_skills.items():
            for skill in skills:
                pattern = self._create_skill_pattern(skill)
                self.skill_patterns[skill] = pattern
                self.skill_categories[skill] = f"domain_{category}"
    
    def _create_skill_pattern(self, skill: str) -> re.Pattern:
        """Create regex pattern for skill matching"""
        # Handle special characters in skill names
        escaped_skill = re.escape(skill)
        
        # Create flexible pattern that handles variations
        pattern = r'\b' + escaped_skill.replace(r'\ ', r'[\s\-]*') + r'\b'
        
        return re.compile(pattern, re.IGNORECASE)
    
    def extract_skills(self, text: str, include_context: bool = False) -> List[SkillMatch]:
        """Extract skills from text with optional context"""
        if not text:
            return []
        
        found_skills = []
        text_lower = text.lower()
        
        for skill, pattern in self.skill_patterns.items():
            matches = list(pattern.finditer(text))
            
            if matches:
                # Calculate confidence based on context and frequency
                confidence = self._calculate_confidence(skill, text, matches)
                
                # Extract context if requested
                context = []
                if include_context:
                    context = self._extract_context(text, matches)
                
                skill_match = SkillMatch(
                    skill=skill,
                    category=self.skill_categories[skill],
                    confidence=confidence,
                    frequency=len(matches),
                    context=context
                )
                
                found_skills.append(skill_match)
        
        # Sort by confidence and remove duplicates
        found_skills.sort(key=lambda x: x.confidence, reverse=True)
        
        return found_skills
    
    def _calculate_confidence(self, skill: str, text: str, matches: List) -> float:
        """Calculate confidence score for skill match"""
        base_confidence = 0.5
        
        # Frequency bonus
        frequency_bonus = min(0.3, len(matches) * 0.1)
        
        # Context bonus - check if skill appears in relevant context
        context_bonus = 0.0
        for match in matches:
            start, end = match.span()
            context_window = text[max(0, start-50):min(len(text), end+50)]
            
            # Look for context indicators
            context_indicators = [
                'experience', 'skilled', 'proficient', 'expert', 'knowledge',
                'familiar', 'worked with', 'used', 'developed', 'implemented'
            ]
            
            for indicator in context_indicators:
                if indicator in context_window.lower():
                    context_bonus = max(context_bonus, 0.2)
                    break
        
        # Category-specific adjustments
        category = self.skill_categories[skill]
        if 'technical' in category:
            # Technical skills get higher base confidence
            base_confidence = 0.6
        elif 'soft' in category:
            # Soft skills need stronger context
            base_confidence = 0.4
            context_bonus *= 0.8
        
        final_confidence = min(1.0, base_confidence + frequency_bonus + context_bonus)
        return final_confidence
    
    def _extract_context(self, text: str, matches: List) -> List[str]:
        """Extract context around skill matches"""
        contexts = []
        
        for match in matches:
            start, end = match.span()
            # Get surrounding context
            context_start = max(0, start - 30)
            context_end = min(len(text), end + 30)
            
            context = text[context_start:context_end].strip()
            if context and len(context) > 10:
                contexts.append(context)
        
        # Remove duplicates and limit
        unique_contexts = list(set(contexts))[:3]
        return unique_contexts
    
    def get_skill_summary(self, skills: List[SkillMatch]) -> Dict[str, any]:
        """Generate summary statistics for extracted skills"""
        if not skills:
            return {
                'total_skills': 0,
                'categories': {},
                'confidence_stats': {},
                'top_skills': []
            }
        
        # Category breakdown
        category_counts = Counter(skill.category for skill in skills)
        category_breakdown = {}
        
        for category, count in category_counts.items():
            category_skills = [s for s in skills if s.category == category]
            avg_confidence = sum(s.confidence for s in category_skills) / len(category_skills)
            
            category_breakdown[category] = {
                'count': count,
                'avg_confidence': avg_confidence,
                'skills': [s.skill for s in category_skills]
            }
        
        # Confidence statistics
        confidences = [skill.confidence for skill in skills]
        confidence_stats = {
            'avg': sum(confidences) / len(confidences),
            'min': min(confidences),
            'max': max(confidences),
            'high_confidence_count': sum(1 for c in confidences if c > 0.7)
        }
        
        # Top skills
        top_skills = sorted(skills, key=lambda x: x.confidence, reverse=True)[:10]
        
        return {
            'total_skills': len(skills),
            'categories': category_breakdown,
            'confidence_stats': confidence_stats,
            'top_skills': [(s.skill, s.confidence) for s in top_skills]
        }
    
    def match_skills(self, resume_skills: List[SkillMatch], job_skills: List[SkillMatch]) -> Dict[str, any]:
        """Match resume skills against job requirements"""
        if not resume_skills or not job_skills:
            return {
                'match_score': 0.0,
                'matched_skills': [],
                'missing_skills': [],
                'extra_skills': []
            }
        
        # Convert to sets for matching
        resume_skill_names = {s.skill.lower() for s in resume_skills}
        job_skill_names = {s.skill.lower() for s in job_skills}
        
        # Find matches
        matched = resume_skill_names.intersection(job_skill_names)
        missing = job_skill_names - resume_skill_names
        extra = resume_skill_names - job_skill_names
        
        # Calculate weighted match score
        total_job_skills = len(job_skill_names)
        matched_count = len(matched)
        
        if total_job_skills == 0:
            match_score = 0.0
        else:
            # Base score from percentage match
            base_score = matched_count / total_job_skills
            
            # Weight by skill importance and confidence
            weighted_score = 0.0
            total_weight = 0.0
            
            for job_skill in job_skills:
                skill_weight = job_skill.confidence * job_skill.frequency
                total_weight += skill_weight
                
                if job_skill.skill.lower() in matched:
                    weighted_score += skill_weight
            
            if total_weight > 0:
                match_score = weighted_score / total_weight
            else:
                match_score = base_score
        
        return {
            'match_score': min(1.0, match_score),
            'matched_skills': list(matched),
            'missing_skills': list(missing),
            'extra_skills': list(extra),
            'match_percentage': (matched_count / total_job_skills * 100) if total_job_skills > 0 else 0
        }