"""File utilities for the Euterpe library.

This module provides utility functions for file operations.
"""

import hashlib
import json
import logging
import os
import re
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any, Union, BinaryIO

# Set up logger
logger = logging.getLogger(__name__)


def ensure_directory(directory: Path) -> Path:
    """Ensure that a directory exists, creating it if necessary.
    
    Args:
        directory: The directory path to ensure exists.
        
    Returns:
        Path: The directory path.
    """
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def clean_directory(directory: Path, keep_dir: bool = True) -> None:
    """Clean a directory by removing all its contents.
    
    Args:
        directory: The directory path to clean.
        keep_dir: Whether to keep the directory itself. 
            If False, removes the directory too.
    """
    if not directory.exists():
        return
        
    for item in directory.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()
            
    if not keep_dir:
        directory.rmdir()


def list_files(directory: Path, pattern: str = "*", recursive: bool = False) -> List[Path]:
    """List files in a directory matching a pattern.
    
    Args:
        directory: The directory path to search.
        pattern: A glob pattern to match filenames.
        recursive: Whether to search recursively in subdirectories.
        
    Returns:
        List[Path]: List of matching file paths.
    """
    if recursive:
        return list(directory.glob(f"**/{pattern}"))
    return list(directory.glob(pattern))


def safe_filename(text: str, max_length: int = 100) -> str:
    """Generate a safe filename from text, removing invalid characters.
    
    Args:
        text: Text to convert to a safe filename.
        max_length: Maximum length for the filename.
        
    Returns:
        str: Safe filename.
    """
    # Remove invalid filename characters
    text = re.sub(r'[\\/*?:"<>|]', "", text)
    # Replace spaces and other separators with underscores
    text = re.sub(r'[\s\t\n\r\f\v\-]+', "_", text)
    # Limit length
    if len(text) > max_length:
        text = text[:max_length]
    # Remove leading/trailing underscores
    text = text.strip("_")
    # Ensure we have a valid filename
    if not text:
        text = "unnamed"
    return text


def get_temp_directory(prefix: str = "euterpe_") -> Path:
    """Get a temporary directory.
    
    Args:
        prefix: Prefix for the temporary directory name.
        
    Returns:
        Path: Path to the temporary directory.
    """
    temp_dir = Path(tempfile.mkdtemp(prefix=prefix))
    return temp_dir


def get_file_hash(file_path: Path, algorithm: str = "md5") -> str:
    """Calculate a hash of a file.
    
    Args:
        file_path: Path to the file.
        algorithm: Hash algorithm to use (md5, sha1, sha256).
        
    Returns:
        str: Hexadecimal hash digest.
        
    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
        
    hash_func = getattr(hashlib, algorithm)()
    
    with open(file_path, "rb") as f:
        # Read in chunks to handle large files
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
            
    return hash_func.hexdigest()


def save_json(data: Dict[str, Any], file_path: Path) -> None:
    """Save data as a JSON file.
    
    Args:
        data: Data to save.
        file_path: Path to the output JSON file.
    """
    ensure_directory(file_path.parent)
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    logger.debug(f"Saved JSON data to {file_path}")


def load_json(file_path: Path) -> Dict[str, Any]:
    """Load data from a JSON file.
    
    Args:
        file_path: Path to the JSON file.
        
    Returns:
        Dict[str, Any]: Loaded data.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"JSON file not found: {file_path}")
        
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    return data


def save_metadata(data: Dict[str, Any], directory: Path, filename: str = "metadata.json") -> Path:
    """Save metadata for a generation run.
    
    Args:
        data: Metadata to save.
        directory: Directory to save the metadata file in.
        filename: Name of the metadata file.
        
    Returns:
        Path: Path to the saved metadata file.
    """
    # Add timestamp if not present
    if "timestamp" not in data:
        data["timestamp"] = datetime.now().isoformat()
        
    file_path = directory / filename
    save_json(data, file_path)
    
    return file_path


def copy_file(src: Path, dst: Path, overwrite: bool = False) -> Path:
    """Copy a file from source to destination.
    
    Args:
        src: Source file path.
        dst: Destination file path.
        overwrite: Whether to overwrite existing files.
        
    Returns:
        Path: Path to the copied file.
        
    Raises:
        FileNotFoundError: If the source file does not exist.
        FileExistsError: If the destination file exists and overwrite is False.
    """
    if not src.exists():
        raise FileNotFoundError(f"Source file not found: {src}")
        
    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination file exists: {dst}")
        
    ensure_directory(dst.parent)
    
    return Path(shutil.copy2(src, dst))
    
    
def get_unique_filename(directory: Path, base_name: str, extension: str) -> Path:
    """Get a unique filename in a directory.
    
    Args:
        directory: Directory path.
        base_name: Base name for the file.
        extension: File extension (without the dot).
        
    Returns:
        Path: Unique file path.
    """
    # Ensure extension doesn't have a leading dot
    extension = extension.lstrip(".")
    
    # Try the base name first
    file_path = directory / f"{base_name}.{extension}"
    if not file_path.exists():
        return file_path
        
    # Add a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = directory / f"{base_name}_{timestamp}.{extension}"
    
    # If still exists (unlikely), add a counter
    counter = 1
    while file_path.exists():
        file_path = directory / f"{base_name}_{timestamp}_{counter}.{extension}"
        counter += 1
        
    return file_path
