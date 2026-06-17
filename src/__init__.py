"""
SkillFitAI - Professional Resume-Job Matching System
====================================================

A sophisticated AI-powered system for matching resumes with job descriptions
across multiple document formats with professional content generation capabilities.

Author: SkillFitAI Development Team
Version: 2.0.0
License: MIT
"""

__version__ = "2.0.0"
__author__ = "SkillFitAI Development Team"

# Import main classes for easy access
from .core.matcher import SkillMatcher, ResumeJobMatcher
from .generators.dataset_generator import DatasetGenerator
from .models.resume import Resume
from .models.job_description import JobDescription

__all__ = [
    'SkillMatcher',
    'ResumeJobMatcher', 
    'DatasetGenerator',
    'Resume',
    'JobDescription'
]