"""
Unit tests for data management functionality.
"""

import pytest
from pathlib import Path


class TestDataManagement:
    """Test cases for data download and management."""
    
    def test_download_data_function_exists(self):
        """Test that download_data function exists and is callable."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        # Check that function exists
        assert hasattr(oxidize_postal, 'download_data')
        assert callable(oxidize_postal.download_data)
    
    def test_download_data_parameters(self):
        """Test download_data function with different parameters."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        # Test with default parameters (should not raise exception)
        try:
            # Note: This might fail if libpostal_data binary is not available
            # but it should at least accept the parameters
            result = oxidize_postal.download_data(False)
            assert isinstance(result, bool)
        except Exception as e:
            # Expected if libpostal_data binary is not found
            error_msg = str(e).lower()
            assert any(keyword in error_msg for keyword in ['libpostal_data', 'binary', 'tool', 'command'])
    


