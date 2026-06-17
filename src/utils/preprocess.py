import re
from typing import Dict, List

def clean_text(text: str) -> str:
    """
    Enhanced preprocessing for resumes and job descriptions.
    - Lowercase
    - Remove special characters
    - Remove extra spaces
    - Handle redacted content properly
    """
    if not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Replace redacted content (asterisks) with placeholder
    text = re.sub(r'\*{3,}', ' [redacted] ', text)
    
    # Remove special characters but keep alphanumeric and spaces
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    
    # Remove extra spaces and normalize
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def advanced_redaction(text: str, custom_patterns: Dict[str, str] = None) -> str:
    """
    Advanced redaction function with customizable patterns
    
    Args:
        text: Input text to redact
        custom_patterns: Dictionary of pattern names and regex patterns
    
    Returns:
        Redacted text
    """
    if not isinstance(text, str):
        return ""
    
    # Default sensitive patterns
    default_patterns = {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'phone': r'(\+?\d{1,4}[-.\s]?)?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
        'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
        'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
        'ip_address': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
        'url': r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        'date': r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
        'postal_code': r'\b\d{5}(-\d{4})?\b',
    }
    
    # Merge custom patterns if provided
    patterns = default_patterns.copy()
    if custom_patterns:
        patterns.update(custom_patterns)
    
    redacted_text = text
    
    # Apply each pattern
    for pattern_name, pattern in patterns.items():
        redacted_text = re.sub(pattern, lambda m: '*' * len(m.group()), redacted_text, flags=re.IGNORECASE)
    
    return redacted_text

def extract_skills(text: str, skill_keywords: List[str] = None) -> List[str]:
    """
    Extract skills from text based on keyword matching
    
    Args:
        text: Input text
        skill_keywords: List of skill keywords to search for
    
    Returns:
        List of found skills
    """
    if not isinstance(text, str):
        return []
    
    # Default skill keywords (can be expanded)
    default_skills = [
        'python', 'java', 'javascript', 'react', 'angular', 'vue', 'nodejs', 'express',
        'django', 'flask', 'fastapi', 'sql', 'mysql', 'postgresql', 'mongodb', 'redis',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'github',
        'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn',
        'data science', 'pandas', 'numpy', 'matplotlib', 'seaborn', 'tableau',
        'html', 'css', 'bootstrap', 'sass', 'less', 'webpack', 'babel',
        'restful', 'api', 'microservices', 'agile', 'scrum', 'devops', 'ci/cd',
        'linux', 'windows', 'macos', 'bash', 'powershell', 'vim', 'vscode'
    ]
    
    skills = skill_keywords if skill_keywords else default_skills
    found_skills = []
    
    text_lower = text.lower()
    
    for skill in skills:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    
    return list(set(found_skills))  # Remove duplicates

def preprocess_for_matching(text: str, redact_sensitive: bool = True, extract_skills_flag: bool = False) -> Dict:
    """
    Complete preprocessing pipeline for resume/JD matching
    
    Args:
        text: Input text
        redact_sensitive: Whether to redact sensitive information
        extract_skills_flag: Whether to extract skills
    
    Returns:
        Dictionary with processed text and metadata
    """
    if not isinstance(text, str):
        return {"cleaned_text": "", "skills": [], "word_count": 0}
    
    # Step 1: Redact sensitive information if requested
    processed_text = advanced_redaction(text) if redact_sensitive else text
    
    # Step 2: Clean text for matching
    cleaned_text = clean_text(processed_text)
    
    # Step 3: Extract skills if requested
    skills = extract_skills(cleaned_text) if extract_skills_flag else []
    
    # Step 4: Get word count
    word_count = len(cleaned_text.split())
    
    return {
        "original_text": text,
        "redacted_text": processed_text,
        "cleaned_text": cleaned_text,
        "skills": skills,
        "word_count": word_count,
        "has_content": bool(cleaned_text.strip())
    }
