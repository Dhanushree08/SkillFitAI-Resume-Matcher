"""
Resume-Job Matching Engine
=========================

Core matching algorithms for SkillFitAI system that compares resumes
with job descriptions and provides similarity scoring.
"""

import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import json


@dataclass
class MatchResult:
    """Result of a resume-job match"""
    resume_name: str
    job_name: str
    similarity_score: float
    matched_skills: List[str]
    skill_count: int
    resume_format: str
    job_format: str


class SkillExtractor:
    """Extracts skills from text content"""
    
    def __init__(self):
        self.tech_skills = [
            'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue', 'vue.js',
            'node.js', 'nodejs', 'express', 'express.js', 'django', 'flask', 'fastapi',
            'spring', 'spring boot', 'html', 'css', 'bootstrap', 'sass', 'scss',
            'c++', 'c#', '.net', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin',
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
            'aws', 'azure', 'google cloud', 'gcp', 'docker', 'kubernetes', 'jenkins',
            'git', 'github', 'gitlab', 'ci/cd', 'devops', 'terraform', 'ansible',
            'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras',
            'scikit-learn', 'data science', 'pandas', 'numpy', 'matplotlib', 'seaborn',
            'tableau', 'power bi', 'ai', 'nlp', 'natural language processing',
            'rest', 'restful', 'api', 'graphql', 'microservices', 'agile', 'scrum',
            'linux', 'windows', 'bash', 'powershell', 'networking', 'cybersecurity',
            'analytical skills', 'communication', 'leadership', 'problem solving',
            'project management', 'time management', 'team collaboration',
            'ui/ux', 'design', 'figma', 'photoshop', 'blockchain', 'scala', 'r'
        ]
        
        # Compile skill patterns for efficient matching
        self.skill_patterns = {
            skill: re.compile(r'\b' + re.escape(skill) + r'\b', re.IGNORECASE)
            for skill in self.tech_skills
        }
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract technical skills from text"""
        if not text:
            return []
        
        found_skills = []
        text_lower = text.lower()
        
        # Use compiled patterns for efficient matching
        for skill, pattern in self.skill_patterns.items():
            if pattern.search(text_lower):
                found_skills.append(skill)
        
        return list(set(found_skills))  # Remove duplicates
    
    def get_skill_frequency(self, text: str) -> Dict[str, int]:
        """Get frequency count of skills in text"""
        if not text:
            return {}
        
        skill_freq = {}
        text_lower = text.lower()
        
        for skill, pattern in self.skill_patterns.items():
            matches = pattern.findall(text_lower)
            if matches:
                skill_freq[skill] = len(matches)
        
        return skill_freq


class DocumentProcessor:
    """Processes various document formats"""
    
    def __init__(self):
        self.sensitive_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'(\+?\d{1,4}[-.\s]?)?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
            'address': r'\b\d+\s+[A-Za-z\s,]+\b(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Place|Pl)\b',
        }
    
    def read_document(self, file_path: str) -> str:
        """Read document content regardless of format"""
        file_path = Path(file_path)
        
        try:
            # Read all files as text (including placeholders)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Clean up format-specific content
            if content.startswith('DOCX FORMAT PLACEHOLDER'):
                content = content.replace('DOCX FORMAT PLACEHOLDER\n\n', '')
            elif content.startswith('PDF FORMAT PLACEHOLDER'):
                content = content.replace('PDF FORMAT PLACEHOLDER\n\n', '')
            elif file_path.suffix == '.rtf':
                # Clean RTF formatting
                content = re.sub(r'\\[a-z]+\d*', ' ', content)
                content = re.sub(r'[{}]', ' ', content)
                content = content.replace('\\par', '\n')
                
            return content
            
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""
    
    def redact_sensitive_info(self, text: str) -> str:
        """Redact sensitive information from text"""
        if not text:
            return text
            
        redacted_text = text
        
        # Redact patterns
        for info_type, pattern in self.sensitive_patterns.items():
            redacted_text = re.sub(pattern, f'[REDACTED_{info_type.upper()}]', redacted_text)
        
        return redacted_text
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s\.\,\-\+\(\)]', ' ', text)
        
        # Normalize whitespace
        text = ' '.join(text.split())
        
        return text.strip()


class SkillMatcher:
    """Core skill matching algorithm"""
    
    def __init__(self):
        self.skill_extractor = SkillExtractor()
    
    def calculate_similarity(self, resume_skills: List[str], job_skills: List[str]) -> Tuple[float, List[str]]:
        """Calculate similarity between resume and job skills"""
        if not resume_skills or not job_skills:
            return 0.0, []
        
        # Convert to sets for efficient operations
        resume_set = set(skill.lower() for skill in resume_skills)
        job_set = set(skill.lower() for skill in job_skills)
        
        # Find intersection (matched skills)
        matched_skills = list(resume_set.intersection(job_set))
        
        if not matched_skills:
            return 0.0, []
        
        # Calculate Jaccard similarity with weighting
        union_size = len(resume_set.union(job_set))
        intersection_size = len(matched_skills)
        
        # Base Jaccard similarity
        jaccard_similarity = intersection_size / union_size if union_size > 0 else 0.0
        
        # Add bonus for high match count
        match_bonus = min(0.3, intersection_size * 0.02)
        
        # Final similarity score
        similarity_score = min(1.0, jaccard_similarity + match_bonus)
        
        return similarity_score, matched_skills
    
    def match_resume_to_job(self, resume_text: str, job_text: str) -> Tuple[float, List[str], int]:
        """Match a single resume to a single job"""
        # Extract skills
        resume_skills = self.skill_extractor.extract_skills(resume_text)
        job_skills = self.skill_extractor.extract_skills(job_text)
        
        # Calculate similarity
        similarity_score, matched_skills = self.calculate_similarity(resume_skills, job_skills)
        
        return similarity_score, matched_skills, len(matched_skills)


class ResumeJobMatcher:
    """Main matcher class for the SkillFitAI system"""
    
    def __init__(self, skill_extractor=None, document_processor=None):
        self.document_processor = document_processor or DocumentProcessor()
        self.skill_extractor = skill_extractor or SkillExtractor()
        self.skill_matcher = SkillMatcher()
        self.results = []
        
    def load_documents(self, resume_dir: str, job_dir: str) -> Tuple[List[Dict], List[Dict]]:
        """Load all resumes and job descriptions"""
        resumes = []
        jobs = []
        
        # Load resumes
        resume_path = Path(resume_dir)
        if resume_path.exists():
            for file_path in resume_path.iterdir():
                if file_path.is_file() and not file_path.name.startswith('.'):
                    content = self.document_processor.read_document(file_path)
                    if content.strip():  # Only add non-empty documents
                        resumes.append({
                            'name': file_path.name,
                            'path': str(file_path),
                            'content': content,
                            'format': file_path.suffix
                        })
        
        # Load job descriptions
        job_path = Path(job_dir)
        if job_path.exists():
            for file_path in job_path.iterdir():
                if file_path.is_file() and not file_path.name.startswith('.'):
                    content = self.document_processor.read_document(file_path)
                    if content.strip():  # Only add non-empty documents
                        jobs.append({
                            'name': file_path.name,
                            'path': str(file_path), 
                            'content': content,
                            'format': file_path.suffix
                        })
        
        return resumes, jobs
    
    def match_all(self, resumes: List[Dict], jobs: List[Dict], top_k: int = 5) -> List[MatchResult]:
        """Match all resumes against all jobs"""
        all_results = []
        
        for job in jobs:
            job_results = []
            
            # Match each resume against this job
            for resume in resumes:
                similarity_score, matched_skills, skill_count = self.skill_matcher.match_resume_to_job(
                    resume['content'], job['content']
                )
                
                result = MatchResult(
                    resume_name=resume['name'],
                    job_name=job['name'],
                    similarity_score=similarity_score,
                    matched_skills=matched_skills,
                    skill_count=skill_count,
                    resume_format=resume['format'],
                    job_format=job['format']
                )
                
                job_results.append(result)
            
            # Sort by similarity score and take top K
            job_results.sort(key=lambda x: x.similarity_score, reverse=True)
            all_results.extend(job_results[:top_k])
        
        return all_results
    
    def save_results(self, results: List[MatchResult], output_dir: str = "results") -> None:
        """Save matching results to files"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Convert results to dictionaries for JSON serialization
        results_data = []
        for result in results:
            results_data.append({
                'resume_name': result.resume_name,
                'job_name': result.job_name,
                'similarity_score': result.similarity_score,
                'matched_skills': result.matched_skills,
                'skill_count': result.skill_count,
                'resume_format': result.resume_format,
                'job_format': result.job_format
            })
        
        # Save as JSON
        json_file = output_path / "matching_results.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=2, ensure_ascii=False)
        
        # Save as text report
        report_file = output_path / "matching_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("SkillFitAI Matching Report\n")
            f.write("=" * 50 + "\n\n")
            
            for i, result in enumerate(results):
                f.write(f"Match {i + 1}:\n")
                f.write(f"  Resume: {result.resume_name} ({result.resume_format})\n")
                f.write(f"  Job: {result.job_name} ({result.job_format})\n")
                f.write(f"  Similarity Score: {result.similarity_score:.4f}\n")
                f.write(f"  Matched Skills ({result.skill_count}): {', '.join(result.matched_skills[:10])}\n")
                if len(result.matched_skills) > 10:
                    f.write(f"    ... and {len(result.matched_skills) - 10} more\n")
                f.write("\n")
        
        print(f"✅ Results saved to {output_dir}/")
    
    def match_resume_to_job(self, resume, job_description):
        """Match Resume and JobDescription objects"""
        from dataclasses import dataclass
        
        @dataclass
        class MatchResult:
            overall_score: float
            skill_match_percentage: float
            matched_skills: List[str]
            missing_skills: List[str]
            bonus_skills: List[str]
            recommendation: str
            confidence: float
        
        # Get skills from both objects
        resume_skills = resume.all_skills if hasattr(resume, 'all_skills') else set()
        job_skills = job_description.all_skills if hasattr(job_description, 'all_skills') else set()
        
        # Calculate matches
        matched_skills = list(resume_skills.intersection(job_skills))
        missing_skills = list(job_skills - resume_skills)
        bonus_skills = list(resume_skills - job_skills)
        
        # Calculate scores
        if len(job_skills) > 0:
            skill_match_percentage = (len(matched_skills) / len(job_skills)) * 100
        else:
            skill_match_percentage = 0
        
        # Overall score based on multiple factors
        base_score = skill_match_percentage / 100
        bonus_factor = min(0.2, len(bonus_skills) * 0.01)
        overall_score = min(1.0, base_score + bonus_factor)
        
        # Generate recommendation
        if overall_score >= 0.8:
            recommendation = "Excellent Match"
        elif overall_score >= 0.6:
            recommendation = "Good Match"
        elif overall_score >= 0.4:
            recommendation = "Fair Match"
        else:
            recommendation = "Poor Match"
        
        # Confidence based on skill overlap
        confidence = min(1.0, len(matched_skills) / max(5, len(job_skills)))
        
        return MatchResult(
            overall_score=round(overall_score * 100, 2),
            skill_match_percentage=round(skill_match_percentage, 2),
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            bonus_skills=bonus_skills,
            recommendation=recommendation,
            confidence=round(confidence, 2)
        )
