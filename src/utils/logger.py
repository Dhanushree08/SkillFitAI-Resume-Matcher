"""
Logger Configuration
===================

Comprehensive logging setup for the SkillFitAI system.
Provides structured logging with multiple outputs and log levels.
"""

import logging
import logging.handlers
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import json


class SkillFitLogger:
    """Advanced logging system with multiple handlers and formats"""
    
    def __init__(self, name: str = "SkillFitAI", log_dir: str = "logs"):
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create main logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup different logging handlers"""
        
        # Console Handler - INFO and above
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File Handler - All levels
        log_file = self.log_dir / f"{self.name.lower()}.log"
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Error Handler - ERROR and above only
        error_file = self.log_dir / f"{self.name.lower()}_errors.log"
        error_handler = logging.handlers.RotatingFileHandler(
            error_file,
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        self.logger.addHandler(error_handler)
        
        # JSON Handler for structured logging
        json_file = self.log_dir / f"{self.name.lower()}_structured.log"
        json_handler = logging.handlers.RotatingFileHandler(
            json_file,
            maxBytes=20*1024*1024,  # 20MB
            backupCount=3
        )
        json_handler.setLevel(logging.INFO)
        json_handler.setFormatter(StructuredFormatter())
        self.logger.addHandler(json_handler)
    
    def get_logger(self) -> logging.Logger:
        """Get the configured logger instance"""
        return self.logger
    
    def log_performance(self, operation: str, duration: float, 
                       details: Optional[Dict[str, Any]] = None):
        """Log performance metrics"""
        perf_data = {
            'operation': operation,
            'duration_seconds': round(duration, 3),
            'timestamp': datetime.now().isoformat()
        }
        
        if details:
            perf_data.update(details)
        
        self.logger.info(f"PERFORMANCE: {operation} completed in {duration:.3f}s", 
                        extra={'performance_data': perf_data})
    
    def log_file_operation(self, operation: str, file_path: str, 
                          success: bool = True, error: Optional[str] = None):
        """Log file operations"""
        file_data = {
            'operation': operation,
            'file_path': file_path,
            'success': success,
            'timestamp': datetime.now().isoformat()
        }
        
        if error:
            file_data['error'] = error
        
        level = logging.INFO if success else logging.ERROR
        message = f"FILE_OP: {operation} {'succeeded' if success else 'failed'} for {file_path}"
        
        if error:
            message += f" - {error}"
        
        self.logger.log(level, message, extra={'file_operation': file_data})
    
    def log_matching_result(self, resume_file: str, job_file: str, 
                           match_score: float, skills_matched: int,
                           total_skills: int):
        """Log skill matching results"""
        match_data = {
            'resume_file': resume_file,
            'job_file': job_file,
            'match_score': round(match_score, 2),
            'skills_matched': skills_matched,
            'total_skills': total_skills,
            'match_percentage': round((skills_matched / total_skills * 100), 2) if total_skills > 0 else 0,
            'timestamp': datetime.now().isoformat()
        }
        
        self.logger.info(f"MATCH: {Path(resume_file).name} vs {Path(job_file).name} - Score: {match_score:.2f}",
                        extra={'matching_result': match_data})
    
    def log_processing_stats(self, processed_files: int, successful_files: int,
                           failed_files: int, total_duration: float):
        """Log batch processing statistics"""
        stats_data = {
            'processed_files': processed_files,
            'successful_files': successful_files,
            'failed_files': failed_files,
            'success_rate': round((successful_files / processed_files * 100), 2) if processed_files > 0 else 0,
            'total_duration': round(total_duration, 3),
            'avg_time_per_file': round(total_duration / processed_files, 3) if processed_files > 0 else 0,
            'timestamp': datetime.now().isoformat()
        }
        
        self.logger.info(f"BATCH_STATS: Processed {processed_files} files, "
                        f"{successful_files} successful, {failed_files} failed",
                        extra={'processing_stats': stats_data})
    
    def log_system_info(self):
        """Log system information at startup"""
        import platform
        
        system_info = {
            'python_version': sys.version,
            'platform': platform.platform(),
            'architecture': platform.architecture(),
            'processor': platform.processor(),
            'working_directory': os.getcwd(),
            'log_directory': str(self.log_dir.absolute()),
            'timestamp': datetime.now().isoformat()
        }
        
        self.logger.info("SYSTEM_INFO: Application started", 
                        extra={'system_info': system_info})


class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured JSON logging"""
    
    def format(self, record):
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'message': record.getMessage()
        }
        
        # Add any extra structured data
        if hasattr(record, 'performance_data'):
            log_entry['performance_data'] = record.performance_data
        
        if hasattr(record, 'file_operation'):
            log_entry['file_operation'] = record.file_operation
        
        if hasattr(record, 'matching_result'):
            log_entry['matching_result'] = record.matching_result
        
        if hasattr(record, 'processing_stats'):
            log_entry['processing_stats'] = record.processing_stats
        
        if hasattr(record, 'system_info'):
            log_entry['system_info'] = record.system_info
        
        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry)


