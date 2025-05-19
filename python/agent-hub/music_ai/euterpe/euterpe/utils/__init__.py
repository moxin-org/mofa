"""Utils package for the Euterpe library.

This package contains utility modules for common tasks.
"""

from .file_utils import (
    ensure_directory, 
    clean_directory, 
    list_files, 
    safe_filename, 
    get_temp_directory, 
    get_file_hash,
    save_json,
    load_json, 
    save_metadata,
    copy_file,
    get_unique_filename
)

__all__ = [
    "ensure_directory", 
    "clean_directory", 
    "list_files",
    "safe_filename",
    "get_temp_directory",
    "get_file_hash",
    "save_json",
    "load_json",
    "save_metadata",
    "copy_file",
    "get_unique_filename"
]
