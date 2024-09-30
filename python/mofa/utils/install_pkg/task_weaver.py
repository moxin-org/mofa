import os
import sys
import subprocess
import importlib.util
import urllib.request
import zipfile
import shutil
from typing import Optional


def is_package_installed(package_name: str) -> bool:
    """
    Check if the specified Python package is installed.

    Args:
        package_name (str): The name of the package to check.

    Returns:
        bool: True if the package is installed, False otherwise.
    """
    spec = importlib.util.find_spec(package_name)
    return spec is not None


def create_temp_directory(temp_dir: str) -> None:
    """
    Create a temporary directory if it does not exist.

    Args:
        temp_dir (str): The path of the temporary directory.

    Raises:
        SystemExit: If the directory cannot be created.
    """
    if not os.path.exists(temp_dir):
        try:
            os.makedirs(temp_dir)
            print(f"Created directory: {temp_dir}")
        except Exception as e:
            print(f"Failed to create directory {temp_dir}: {e}")
            sys.exit(1)
    else:
        print(f"Directory already exists: {temp_dir}")


def download_taskweaver(repo_url: str, download_path: str) -> str:
    """
    Download the TaskWeaver ZIP file from the GitHub repository.

    Args:
        repo_url (str): The URL of the GitHub repository.
        download_path (str): The target directory to download the file.

    Returns:
        str: The full path to the downloaded ZIP file.

    Raises:
        SystemExit: If the download fails.
    """
    zip_url = f"{repo_url}/archive/refs/heads/main.zip"
    zip_file_path = os.path.join(download_path, "taskweaver-main.zip")

    try:
        print(f"Downloading TaskWeaver from {zip_url} to {zip_file_path}...")
        urllib.request.urlretrieve(zip_url, zip_file_path)
        print("Download completed.")
    except Exception as e:
        print(f"Download failed: {e}")
        sys.exit(1)

    return zip_file_path


def extract_zip(zip_file_path: str, extract_to: str) -> None:
    """
    Extract the downloaded ZIP file to the specified directory.

    Args:
        zip_file_path (str): The path to the ZIP file.
        extract_to (str): The directory to extract the contents to.

    Raises:
        SystemExit: If extraction fails or the file is not a valid ZIP file.
    """
    try:
        print(f"Extracting {zip_file_path} to {extract_to}...")
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print("Extraction completed.")
    except zipfile.BadZipFile:
        print("The downloaded file is not a valid ZIP file.")
        sys.exit(1)
    except Exception as e:
        print(f"Extraction failed: {e}")
        sys.exit(1)


def install_package(package_dir: str) -> None:
    """
    Install the Python package from the specified directory using pip.

    Args:
        package_dir (str): The directory path of the package.

    Raises:
        SystemExit: If the installation fails.
    """
    try:
        print(f"Installing package from: {package_dir}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_dir])
        print("Installation completed.")
    except subprocess.CalledProcessError as e:
        print(f"Installation failed: {e}")
        sys.exit(1)


def clean_up(zip_file_path: str, extract_dir: str) -> None:
    """
    Clean up by removing the downloaded ZIP file and the extracted directory.

    Args:
        zip_file_path (str): The path to the ZIP file.
        extract_dir (str): The path to the extracted directory.

    Raises:
        SystemExit: If the cleanup fails.
    """
    try:
        if os.path.exists(zip_file_path):
            os.remove(zip_file_path)
            print(f"Deleted file: {zip_file_path}")

        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)
            print(f"Deleted directory: {extract_dir}")
    except Exception as e:
        print(f"Cleanup failed: {e}")


def download_and_install_taskweaver(package_name: str = "taskweaver",repo_url: str = "https://github.com/microsoft/taskweaver",temp_dir: str = "/tmp/python/") -> None:
    """
    Main function to execute the package check, download, and installation process.
    """
    # package_name: str = "taskweaver"
    # repo_url: str = "https://github.com/microsoft/taskweaver"
    # current_dir: str = os.getcwd()
    # temp_dir: str = os.path.join(current_dir, "temp")

    # Check if the package is already installed
    if is_package_installed(package_name):
        print(f"Package '{package_name}' is already installed.")
    else:
        print(f"Package '{package_name}' is not installed. Preparing to download and install.")

    # Create temporary directory
    create_temp_directory(temp_dir)

    # Download TaskWeaver
    zip_file_path: str = download_taskweaver(repo_url, temp_dir)

    # Extract ZIP file
    extract_dir: str = os.path.join(temp_dir, "taskweaver-main")
    extract_zip(zip_file_path, temp_dir)

    # Install the package
    install_package(extract_dir)

    # Optional: Clean up downloaded files and extracted directories
    # clean_up(zip_file_path, extract_dir)

    # Final check to confirm installation
    if is_package_installed(package_name):
        print(f"Package '{package_name}' has been successfully installed.")
    else:
        print(f"Package '{package_name}' installation failed.")
        sys.exit(1)


if __name__ == "__main__":
    download_and_install_taskweaver(temp_dir='/Users/chenzi/project/zcbc')