class TimerContext:
    """Context manager for timing operations"""
    
    def __init__(self, logger: SkillFitLogger, operation: str, 
                 details: Optional[Dict[str, Any]] = None):
        self.logger = logger
        self.operation = operation
        self.details = details or {}
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        self.logger.get_logger().debug(f"Starting {self.operation}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration = (datetime.now() - self.start_time).total_seconds()
            
            if exc_type is None:
                self.logger.log_performance(self.operation, duration, self.details)
            else:
                self.details['error'] = str(exc_val) if exc_val else "Unknown error"
                self.logger.get_logger().error(f"Operation {self.operation} failed after {duration:.3f}s",
                                             extra={'performance_data': {
                                                 'operation': self.operation,
                                                 'duration_seconds': duration,
                                                 'success': False,
                                                 'error': self.details['error']
                                             }})


# Global logger instance
_global_logger = None

def get_logger(name: str = "SkillFitAI", log_dir: str = "logs") -> SkillFitLogger:
    """Get or create global logger instance"""
    global _global_logger
    
    if _global_logger is None or _global_logger.name != name:
        _global_logger = SkillFitLogger(name, log_dir)
        _global_logger.log_system_info()
    
    return _global_logger

def setup_logging(name: str = "SkillFitAI", log_dir: str = "logs", 
                 console_level: str = "INFO") -> SkillFitLogger:
    """Setup logging with custom configuration"""
    logger = SkillFitLogger(name, log_dir)
    
    # Adjust console logging level if requested
    if console_level.upper() in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        for handler in logger.logger.handlers:
            if isinstance(handler, logging.StreamHandler) and handler.stream == sys.stdout:
                handler.setLevel(getattr(logging, console_level.upper()))
                break
    
    return logger

def log_function_call(logger: Optional[SkillFitLogger] = None):
    """Decorator to log function calls"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if logger is None:
                current_logger = get_logger()
            else:
                current_logger = logger
            
            func_name = func.__name__
            current_logger.get_logger().debug(f"Calling function: {func_name}")
            
            try:
                with TimerContext(current_logger, f"function_{func_name}"):
                    result = func(*args, **kwargs)
                return result
            except Exception as e:
                current_logger.get_logger().error(f"Function {func_name} failed: {str(e)}", 
                                                 exc_info=True)
                raise
        
        return wrapper
    return decorator


# Example usage and testing
if __name__ == "__main__":
    # Test the logging system
    logger = setup_logging("TestLogger", "test_logs")
    
    # Test different log levels
    logger.get_logger().debug("This is a debug message")
    logger.get_logger().info("This is an info message")
    logger.get_logger().warning("This is a warning message")
    logger.get_logger().error("This is an error message")
    
    # Test structured logging
    logger.log_performance("test_operation", 1.234, {"files_processed": 10})
    logger.log_file_operation("read", "/path/to/file.txt", True)
    logger.log_matching_result("resume1.pdf", "job1.txt", 85.5, 17, 20)
    logger.log_processing_stats(100, 95, 5, 45.67)
    
    # Test timer context
    with TimerContext(logger, "test_timer", {"test_param": "value"}):
        import time
        time.sleep(0.1)
    
    print("Logging test completed. Check the test_logs directory for output files.")