import os
from pathlib import Path
from typing import Optional, Tuple, Union
import shutil
import git
from git import Repo, GitCommandError, InvalidGitRepositoryError
from urllib.parse import urlparse


def get_repo_name_from_url(repo_url: str) -> str:
    """Extract repository name from GitHub URL"""
    parsed = urlparse(repo_url)
    path = parsed.path.strip('/')
    if path.endswith('.git'):
        path = path[:-4]
    return path.split('/')[-1]


def clone_github_repo(
    repo_url: str,
    base_dir: Union[str, Path],
    branch: Optional[str] = None,
    depth: Optional[int] = None,
    force_clean: bool = False
) -> Tuple[bool, str, Path]:
    """
    Clone a GitHub repository to a project-specific subdirectory.

    Args:
        repo_url: URL of the GitHub repository
        base_dir: Base directory where project subdir will be created
        branch: Specific branch to clone (optional)
        depth: Depth for shallow clone (optional)
        force_clean: If True, will clean existing git repository (default: False)

    Returns:
        Tuple of (success: bool, message: str, target_path: Path)
    """
    try:
        # Create project-specific directory
        repo_name = get_repo_name_from_url(repo_url)
        target_path = Path(base_dir) / repo_name
        target_path = target_path.absolute()

        # Handle existing directory (only clean if it's a git repo)
        if target_path.exists():
            try:
                existing_repo = Repo(target_path)
                if existing_repo.git_dir:
                    if not force_clean:
                        return False, f"Target directory {target_path} is already a Git repository", target_path
                    shutil.rmtree(target_path)
            except InvalidGitRepositoryError:
                pass  # Not a git repo - safe to proceed

        # Ensure parent directory exists
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # Prepare clone arguments
        clone_args = {}
        if branch:
            clone_args['branch'] = branch
        if depth:
            clone_args['depth'] = depth

        # Execute clone
        Repo.clone_from(
            url=repo_url,
            to_path=str(target_path),
            **clone_args
        )
        return True, f"Successfully cloned {repo_url} to {target_path}", target_path
    except GitCommandError as e:
        return False, f"Git operation failed: {str(e)}", target_path
    except Exception as e:
        return False, f"Unexpected error: {str(e)}", target_path


def validate_github_url(url: str) -> bool:
    """Validate GitHub URL format"""
    try:
        parsed = urlparse(url)
        return (
            (parsed.scheme in ('https', 'git') or url.startswith('git@')) and
            'github.com' in (parsed.netloc or url)
        )
    except:
        return False


def download_project(
    github_url: str,
    branch: Optional[str] = None,
    force_clean: bool = False,
    **clone_kwargs
) -> Tuple[bool, str, Path]:
    """
    Download GitHub project to a dedicated subdirectory.

    Args:
        github_url: GitHub repository URL
        branch: Specific branch to clone (overrides PROJECT_BRANCH)
        force_clean: Force clean existing git repo (default: False)
        **clone_kwargs: Additional clone parameters

    Returns:
        Tuple of (success: bool, message: str, target_path: Path)
    """
    if not validate_github_url(github_url):
        return False, "Invalid GitHub URL format", Path()

    # Get output path from environment (default to current directory)
    output_dir = os.getenv('PROJECT_OUTPUT_PATH', '.')

    # Get branch (parameter takes precedence, then environment, then default to 'main')
    branch = branch or os.getenv('PROJECT_BRANCH', 'main')

    return clone_github_repo(
        repo_url=github_url,
        base_dir=output_dir,
        branch=branch,
        force_clean=force_clean,
        **clone_kwargs
    )


if __name__ == "__main__":
    # Example usage:
    # Set environment variables first:
    # export PROJECT_OUTPUT_PATH=/path/to/output
    # export PROJECT_BRANCH=develop
    
    success, message, project_path = download_project(
        "https://github.com/Blaizzy/mlx-audio.git",
        force_clean=False
    )
    
    print(f"Download {'succeeded' if success else 'failed'}: {message}")
    if success:
        print(f"Project cloned to: {project_path}")