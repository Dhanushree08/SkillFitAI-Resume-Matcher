"""
Text Processing Utilities
========================

Advanced text processing for document analysis and skill extraction.
Includes cleaning, normalization, and linguistic processing functions.
"""

import re
import string
from typing import List, Dict, Set, Optional, Tuple
from collections import Counter
import unicodedata


class TextProcessor:
    """Advanced text processing and cleaning utilities"""
    
    def __init__(self):
        # Common stop words
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 
            'for', 'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through',
            'during', 'before', 'after', 'above', 'below', 'between', 'among',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her',
            'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their',
            'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'can', 'shall'
        }
        
        # Technical abbreviations that should be preserved
        self.tech_abbreviations = {
            'ai', 'ml', 'api', 'ui', 'ux', 'sql', 'html', 'css', 'js',
            'json', 'xml', 'rest', 'http', 'https', 'tcp', 'ip', 'dns',
            'aws', 'gcp', 'azure', 'devops', 'cicd', 'git', 'svn',
            'ide', 'sdk', 'cli', 'gui', 'erp', 'crm', 'seo', 'sas',
            'etl', 'bi', 'iot', 'ar', 'vr', 'nlp', 'cv', 'dl', 'nn'
        }
        
        # Pattern for extracting technical skills
        self.skill_patterns = [
            r'\b(?:python|java|javascript|c\+\+|c#|php|ruby|go|rust|kotlin|swift)\b',
            r'\b(?:react|angular|vue|node\.?js|express|django|flask|spring)\b',
            r'\b(?:mysql|postgresql|mongodb|redis|elasticsearch|oracle)\b',
            r'\b(?:docker|kubernetes|jenkins|git|aws|azure|gcp)\b',
            r'\b(?:machine learning|deep learning|artificial intelligence|data science)\b',
        ]
        
        # Email and phone patterns for redaction
        self.sensitive_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}',
            'ssn': r'\b(?:\d{3}-?\d{2}-?\d{4})\b',
            'url': r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
        }
    
    def clean_text(self, text: str, level: str = 'standard') -> str:
        """Clean text with different intensity levels"""
        if not text or not isinstance(text, str):
            return ""
        
        # Basic cleaning (always applied)
        cleaned = text.strip()
        
        if level == 'minimal':
            # Only basic whitespace normalization
            cleaned = re.sub(r'\s+', ' ', cleaned)
            return cleaned
        
        elif level == 'standard':
            # Standard cleaning for general processing
            # Normalize unicode
            cleaned = unicodedata.normalize('NFKD', cleaned)
            
            # Remove excessive whitespace
            cleaned = re.sub(r'\s+', ' ', cleaned)
            
            # Remove special characters but keep basic punctuation
            cleaned = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)]', ' ', cleaned)
            
            # Clean up multiple punctuation
            cleaned = re.sub(r'[.]{2,}', '.', cleaned)
            cleaned = re.sub(r'[,]{2,}', ',', cleaned)
            
        elif level == 'aggressive':
            # Aggressive cleaning for keyword extraction
            # Normalize unicode
            cleaned = unicodedata.normalize('NFKD', cleaned)
            
            # Convert to lowercase
            cleaned = cleaned.lower()
            
            # Remove all punctuation except hyphens in words
            cleaned = re.sub(r'[^\w\s\-]', ' ', cleaned)
            
            # Keep hyphens only within words
            cleaned = re.sub(r'\s+-+\s+', ' ', cleaned)
            cleaned = re.sub(r'^-+\s+', '', cleaned)
            cleaned = re.sub(r'\s+-+$', '', cleaned)
            
            # Remove excessive whitespace
            cleaned = re.sub(r'\s+', ' ', cleaned)
            
        return cleaned.strip()
    
    def extract_sentences(self, text: str) -> List[str]:
        """Extract sentences from text"""
        if not text:
            return []
        
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        
        # Clean and filter sentences
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:  # Minimum sentence length
                cleaned_sentences.append(sentence)
        
        return cleaned_sentences
    
    def extract_keywords(self, text: str, min_length: int = 2, 
                        max_keywords: int = 50) -> List[Tuple[str, int]]:
        """Extract keywords with frequency counts"""
        if not text:
            return []
        
        # Clean text aggressively for keyword extraction
        cleaned = self.clean_text(text, level='aggressive')
        
        # Split into words
        words = cleaned.split()
        
        # Filter words
        filtered_words = []
        for word in words:
            # Skip if too short
            if len(word) < min_length:
                continue
                
            # Skip stop words (unless it's a technical abbreviation)
            if word.lower() in self.stop_words and word.lower() not in self.tech_abbreviations:
                continue
                
            # Skip if all digits
            if word.isdigit():
                continue
                
            filtered_words.append(word.lower())
        
        # Count frequencies
        word_counts = Counter(filtered_words)
        
        # Return top keywords
        return word_counts.most_common(max_keywords)
    
    def extract_technical_terms(self, text: str) -> List[str]:
        """Extract technical terms and skills from text"""
        if not text:
            return []
        
        technical_terms = set()
        text_lower = text.lower()
        
        # Apply skill extraction patterns
        for pattern in self.skill_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            technical_terms.update(matches)
        
        # Look for common technical patterns
        # Programming languages, frameworks, tools, etc.
        tech_patterns = [
            # Languages
            r'\b(?:python|java|javascript|typescript|c\+\+|c#|php|ruby|go|rust|kotlin|swift|scala|r|matlab)\b',
            # Web frameworks
            r'\b(?:react|angular|vue|svelte|next\.js|nuxt\.js|gatsby|ember)\b',
            # Backend frameworks
            r'\b(?:django|flask|fastapi|express|nest\.js|spring|laravel|rails|asp\.net)\b',
            # Databases
            r'\b(?:mysql|postgresql|sqlite|mongodb|redis|elasticsearch|cassandra|dynamodb)\b',
            # Cloud platforms
            r'\b(?:aws|azure|gcp|google cloud|amazon web services|microsoft azure)\b',
            # DevOps tools
            r'\b(?:docker|kubernetes|jenkins|gitlab|github|terraform|ansible|puppet)\b',
            # Data science
            r'\b(?:pandas|numpy|scikit-learn|tensorflow|pytorch|keras|spark|hadoop)\b',
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            technical_terms.update(matches)
        
        return sorted(list(technical_terms))
    
    def redact_sensitive_info(self, text: str, redaction_char: str = '*') -> str:
        """Remove or redact sensitive information"""
        if not text:
            return ""
        
        redacted_text = text
        
        for info_type, pattern in self.sensitive_patterns.items():
            if info_type == 'email':
                # Keep domain but redact username
                def redact_email(match):
                    email = match.group(0)
                    username, domain = email.split('@')
                    redacted_username = username[0] + redaction_char * (len(username) - 1)
                    return f"{redacted_username}@{domain}"
                
                redacted_text = re.sub(pattern, redact_email, redacted_text)
                
            elif info_type == 'phone':
                # Keep area code but redact rest
                def redact_phone(match):
                    phone = match.group(0)
                    # Extract digits
                    digits = re.sub(r'\D', '', phone)
                    if len(digits) >= 10:
                        area_code = digits[:3]
                        redacted = area_code + '-' + redaction_char * 3 + '-' + redaction_char * 4
                        return redacted
                    return redaction_char * len(phone)
                
                redacted_text = re.sub(pattern, redact_phone, redacted_text)
                
            else:
                # Complete redaction for other sensitive info
                redacted_text = re.sub(pattern, redaction_char * 8, redacted_text)
        
        return redacted_text
    
    def normalize_whitespace(self, text: str) -> str:
        """Normalize all whitespace in text"""
        if not text:
            return ""
        
        # Replace all whitespace variants with single spaces
        normalized = re.sub(r'\s+', ' ', text)
        return normalized.strip()
    
    def extract_contact_info(self, text: str) -> Dict[str, List[str]]:
        """Extract contact information (for processing, not storage)"""
        if not text:
            return {}
        
        contact_info = {
            'emails': [],
            'phones': [],
            'urls': []
        }
        
        # Extract emails
        emails = re.findall(self.sensitive_patterns['email'], text, re.IGNORECASE)
        contact_info['emails'] = list(set(emails))
        
        # Extract phone numbers
        phones = re.findall(self.sensitive_patterns['phone'], text)
        contact_info['phones'] = list(set(phones))
        
        # Extract URLs
        urls = re.findall(self.sensitive_patterns['url'], text, re.IGNORECASE)
        contact_info['urls'] = list(set(urls))
        
        return contact_info
    
    def calculate_text_metrics(self, text: str) -> Dict[str, any]:
        """Calculate comprehensive text metrics"""
        if not text:
            return {}
        
        # Basic counts
        char_count = len(text)
        char_count_no_spaces = len(text.replace(' ', ''))
        word_count = len(text.split())
        sentence_count = len(self.extract_sentences(text))
        
        # Paragraph count (simple approximation)
        paragraph_count = len([p for p in text.split('\n\n') if p.strip()])
        
        # Calculate averages
        avg_word_length = char_count_no_spaces / word_count if word_count > 0 else 0
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        
        # Technical content analysis
        technical_terms = self.extract_technical_terms(text)
        keywords = self.extract_keywords(text, max_keywords=20)
        
        # Readability approximation (simplified)
        readability_score = 0
        if sentence_count > 0 and word_count > 0:
            # Simple approximation of readability
            readability_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * (avg_word_length / 4.7))
        
        return {
            'character_count': char_count,
            'character_count_no_spaces': char_count_no_spaces,
            'word_count': word_count,
            'sentence_count': sentence_count,
            'paragraph_count': paragraph_count,
            'average_word_length': round(avg_word_length, 2),
            'average_sentence_length': round(avg_sentence_length, 2),
            'technical_terms_count': len(technical_terms),
            'top_keywords_count': len(keywords),
            'readability_score': round(readability_score, 2),
            'technical_density': round((len(technical_terms) / word_count * 100), 2) if word_count > 0 else 0
        }
    
    def split_into_chunks(self, text: str, chunk_size: int = 1000, 
                         overlap: int = 100) -> List[str]:
        """Split text into overlapping chunks for processing"""
        if not text or chunk_size <= 0:
            return []
        
        chunks = []
        words = text.split()
        
        if len(words) <= chunk_size:
            return [text]
        
        start = 0
        while start < len(words):
            end = min(start + chunk_size, len(words))
            chunk = ' '.join(words[start:end])
            chunks.append(chunk)
            
            if end >= len(words):
                break
                
            start = end - overlap
        
        return chunks
    
    def find_similar_phrases(self, text: str, min_length: int = 3) -> List[Tuple[str, int]]:
        """Find repeated phrases in text"""
        if not text:
            return []
        
        # Clean text
        cleaned = self.clean_text(text, level='standard')
        words = cleaned.lower().split()
        
        phrase_counts = Counter()
        
        # Generate n-grams from min_length to reasonable maximum
        max_length = min(10, len(words) // 2)
        
        for n in range(min_length, max_length + 1):
            for i in range(len(words) - n + 1):
                phrase = ' '.join(words[i:i+n])
                phrase_counts[phrase] += 1
        
        # Filter to only phrases that appear more than once
        repeated_phrases = [(phrase, count) for phrase, count in phrase_counts.items() if count > 1]
        
        # Sort by frequency
        return sorted(repeated_phrases, key=lambda x: x[1], reverse=True)[:20]