import os
import re
from datetime import datetime

# Get the current year
current_year = datetime.now().year

# Define the license claim template with placeholders for different comment styles
license_claim_template = {
    'block': f"""/*
Copyright (C) {current_year} The XLang Foundation

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/""",
    'hash': f"""#
# Copyright (C) {current_year} The XLang Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# <END>""",
    'xml': f"""<!--
Copyright (C) {current_year} The XLang Foundation

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->"""
}

# Define file extensions and their corresponding comment styles
extensions_with_comment_styles = {
    '.c': 'block', '.cpp': 'block', '.cc': 'block', '.cxx': 'block',
    '.h': 'block', '.hpp': 'block', '.hxx': 'block', '.inl': 'block',
    '.java': 'block',
    '.js': 'block', '.jsx': 'block', '.ts': 'block', '.tsx': 'block',
    '.py': 'hash', '.pyx': 'hash', '.pxd': 'hash',
    '.x': 'hash',
    '.yaml': 'hash', '.yml': 'hash',
    '.json': 'hash',  # JSON files typically use '//' but we're using '#' for consistency
    '.xml': 'xml', '.html': 'xml', '.htm': 'xml',
    '.cmake': 'hash',  # CMake files treated as regular hash-style files now
    '.cs': 'block'  # C# files
}

# Define files and directories to be excluded
exclude_list = [
    '\\ThirdParty',
    '\\Tools\\file_scan_add_lic.py',
]

# Normalize paths in the exclude list to ensure cross-platform compatibility
exclude_list = [os.path.normpath(exclude) for exclude in exclude_list]

def is_excluded(path, exclude_list):
    """Check if a given path should be excluded based on the exclude_list."""
    norm_path = os.path.normpath(path)
    for exclude in exclude_list:
        if exclude in norm_path:
            return True
    return False

def remove_existing_license(content, comment_style):
    """Remove existing license block if found at the top of the file."""
    # Define the patterns for removing the license based on the comment style
    license_patterns = {
        'block': re.compile(
            r"/\*.*?Copyright \(C\) \d{4} The XLang Foundation.*?\*/", re.DOTALL
        ),
        'hash': re.compile(
            r"^#.*?Copyright \(C\) \d{4} The XLang Foundation.*?<END>", re.MULTILINE | re.DOTALL
        ),
        'xml': re.compile(
            r"<!--.*?Copyright \(C\) \d{4} The XLang Foundation.*?-->", re.DOTALL
        ),
    }

    pattern = license_patterns.get(comment_style)
    if pattern:
        content = re.sub(pattern, '', content).lstrip()
    return content

def add_license_to_file(filepath, comment_style):
    """Add license claim to the top of the file based on its comment style."""
    license_claim = license_claim_template[comment_style]

    # Open the file with utf-8 encoding, which does not introduce a BOM
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    # Remove BOM if it exists
    if content.startswith('\ufeff'):
        content = content[1:]

    # Remove existing license block if present in the top lines
    content = remove_existing_license(content, comment_style)

    # Write the new license and content with a space line between the claim and content
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(license_claim + '\n\n' + content)
    
    # Print out the file being processed
    print(f"License updated in {filepath}")

def scan_and_add_license(directory):
    """Recursively scan the directory and add or update the license claim in matching files."""
    for root, dirs, files in os.walk(directory):
        # Normalize root path to ensure compatibility
        norm_root = os.path.normpath(root)

        # Exclude specified folders
        dirs[:] = [d for d in dirs if not is_excluded(os.path.join(norm_root, d), exclude_list)]

        for file in files:
            filepath = os.path.join(norm_root, file)

            if is_excluded(filepath, exclude_list):
                continue  # Skip excluded files

            # Determine the comment style based on the file extension or specific file name
            ext = os.path.splitext(file)[1]
            comment_style = extensions_with_comment_styles.get(ext, None)

            if comment_style:
                add_license_to_file(filepath, comment_style)

if __name__ == "__main__":
    # Define the directory to be scanned
    directory_to_scan = "D:\\source\\xMind"
    directory_to_scan = os.path.normpath(directory_to_scan)

    scan_and_add_license(directory_to_scan)
