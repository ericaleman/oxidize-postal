#!/usr/bin/env python3
"""
Data manager for oxidize-postal package.
Downloads libpostal data files to the standard system location.
"""

import os
import sys
import subprocess
from pathlib import Path


def get_default_data_directories():
    """Get the default libpostal data directories that libpostal checks."""
    return [
        Path("/usr/local/share/libpostal"),
        Path("/usr/share/libpostal")
    ]


def get_libpostal_data_tool():
    """Find the libpostal_data binary built by the package."""
    # Look for the built libpostal_data tool
    try:
        import oxidize_postal
        package_dir = Path(oxidize_postal.__file__).parent
    except ImportError:
        # If package not installed, look relative to current directory
        package_dir = Path(__file__).parent
    
    # Common locations where the binary might be
    search_paths = [
        # In the current working directory build (most common during development)
        "oxidize-postal/target/release/build/libpostal-sys-*/out/bin/libpostal_data",
        # System-wide installation
        "/usr/local/bin/libpostal_data",
        "/usr/bin/libpostal_data",
    ]
    
    for path_pattern in search_paths:
        if "*" in path_pattern:
            # Handle glob pattern - use the shell to find it
            import glob
            matches = glob.glob(path_pattern)
            for match in matches:
                path_obj = Path(match)
                if path_obj.exists() and path_obj.is_file():
                    return path_obj
        else:
            path_obj = Path(path_pattern)
            if path_obj.exists() and path_obj.is_file():
                return path_obj
    
    return None


def check_data():
    """Check if libpostal data is available and appears valid."""
    # Check both standard locations
    data_dirs = get_default_data_directories()
    
    for data_dir in data_dirs:
        if not data_dir.exists():
            continue
        
        # Check for essential data files
        required_files = [
            "address_expansions/address_dictionary.dat",
            "address_parser/address_parser_crf.dat",
            "transliteration/transliteration.dat"
        ]
        
        all_files_exist = True
        for file_path in required_files:
            full_path = data_dir / file_path
            if not full_path.exists():
                all_files_exist = False
                break
        
        if all_files_exist:
            return True
    
    return False


def download_data(force=False):
    """
    Download libpostal data files to the standard system location.
    
    Args:
        force (bool): Force re-download even if data exists
    
    Returns:
        bool: True if successful, False otherwise
    """
    print("🌍 Setting up libpostal data")
    
    # Use standard libpostal location
    data_dir = Path("/usr/local/share/libpostal")
    
    if not force and check_data():
        print("✅ Libpostal data already exists and appears valid")
        return True
    
    # Find libpostal_data tool
    libpostal_tool = get_libpostal_data_tool()
    if not libpostal_tool:
        print("❌ Could not find libpostal_data tool.")
        print("Make sure the package is properly installed and built.")
        return False
    
    try:
        print("📥 Downloading libpostal data...")
        print(f"📁 Data will be stored in: {data_dir}")
        
        # Run libpostal_data download (may need sudo for system directory)
        # Need to specify data type - using 'all' to download all required data
        cmd = [str(libpostal_tool), "download", "all", str(data_dir)]
        
        # Try without sudo first
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            # If failed due to permissions, try with sudo
            if "Permission denied" in result.stderr:
                print("🔐 Need administrator privileges for system directory...")
                cmd = ["sudo"] + cmd
                result = subprocess.run(cmd, capture_output=False, text=True)
        
        if result.returncode != 0:
            print(f"❌ Download failed: {result.stderr}")
            return False
        
        print("✅ Data download completed.")
        return True
        
    except Exception as e:
        print(f"❌ Error during download: {e}")
        return False


def remove_data():
    """Remove libpostal data files."""
    data_dirs = get_default_data_directories()
    
    for data_dir in data_dirs:
        if data_dir.exists():
            try:
                print(f"🗑️  Removing data from {data_dir}")
                subprocess.run(["sudo", "rm", "-rf", str(data_dir)], check=True)
                print("✅ Data removed successfully")
                return True
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to remove data: {e}")
    
    print("ℹ️  No data found to remove")
    return True


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage libpostal data for oxidize-postal")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Download command
    download_parser = subparsers.add_parser("download", help="Download libpostal data")
    download_parser.add_argument("--force", action="store_true", 
                               help="Force re-download even if data exists")
    
    # Check command
    subparsers.add_parser("check", help="Check if data is available")
    
    # Remove command
    subparsers.add_parser("remove", help="Remove libpostal data")
    
    args = parser.parse_args()
    
    if args.command == "download":
        success = download_data(args.force)
        sys.exit(0 if success else 1)
    elif args.command == "check":
        if check_data():
            print("✅ Libpostal data is available and valid")
            sys.exit(0)
        else:
            print("❌ Libpostal data is not available")
            sys.exit(1)
    elif args.command == "remove":
        success = remove_data()
        sys.exit(0 if success else 1)
    else:
        parser.print_help()
        sys.exit(1)