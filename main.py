#!/usr/bin/env python3
"""
SkillFitAI - Professional Resume-Job Description Matching System
Main Entry Point with Clean Architecture Implementation

This is the main entry point for the SkillFitAI application.
Uses clean architecture principles with proper separation of concerns.
"""

import sys
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Optional
import json
import csv
from datetime import datetime

# Clean architecture imports
from src.core.matcher import ResumeJobMatcher
from src.core.document_processor import DocumentProcessor
from src.core.skill_extractor import SkillExtractor
from src.models.resume import Resume
from src.models.job_description import JobDescription
from src.utils.logger import get_logger, setup_logging
from src.utils.file_handler import FileHandler

class SkillFitAI:
    """Main SkillFitAI Application Class with Clean Architecture"""
    
    def __init__(self):
        """Initialize the SkillFitAI application with clean architecture components."""
        self.logger = None
        self.matcher = None
        self.processor = None
        self.file_handler = None
        self.setup_components()
        
    def setup_components(self):
        """Setup all application components using dependency injection."""
        # Setup logger
        logger_instance = setup_logging("SkillFitAI", "logs", "INFO")
        self.logger = logger_instance.get_logger()
        
        # Initialize core components
        self.processor = DocumentProcessor()
        self.skill_extractor = SkillExtractor()
        self.matcher = ResumeJobMatcher(self.logger)
        self.file_handler = FileHandler()
        
        self.logger.info("SkillFitAI components initialized successfully")
        
    def load_resumes(self, resume_path: str) -> List[Resume]:
        """Load all resumes from the specified path."""
        self.logger.info(f"Loading resumes from: {resume_path}")
        
        resumes = []
        supported_extensions = ['.pdf', '.docx', '.doc', '.txt', '.rtf']
        resume_files_info = self.file_handler.scan_directory(
            resume_path, 
            recursive=False,
            filter_formats=supported_extensions
        )
        resume_files = [info['path'] for info in resume_files_info]
        
        self.logger.info(f"Found {len(resume_files)} resume files")
        
        for i, file_path in enumerate(resume_files, 1):
            try:
                # Process document
                text = self.processor.read_document(file_path)
                if text:
                    # Extract skills
                    skills = self.skill_extractor.extract_skills(text)
                    
                    # Create Resume object
                    resume = Resume(
                        file_path=file_path,
                        raw_text=text
                    )
                    # Set the skills after creation
                    resume.all_skills = set(skill.skill for skill in skills if hasattr(skill, 'skill'))
                    
                    resumes.append(resume)
                    
                    if i % 5 == 0:  # Log progress every 5 files
                        self.logger.info(f"Processed {i}/{len(resume_files)} resumes")
                        
            except Exception as e:
                self.logger.error(f"Error processing resume {file_path}: {str(e)}")
                
        self.logger.info(f"Successfully loaded {len(resumes)} resumes")
        return resumes
        
    def load_job_descriptions(self, jd_path: str) -> List[JobDescription]:
        """Load all job descriptions from the specified path."""
        self.logger.info(f"Loading job descriptions from: {jd_path}")
        
        job_descriptions = []
        supported_extensions = ['.pdf', '.docx', '.doc', '.txt', '.rtf']
        jd_files_info = self.file_handler.scan_directory(
            jd_path,
            recursive=False,
            filter_formats=supported_extensions
        )
        jd_files = [info['path'] for info in jd_files_info]
        
        self.logger.info(f"Found {len(jd_files)} job description files")
        
        for i, file_path in enumerate(jd_files, 1):
            try:
                # Process document
                text = self.processor.read_document(file_path)
                if text:
                    # Extract skills
                    skills = self.skill_extractor.extract_skills(text)
                    
                    # Create JobDescription object
                    jd = JobDescription(
                        file_path=file_path,
                        raw_text=text
                    )
                    # Set the skills after creation
                    jd.all_skills = set(skill.skill for skill in skills if hasattr(skill, 'skill'))
                    
                    job_descriptions.append(jd)
                    
                    if i % 5 == 0:  # Log progress every 5 files
                        self.logger.info(f"Processed {i}/{len(jd_files)} job descriptions")
                        
            except Exception as e:
                self.logger.error(f"Error processing JD {file_path}: {str(e)}")
                
        self.logger.info(f"Successfully loaded {len(job_descriptions)} job descriptions")
        return job_descriptions
        
    def process_matches(self, resumes: List[Resume], job_descriptions: List[JobDescription]) -> List[Dict]:
        """Process all resume-job description matches."""
        self.logger.info("Starting matching process...")
        
        all_matches = []
        total_combinations = len(resumes) * len(job_descriptions)
        processed = 0
        
        for jd in job_descriptions:
            self.logger.info(f"Processing matches for JD: {jd.file_name}")
            
            for resume in resumes:
                try:
                    match_result_obj = self.matcher.match_resume_to_job(resume, jd)
                    
                    # Convert MatchResult object to dictionary
                    match_result = {
                        'overall_score': match_result_obj.overall_score,
                        'skill_match_score': match_result_obj.skill_match_percentage,
                        'text_similarity_score': 0.0,  # Not calculated by this method
                        'matched_skills': match_result_obj.matched_skills,
                        'missing_skills': match_result_obj.missing_skills,
                        'confidence': match_result_obj.confidence
                    }
                    
                    # Add metadata
                    match_result.update({
                        'resume_filename': resume.file_name,
                        'jd_filename': jd.file_name,
                        'resume_skills_count': len(resume.all_skills),
                        'jd_skills_count': len(jd.all_skills),
                        'processing_timestamp': datetime.now().isoformat()
                    })
                    
                    all_matches.append(match_result)
                    processed += 1
                    
                    if processed % 50 == 0:  # Log progress every 50 matches
                        progress = (processed / total_combinations) * 100
                        self.logger.info(f"Matching progress: {processed}/{total_combinations} ({progress:.1f}%)")
                        
                except Exception as e:
                    self.logger.error(f"Error matching {resume.filename} with {jd.filename}: {str(e)}")
                    
        self.logger.info(f"Completed matching: {len(all_matches)} total matches generated")
        return all_matches
        
    def save_results(self, matches: List[Dict], output_dir: str = "results") -> None:
        """Save results in multiple formats."""
        self.logger.info(f"Saving results to {output_dir}/")
        
        # Ensure output directory exists
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Save as JSON
        json_file = output_path / "main_matching_results.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(matches, f, indent=2, default=str)
        self.logger.info(f"Saved JSON results: {json_file}")
        
        # Save as CSV
        csv_file = output_path / "main_matching_results.csv"
        if matches:
            # Flatten nested data for CSV
            csv_data = []
            for match in matches:
                flat_match = {
                    'resume_filename': match.get('resume_filename', ''),
                    'jd_filename': match.get('jd_filename', ''),
                    'overall_score': match.get('overall_score', 0),
                    'skill_match_score': match.get('skill_match_score', 0),
                    'text_similarity_score': match.get('text_similarity_score', 0),
                    'matched_skills_count': len(match.get('matched_skills', [])),
                    'resume_skills_count': match.get('resume_skills_count', 0),
                    'jd_skills_count': match.get('jd_skills_count', 0),
                    'top_matched_skills': ', '.join(match.get('matched_skills', [])[:5])
                }
                csv_data.append(flat_match)
                
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                if csv_data:
                    writer = csv.DictWriter(f, fieldnames=csv_data[0].keys())
                    writer.writeheader()
                    writer.writerows(csv_data)
            self.logger.info(f"Saved CSV results: {csv_file}")
            
        # Generate summary report
        self.generate_summary_report(matches, output_path)
        
    def generate_summary_report(self, matches: List[Dict], output_path: Path) -> None:
        """Generate a comprehensive summary report."""
        if not matches:
            return
            
        report_file = output_path / "main_summary_report.txt"
        
        # Calculate statistics
        scores = [match.get('overall_score', 0) for match in matches]
        avg_score = sum(scores) / len(scores) if scores else 0
        max_score = max(scores) if scores else 0
        min_score = min(scores) if scores else 0
        
        # Get top matches
        top_matches = sorted(matches, key=lambda x: x.get('overall_score', 0), reverse=True)[:10]
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("SKILLFITAI MAIN.PY - COMPREHENSIVE MATCHING REPORT\n")
            f.write("=" * 60 + "\n\n")
            
            f.write("EXECUTIVE SUMMARY\n")
            f.write("-" * 30 + "\n")
            f.write(f"Total Matches Processed: {len(matches)}\n")
            f.write(f"Average Match Score: {avg_score:.2f}%\n")
            f.write(f"Highest Match Score: {max_score:.2f}%\n")
            f.write(f"Lowest Match Score: {min_score:.2f}%\n")
            f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("TOP 10 MATCHES\n")
            f.write("-" * 30 + "\n")
            for i, match in enumerate(top_matches, 1):
                f.write(f"{i:2d}. {match.get('resume_filename', 'Unknown')} ↔ {match.get('jd_filename', 'Unknown')}\n")
                f.write(f"    Overall Score: {match.get('overall_score', 0):.2f}%\n")
                f.write(f"    Skill Match: {match.get('skill_match_score', 0):.2f}%\n")
                f.write(f"    Text Similarity: {match.get('text_similarity_score', 0):.2f}%\n")
                f.write(f"    Matched Skills: {len(match.get('matched_skills', []))}\n")
                if match.get('matched_skills'):
                    f.write(f"    Top Skills: {', '.join(match.get('matched_skills', [])[:3])}\n")
                f.write("\n")
                
            # Score distribution
            f.write("SCORE DISTRIBUTION\n")
            f.write("-" * 30 + "\n")
            score_ranges = {
                "90-100%": len([s for s in scores if s >= 90]),
                "80-89%": len([s for s in scores if 80 <= s < 90]),
                "70-79%": len([s for s in scores if 70 <= s < 80]),
                "60-69%": len([s for s in scores if 60 <= s < 70]),
                "50-59%": len([s for s in scores if 50 <= s < 60]),
                "Below 50%": len([s for s in scores if s < 50])
            }
            
            for range_name, count in score_ranges.items():
                percentage = (count / len(scores)) * 100 if scores else 0
                f.write(f"{range_name}: {count} matches ({percentage:.1f}%)\n")
                
        self.logger.info(f"Generated summary report: {report_file}")
        
    def run(self, resume_path: str, jd_path: str, output_dir: str = "results") -> None:
        """Main execution method."""
        self.logger.info("Starting SkillFitAI main execution")
        
        try:
            # Load data
            resumes = self.load_resumes(resume_path)
            job_descriptions = self.load_job_descriptions(jd_path)
            
            if not resumes:
                self.logger.error("No resumes loaded. Please check the resume path.")
                return
                
            if not job_descriptions:
                self.logger.error("No job descriptions loaded. Please check the JD path.")
                return
                
            # Process matches
            matches = self.process_matches(resumes, job_descriptions)
            
            if not matches:
                self.logger.error("No matches generated.")
                return
                
            # Save results
            self.save_results(matches, output_dir)
            
            # Final summary
            avg_score = sum(match.get('overall_score', 0) for match in matches) / len(matches)
            best_match = max(matches, key=lambda x: x.get('overall_score', 0))
            
            self.logger.info("=" * 60)
            self.logger.info("EXECUTION COMPLETED SUCCESSFULLY")
            self.logger.info("=" * 60)
            self.logger.info(f"Resumes processed: {len(resumes)}")
            self.logger.info(f"Job descriptions processed: {len(job_descriptions)}")
            self.logger.info(f"Total matches generated: {len(matches)}")
            self.logger.info(f"Average match score: {avg_score:.2f}%")
            self.logger.info(f"Best match: {best_match.get('resume_filename')} ↔ {best_match.get('jd_filename')} ({best_match.get('overall_score', 0):.2f}%)")
            self.logger.info("=" * 60)
            
        except Exception as e:
            self.logger.error(f"Application error: {str(e)}")
            raise

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="SkillFitAI - Professional Resume-Job Description Matching System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --resumes data/Resume --jobs data/JD
  python main.py --resumes data/Resume --jobs data/JD --output custom_results
  python main.py --help
        """
    )
    
    parser.add_argument(
        "--resumes", "-r",
        required=True,
        help="Path to the directory containing resume files"
    )
    
    parser.add_argument(
        "--jobs", "-j", 
        required=True,
        help="Path to the directory containing job description files"
    )
    
    parser.add_argument(
        "--output", "-o",
        default="results",
        help="Output directory for results (default: results)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--version",
        action="version", 
        version="SkillFitAI v1.0.0"
    )
    
    return parser.parse_args()

def validate_paths(resume_path: str, jd_path: str) -> bool:
    """Validate that the provided paths exist and contain files."""
    resume_dir = Path(resume_path)
    jd_dir = Path(jd_path)
    
    if not resume_dir.exists():
        print(f"❌ Error: Resume directory '{resume_path}' does not exist")
        return False
        
    if not jd_dir.exists():
        print(f"❌ Error: Job description directory '{jd_path}' does not exist")
        return False
        
    # Check for supported file types
    supported_extensions = {'.pdf', '.docx', '.doc', '.txt', '.rtf'}
    
    resume_files = [f for f in resume_dir.iterdir() 
                   if f.is_file() and f.suffix.lower() in supported_extensions]
    
    jd_files = [f for f in jd_dir.iterdir() 
               if f.is_file() and f.suffix.lower() in supported_extensions]
    
    if not resume_files:
        print(f"❌ Error: No supported files found in resume directory '{resume_path}'")
        print(f"Supported formats: {', '.join(supported_extensions)}")
        return False
        
    if not jd_files:
        print(f"❌ Error: No supported files found in job description directory '{jd_path}'")
        print(f"Supported formats: {', '.join(supported_extensions)}")
        return False
        
    print(f"✅ Found {len(resume_files)} resume files and {len(jd_files)} job description files")
    return True

def main():
    """Main entry point for SkillFitAI application."""
    # Print banner
    print("=" * 60)
    print("🎯 SkillFitAI - Professional Resume Matching System")
    print("   Clean Architecture Implementation")
    print("=" * 60)
    
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Setup logging level based on verbose flag
        console_level = "DEBUG" if args.verbose else "INFO"
        
        # Validate input paths
        if not validate_paths(args.resumes, args.jobs):
            sys.exit(1)
            
        print(f"📋 Configuration:")
        print(f"   Resume Path: {args.resumes}")
        print(f"   Job Description Path: {args.jobs}")
        print(f"   Output Directory: {args.output}")
        print(f"   Verbose Logging: {args.verbose}")
        print()
        
        # Initialize and run the application
        app = SkillFitAI()
        app.run(
            resume_path=args.resumes,
            jd_path=args.jobs,
            output_dir=args.output
        )
        
        print("\n🎉 Application completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⚠️ Application interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Application failed with error: {str(e)}")
        if args.verbose if 'args' in locals() else False:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()