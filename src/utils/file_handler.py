"""
File Handler Utility
===================

Robust file handling operations for the SkillFitAI system.
Supports multiple file formats and batch operations.
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict, Optional, Generator, Tuple
import json
import hashlib
from datetime import datetime


class FileHandler:
    """Advanced file handling with format detection and validation"""
    
    def __init__(self):
        self.supported_formats = {
            '.txt', '.rtf', '.pdf', '.docx', '.doc', 
            '.jpeg', '.jpg', '.png', '.json', '.csv'
        }
        
        self.format_descriptions = {
            '.txt': 'Plain Text',
            '.rtf': 'Rich Text Format',
            '.pdf': 'Portable Document Format',
            '.docx': 'Microsoft Word Document (Modern)',
            '.doc': 'Microsoft Word Document (Legacy)',
            '.jpeg': 'JPEG Image',
            '.jpg': 'JPEG Image',
            '.png': 'PNG Image',
            '.json': 'JSON Data',
            '.csv': 'Comma-Separated Values'
        }
    
    def scan_directory(self, directory_path: str, 
                      recursive: bool = False,
                      filter_formats: Optional[List[str]] = None) -> List[Dict[str, any]]:
        """Scan directory for supported files"""
        directory = Path(directory_path)
        
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        files_info = []
        
        # Choose scanning method
        if recursive:
            pattern = "**/*"
            file_iterator = directory.glob(pattern)
        else:
            file_iterator = directory.iterdir()
        
        for file_path in file_iterator:
            if file_path.is_file():
                file_info = self.get_file_info(file_path)
                
                # Apply format filter if specified
                if filter_formats:
                    if file_info['format'] not in filter_formats:
                        continue
                
                # Only include supported formats
                if file_info['format'] in self.supported_formats:
                    files_info.append(file_info)
        
        return sorted(files_info, key=lambda x: x['name'])
    
    def get_file_info(self, file_path: Path) -> Dict[str, any]:
        """Get comprehensive file information"""
        stat = file_path.stat()
        
        return {
            'name': file_path.name,
            'path': str(file_path.absolute()),
            'format': file_path.suffix.lower(),
            'format_description': self.format_descriptions.get(file_path.suffix.lower(), 'Unknown'),
            'size': stat.st_size,
            'size_mb': round(stat.st_size / (1024 * 1024), 2),
            'created': datetime.fromtimestamp(stat.st_ctime),
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'readable': os.access(file_path, os.R_OK),
            'writable': os.access(file_path, os.W_OK)
        }
    
    def batch_validate_files(self, file_paths: List[str]) -> Dict[str, Dict[str, any]]:
        """Validate multiple files in batch"""
        validation_results = {}
        
        for file_path in file_paths:
            path_obj = Path(file_path)
            
            validation = {
                'exists': path_obj.exists(),
                'readable': False,
                'valid_format': False,
                'size_ok': False,
                'errors': []
            }
            
            if validation['exists']:
                try:
                    # Check readability
                    validation['readable'] = os.access(path_obj, os.R_OK)
                    
                    # Check format
                    validation['valid_format'] = path_obj.suffix.lower() in self.supported_formats
                    
                    # Check size (not too small or too large)
                    size = path_obj.stat().st_size
                    validation['size_ok'] = 0 < size < 100 * 1024 * 1024  # 0 < size < 100MB
                    
                    if not validation['readable']:
                        validation['errors'].append('File is not readable')
                    if not validation['valid_format']:
                        validation['errors'].append(f'Unsupported format: {path_obj.suffix}')
                    if not validation['size_ok']:
                        validation['errors'].append(f'Invalid file size: {size} bytes')
                        
                except Exception as e:
                    validation['errors'].append(f'Validation error: {str(e)}')
            else:
                validation['errors'].append('File does not exist')
            
            validation_results[file_path] = validation
        
        return validation_results
    
    def organize_files_by_format(self, source_dir: str, target_dir: str, 
                                copy_files: bool = True) -> Dict[str, List[str]]:
        """Organize files into format-specific subdirectories"""
        source_path = Path(source_dir)
        target_path = Path(target_dir)
        
        if not source_path.exists():
            raise FileNotFoundError(f"Source directory not found: {source_dir}")
        
        # Create target directory
        target_path.mkdir(parents=True, exist_ok=True)
        
        organized_files = {}
        
        # Scan source directory
        files = self.scan_directory(source_dir)
        
        for file_info in files:
            format_name = file_info['format'][1:]  # Remove leading dot
            format_dir = target_path / format_name
            format_dir.mkdir(exist_ok=True)
            
            source_file = Path(file_info['path'])
            target_file = format_dir / source_file.name
            
            # Copy or move file
            if copy_files:
                shutil.copy2(source_file, target_file)
            else:
                shutil.move(source_file, target_file)
            
            # Track organized files
            if format_name not in organized_files:
                organized_files[format_name] = []
            organized_files[format_name].append(str(target_file))
        
        return organized_files
    
    def create_backup(self, source_path: str, backup_dir: str, 
                     include_timestamp: bool = True) -> str:
        """Create backup of files or directories"""
        source = Path(source_path)
        backup_path = Path(backup_dir)
        
        if not source.exists():
            raise FileNotFoundError(f"Source not found: {source_path}")
        
        # Create backup directory
        backup_path.mkdir(parents=True, exist_ok=True)
        
        # Generate backup name
        backup_name = source.name
        if include_timestamp:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{source.stem}_{timestamp}{source.suffix}"
        
        backup_target = backup_path / backup_name
        
        # Perform backup
        if source.is_file():
            shutil.copy2(source, backup_target)
        else:
            shutil.copytree(source, backup_target)
        
        return str(backup_target)
    
    def calculate_file_hash(self, file_path: str, algorithm: str = 'md5') -> str:
        """Calculate hash of file for integrity checking"""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Choose hash algorithm
        if algorithm.lower() == 'md5':
            hash_func = hashlib.md5()
        elif algorithm.lower() == 'sha1':
            hash_func = hashlib.sha1()
        elif algorithm.lower() == 'sha256':
            hash_func = hashlib.sha256()
        else:
            raise ValueError(f"Unsupported hash algorithm: {algorithm}")
        
        # Calculate hash
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        
        return hash_func.hexdigest()
    
    def find_duplicate_files(self, directory_path: str) -> Dict[str, List[str]]:
        """Find duplicate files based on content hash"""
        directory = Path(directory_path)
        
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        file_hashes = {}
        duplicates = {}
        
        # Calculate hashes for all files
        files = self.scan_directory(directory_path, recursive=True)
        
        for file_info in files:
            try:
                file_hash = self.calculate_file_hash(file_info['path'])
                
                if file_hash in file_hashes:
                    # Found duplicate
                    if file_hash not in duplicates:
                        duplicates[file_hash] = [file_hashes[file_hash]]
                    duplicates[file_hash].append(file_info['path'])
                else:
                    file_hashes[file_hash] = file_info['path']
                    
            except Exception as e:
                print(f"Error hashing {file_info['path']}: {e}")
        
        return duplicates
    
    def cleanup_empty_directories(self, root_path: str) -> List[str]:
        """Remove empty directories recursively"""
        root = Path(root_path)
        removed_dirs = []
        
        # Walk directories bottom-up
        for dirpath, dirnames, filenames in os.walk(root, topdown=False):
            current_dir = Path(dirpath)
            
            # Skip if not empty
            if filenames or dirnames:
                continue
            
            # Skip root directory
            if current_dir == root:
                continue
            
            try:
                current_dir.rmdir()
                removed_dirs.append(str(current_dir))
            except OSError as e:
                print(f"Could not remove {current_dir}: {e}")
        
        return removed_dirs
    
    def get_directory_stats(self, directory_path: str) -> Dict[str, any]:
        """Get comprehensive directory statistics"""
        directory = Path(directory_path)
        
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        files = self.scan_directory(directory_path, recursive=True)
        
        # Calculate statistics
        total_files = len(files)
        total_size = sum(f['size'] for f in files)
        
        # Format breakdown
        format_stats = {}
        for file_info in files:
            fmt = file_info['format']
            if fmt not in format_stats:
                format_stats[fmt] = {'count': 0, 'size': 0}
            format_stats[fmt]['count'] += 1
            format_stats[fmt]['size'] += file_info['size']
        
        # Size categories
        size_categories = {
            'small': 0,    # < 1MB
            'medium': 0,   # 1MB - 10MB
            'large': 0     # > 10MB
        }
        
        for file_info in files:
            size_mb = file_info['size_mb']
            if size_mb < 1:
                size_categories['small'] += 1
            elif size_mb <= 10:
                size_categories['medium'] += 1
            else:
                size_categories['large'] += 1
        
        return {
            'total_files': total_files,
            'total_size': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'format_breakdown': format_stats,
            'size_categories': size_categories,
            'avg_file_size': round(total_size / total_files, 2) if total_files > 0 else 0
        }