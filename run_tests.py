#!/usr/bin/env python3
"""
Test runner for oxidize-postal.

This script helps run different types of tests and provides clear output.
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}")
    print(f"Running: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"\n✅ {description} - PASSED")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} - FAILED (exit code {e.returncode})")
        return False
    except FileNotFoundError:
        print(f"\n❌ {description} - FAILED (command not found)")
        return False


def check_package_installed():
    """Check if the package is properly installed."""
    try:
        import oxidize_postal
        print("✅ Package import successful")
        return True
    except ImportError as e:
        print(f"❌ Package import failed: {e}")
        print("💡 Run './build.sh' to build and install the package")
        return False


def check_data_available():
    """Check if libpostal data is available."""
    try:
        import oxidize_postal
        result = oxidize_postal.parse_address("123 Main St")
        if result:
            print("✅ Libpostal data is available and working")
            return True
        else:
            print("❌ Libpostal data appears to be missing")
            return False
    except Exception as e:
        error_msg = str(e).lower()
        if "libpostal data" in error_msg or "could not find" in error_msg:
            print(f"❌ Libpostal data not available: {e}")
            print("💡 Run 'python -c \"import oxidize_postal; oxidize_postal.download_data()\"'")
            return False
        else:
            print(f"❌ Unexpected error: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description="Run tests for oxidize-postal")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--check", action="store_true", help="Check setup without running tests")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Default to all tests if no specific type specified
    if not (args.unit or args.integration or args.check):
        args.all = True
    
    print("🧪 oxidize-postal Test Runner")
    print("=" * 60)
    
    # Check package installation
    print("\n📦 Checking package installation...")
    if not check_package_installed():
        print("\n❌ Package not properly installed. Please run './build.sh' first.")
        return 1
    
    # Check data availability for integration tests
    data_available = False
    if args.integration or args.all:
        print("\n📊 Checking libpostal data availability...")
        data_available = check_data_available()
        if not data_available:
            print("\n⚠️  Libpostal data not available. Integration tests will be skipped.")
    
    if args.check:
        print("\n✅ Setup check complete!")
        return 0
    
    # Build pytest command
    pytest_args = ["python", "-m", "pytest"]
    
    if args.verbose:
        pytest_args.append("-v")
    else:
        pytest_args.append("-q")
    
    # Add test discovery and reporting
    pytest_args.extend(["--tb=short", "--no-header"])
    
    success = True
    
    # Run unit tests
    if args.unit or args.all:
        unit_cmd = pytest_args + ["tests/unit/"]
        if not run_command(unit_cmd, "Unit Tests"):
            success = False
    
    # Run integration tests
    if args.integration or args.all:
        if data_available:
            integration_cmd = pytest_args + ["tests/integration/"]
            if not run_command(integration_cmd, "Integration Tests"):
                success = False
        else:
            print(f"\n{'='*60}")
            print("⏭️  Skipping Integration Tests - Data Not Available")
            print(f"{'='*60}")
            print("💡 To run integration tests:")
            print("   1. Download libpostal data: python -c \"import oxidize_postal; oxidize_postal.download_data()\"")
            print("   2. Run tests again: python run_tests.py --integration")
    
    # Summary
    print(f"\n{'='*60}")
    if success:
        print("🎉 All tests completed successfully!")
        print(f"{'='*60}")
        return 0
    else:
        print("💥 Some tests failed!")
        print(f"{'='*60}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
