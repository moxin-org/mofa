from pathlib import Path
from typing import Dict, Optional, Union, Tuple, List
import codecs
import chardet
import warnings
from collections import defaultdict
from attrs import define, field

@define
class FileReader:
    """
    Enhanced FileReader with attrs decorator for multi-language file handling and directory tree scanning.
    """
    
    base_path: Path = field(converter=lambda x: Path(x).absolute())
    text_file_extensions: Dict[str, List[str]] = field(
        default={
            'code': ['.py', '.js', '.java', '.c', '.cpp', '.h', '.go', '.rs', '.ts', '.jl', '.rb'],
            'text': ['.txt', '.md', '.rst', '.log'],
            'data': ['.json', '.yaml', '.yml', '.xml', '.csv'],
            'config': ['.ini', '.cfg', '.conf', '.toml', '.env']
        },
        kw_only=True
    )
    binary_extensions: List[str] = field(
        default=[
            '.png', '.jpg', '.jpeg', '.gif', '.pdf', '.zip', '.exe',
            '.tar', '.gz', '.bz2', '.xz', '.rar', '.7z'
        ],
        kw_only=True
    )
    
    def detect_encoding(self, file_path: Path) -> str:
        """Detect file encoding with chardet, fallback to utf-8"""
        try:
            with open(file_path, 'rb') as f:
                return chardet.detect(f.read(4096))['encoding'] or 'utf-8'
        except Exception:
            return 'utf-8'
    
    def read_file(self, file_path: Union[str, Path]) -> Tuple[bool, Optional[Union[str, bytes]], Optional[str]]:
        """Read file content with encoding detection and fallback"""
        try:
            path = self.resolve_path(file_path)
            
            if not path.exists():
                return False, None, f"File not found: {path}"
            if path.is_dir():
                return False, None, f"Path is directory: {path}"
                
            ext = path.suffix.lower()
            
            if ext in self.binary_extensions:
                return False, None, f"Skipped binary file: {path}"
                
            try:
                encoding = self.detect_encoding(path)
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    with codecs.open(path, 'r', encoding=encoding, errors='replace') as f:
                        return True, f.read(), None
            except (UnicodeDecodeError, LookupError):
                with open(path, 'rb') as f:
                    return True, f.read(), None
                    
        except Exception as e:
            return False, None, f"Error reading {path}: {str(e)}"
    
    def resolve_path(self, file_path: Union[str, Path]) -> Path:
        """Resolve to absolute path relative to base_path"""
        path = Path(file_path)
        return self.base_path / path if not path.is_absolute() else path
    
    def get_file_type(self, file_path: Union[str, Path]) -> str:
        """Get file type category"""
        ext = Path(file_path).suffix.lower()
        for file_type, extensions in self.text_file_extensions.items():
            if ext in extensions:
                return file_type
        return 'unknown'
    
    def read_file_with_metadata(self, file_path: Union[str, Path]) -> Dict:
        """Read file with comprehensive metadata"""
        path = self.resolve_path(file_path)
        result = {
            'path': str(path),
            'type': self.get_file_type(path),
            'success': False,
            'content': None,
            'error': None,
            'encoding': None,
            'is_binary': False,
            'extension': path.suffix.lower()
        }
        
        if result['extension'] in self.binary_extensions:
            result['error'] = 'Skipped binary file'
            result['is_binary'] = True
            return result
            
        success, content, error = self.read_file(path)
        result.update({
            'success': success,
            'content': content,
            'error': error
        })
        
        if success:
            result['encoding'] = self.detect_encoding(path)
            result['is_binary'] = isinstance(content, bytes)
            
        return result
    
    def generate_file_tree(self,
                         root_path: Union[str, Path] = None,
                         max_depth: int = 5,
                         exclude_dirs: List[str] = None) -> Dict:
        """Generate nested file tree structure"""
        root_path = self.resolve_path(root_path) if root_path else self.base_path
        exclude_dirs = exclude_dirs or ['.git', '__pycache__', '.idea', 'node_modules']
        
        def build_tree(current_path: Path, depth: int) -> Optional[Dict]:
            if depth > max_depth or current_path.name in exclude_dirs:
                return None
                
            node = {
                'path': str(current_path),
                'type': 'directory' if current_path.is_dir() else 'file',
                'extension': current_path.suffix.lower() if current_path.is_file() else None
            }
            
            if current_path.is_dir():
                children = []
                for child in sorted(current_path.iterdir()):
                    if child_node := build_tree(child, depth + 1):
                        children.append(child_node)
                if children:
                    node['children'] = children
                    
            return node
            
        return build_tree(root_path, 0)
    
    def get_file_tree_flat(self,
                         root_path: Union[str, Path] = None,
                         exclude_dirs: List[str] = None) -> List[Dict]:
        """Get flattened list of all files with metadata"""
        tree = self.generate_file_tree(root_path, exclude_dirs=exclude_dirs)
        flat_list = []
        
        def flatten(node, depth=0):
            if not node:
                return
            if node['type'] == 'file':
                flat_list.append({
                    'path': node['path'],
                    'type': 'file',
                    'extension': node['extension'],
                    'depth': depth
                })
            elif 'children' in node:
                for child in node['children']:
                    flatten(child, depth + 1)
                    
        flatten(tree)
        return flat_list


# Example usage
if __name__ == "__main__":
    # Initialize with attrs
    reader = FileReader(base_path='/Users/chenzi/chenzi/project/zcbc/mofa/python/examples/deep-wiki/mofasearch')
    
    # Get file tree
    tree = reader.generate_file_tree(max_depth=5)
    print("File Tree Structure:", tree)
    
    file_data = reader.read_file('/Users/chenzi/chenzi/project/zcbc/mofa/python/examples/deep-wiki/mofasearch/README.md')
    print(file_data)

    
