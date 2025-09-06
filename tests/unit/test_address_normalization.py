"""
Unit tests for address normalization functionality.
"""

import pytest
from tests.fixtures import NORMALIZATION_TEST_CASES, INVALID_ADDRESSES, SAMPLE_ADDRESSES


class TestAddressNormalization:
    """Test cases for address normalization."""
    
    def test_normalize_address_basic(self):
        """Test basic address normalization functionality."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        address = "123 Main St, New York, NY 10001"
        result = oxidize_postal.normalize_address(address)
        
        # Verify result is a string
        assert isinstance(result, str)
        assert len(result) > 0
        
        # Should contain key components
        result_lower = result.lower()
        assert "123" in result_lower
        assert "main" in result_lower
        assert "new york" in result_lower
        assert "ny" in result_lower
        assert "10001" in result_lower
    
    @pytest.mark.parametrize("test_case", NORMALIZATION_TEST_CASES)
    def test_normalize_address_expected_format(self, test_case):
        """Test normalization with expected formats."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        address = test_case["address"]
        expected_normalized = test_case["expected_normalized"]
        
        result = oxidize_postal.normalize_address(address)
        
        # Verify result is a string
        assert isinstance(result, str)
        assert len(result) > 0
        
        # Check that key components from expected format are present
        expected_components = expected_normalized.split(", ")
        result_lower = result.lower()
        
        matched_components = 0
        for component in expected_components:
            if component.lower() in result_lower:
                matched_components += 1
        
        # Should match at least 70% of expected components
        match_ratio = matched_components / len(expected_components)
        assert match_ratio >= 0.7, f"Only {matched_components}/{len(expected_components)} components found in normalized result"
    
    @pytest.mark.parametrize("test_case", SAMPLE_ADDRESSES)
    def test_normalize_address_samples(self, test_case):
        """Test normalization with various sample addresses."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        address = test_case["address"]
        expected_components = test_case["expected_components"]
        
        result = oxidize_postal.normalize_address(address)
        
        # Verify result is a string
        assert isinstance(result, str)
        assert len(result) > 0
        
        # Check that key expected components are present in normalized form
        result_lower = result.lower()
        found_components = 0
        
        for key, value in expected_components.items():
            if value.lower() in result_lower:
                found_components += 1
        
        # Should find at least half the expected components
        assert found_components >= len(expected_components) // 2
    
    @pytest.mark.parametrize("test_case", INVALID_ADDRESSES)
    def test_normalize_address_invalid(self, test_case):
        """Test normalization with invalid addresses."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        address = test_case["address"]
        expected_error = test_case["expected_error"]
        
        with pytest.raises(Exception) as exc_info:
            oxidize_postal.normalize_address(address)
        
        # Check that the error message contains expected text
        error_message = str(exc_info.value).lower()
        assert any(keyword in error_message for keyword in expected_error.lower().split())
    
    def test_normalize_address_consistency(self):
        """Test that normalization is consistent across calls."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        address = "123 Main St, New York, NY 10001"
        
        # Call normalization multiple times
        result1 = oxidize_postal.normalize_address(address)
        result2 = oxidize_postal.normalize_address(address)
        result3 = oxidize_postal.normalize_address(address)
        
        # Results should be identical
        assert result1 == result2 == result3
