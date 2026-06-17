"""
Data Models Module
==================

Data structures and models for representing resumes,
job descriptions, and matching results.
"""

from .resume import Resume
from .job_description import JobDescription

__all__ = [
    'Resume',
    'JobDescription'
]