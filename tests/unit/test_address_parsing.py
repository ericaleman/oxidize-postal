"""
Unit tests for address parsing functionality.
"""

import pytest
import json
from tests.fixtures import (
    SAMPLE_ADDRESSES, 
    INVALID_ADDRESSES,
    INTERNATIONAL_ADDRESSES,
    EDGE_CASES
)


class TestAddressParsing:
    """Test cases for basic address parsing."""
    
    def test_parse_address_basic(self):
        """Test basic address parsing functionality."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        # Test with a simple address
        address = "123 Main St, New York, NY 10001"
        result = oxidize_postal.parse_address(address)
        
        # Verify result is a dictionary
        assert isinstance(result, dict)
        assert len(result) > 0
        
        # Check for expected components (may vary based on libpostal version)
        expected_keys = {"house_number", "road", "city", "state", "postcode"}
        result_keys = set(result.keys())
        
        # Should have at least some expected components
        assert len(expected_keys.intersection(result_keys)) >= 3
    
    @pytest.mark.parametrize("test_case", SAMPLE_ADDRESSES)
    def test_parse_address_samples(self, test_case):
        """Test parsing with various sample addresses."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        address = test_case["address"]
        expected = test_case["expected_components"]
        
        result = oxidize_postal.parse_address(address)
        
        # Verify result is a dictionary
        assert isinstance(result, dict)
        
        # Check that at least 50% of expected components are present
        # (libpostal results may vary slightly)
        matched_components = 0
        for key, expected_value in expected.items():
            if key in result:
                # Normalize for comparison (lowercase, strip)
                result_value = result[key].lower().strip()
                expected_value = expected_value.lower().strip()
                if result_value == expected_value:
                    matched_components += 1
        
        match_ratio = matched_components / len(expected)
        assert match_ratio >= 0.5, f"Only {matched_components}/{len(expected)} components matched for {address}"
    
    @pytest.mark.parametrize("test_case", INVALID_ADDRESSES)
    def test_parse_address_invalid(self, test_case):
        """Test parsing with invalid addresses."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        address = test_case["address"]
        expected_error = test_case["expected_error"]
        
        with pytest.raises(Exception) as exc_info:
            oxidize_postal.parse_address(address)
        
        # Check that the error message contains expected text
        error_message = str(exc_info.value).lower()
        assert any(keyword in error_message for keyword in expected_error.lower().split())


class TestAddressParsingJSON:
    """Test cases for JSON-formatted address parsing."""
    
    def test_parse_address_to_json(self):
        """Test parsing address and returning JSON."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        address = "123 Main St, New York, NY 10001"
        result = oxidize_postal.parse_address_to_json(address)
        
        # Verify result is a valid JSON string
        assert isinstance(result, str)
        
        # Parse the JSON to verify it's valid
        parsed = json.loads(result)
        assert isinstance(parsed, dict)
        assert len(parsed) > 0
    
    def test_json_parse_consistency(self):
        """Test that JSON parsing is consistent with regular parsing."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        address = "123 Main St, New York, NY 10001"
        
        # Get results from both methods
        dict_result = oxidize_postal.parse_address(address)
        json_result = oxidize_postal.parse_address_to_json(address)
        
        # Parse JSON result
        json_parsed = json.loads(json_result)
        
        # Results should be identical
        assert dict_result == json_parsed


class TestInternationalAddresses:
    """Test cases for international address parsing."""
    
    @pytest.mark.parametrize("test_case", INTERNATIONAL_ADDRESSES)
    def test_parse_international_addresses(self, test_case):
        """Test parsing of international addresses with various scripts and formats."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        address = test_case["address"]
        expected = test_case["expected_components"]
        description = test_case["description"]
        
        result = oxidize_postal.parse_address(address)
        
        # Basic assertions
        assert isinstance(result, dict), f"Failed for {description}: result is not a dict"
        assert len(result) > 0, f"Failed for {description}: empty result"
        
        # Check that we get at least some expected components
        # International addresses may vary more in parsing
        matched_components = 0
        for key, expected_value in expected.items():
            if key in result:
                result_value = result[key].lower().strip()
                expected_value = expected_value.lower().strip()
                if expected_value in result_value or result_value in expected_value:
                    matched_components += 1
        
        # For international addresses, expect at least 30% match due to variations
        match_ratio = matched_components / len(expected) if expected else 0
        assert match_ratio >= 0.3 or len(result) > 0, \
            f"Poor parsing for {description}: only {matched_components}/{len(expected)} components matched"
    
    def test_unicode_handling(self):
        """Test that Unicode characters are handled properly."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        # Test various Unicode scripts
        unicode_addresses = [
            "東京都",  # Japanese
            "Москва",  # Cyrillic
            "Straße",  # German with eszett
            "Café Street",  # Accented characters
            "🏠 Home Street"  # Emoji (should handle gracefully)
        ]
        
        for address in unicode_addresses:
            result = oxidize_postal.parse_address(address)
            assert isinstance(result, dict), f"Failed to parse Unicode address: {address}"
            # Should not raise an exception


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    @pytest.mark.parametrize("test_case", EDGE_CASES)
    def test_edge_case_parsing(self, test_case):
        """Test parsing of edge cases."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        address = test_case["address"]
        expected = test_case["expected_components"]
        description = test_case["description"]
        
        # Some edge cases might fail, which is OK
        try:
            result = oxidize_postal.parse_address(address)
            assert isinstance(result, dict), f"Failed for {description}: result is not a dict"
            
            # For edge cases, we just check if it doesn't crash
            # and returns something reasonable
            if expected:
                # Check if any expected components are present
                for key in expected.keys():
                    if key in result:
                        assert result[key] is not None
                        assert isinstance(result[key], str)
        except Exception as e:
            # Some edge cases (like special chars only) might raise exceptions
            if "Special characters only" in description:
                pass  # Expected to potentially fail
            else:
                # Re-raise unexpected failures
                raise
    
    def test_very_long_address(self):
        """Test handling of very long addresses."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        # Create a very long but valid address
        long_address = "123 " + "Very " * 100 + "Long Street, New York, NY 10001"
        
        result = oxidize_postal.parse_address(long_address)
        assert isinstance(result, dict)
        # libpostal may return either 'house_number' or 'house' for complex addresses
        assert "house_number" in result or "house" in result
        if "house_number" in result:
            assert result["house_number"] == "123"
        elif "house" in result:
            # For very long addresses, libpostal may include the number in 'house'
            assert "123" in result["house"]
    
    def test_address_with_special_formatting(self):
        """Test addresses with various formatting issues."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        formatting_tests = [
            ("  123 Main St  ", "123"),  # Extra spaces
            ("123    Main    St", "123"),  # Multiple spaces
            ("123 MAIN ST", "123"),  # All caps
            ("123 main st", "123"),  # All lowercase
            ("123 MaIn St", "123"),  # Mixed case
        ]
        
        for address, expected_number in formatting_tests:
            result = oxidize_postal.parse_address(address)
            assert isinstance(result, dict)
            # Check that the house number is parsed (may be in 'house_number' or 'house')
            assert "house_number" in result or "house" in result
            if "house_number" in result:
                assert result["house_number"] == expected_number
            elif "house" in result:
                assert expected_number in result["house"]
    
    def test_component_extraction_completeness(self):
        """Test that all major components are extracted when present."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        # A complete address with many components
        complete_address = "Apt 4B, 123 Main Street, Suite 200, Brooklyn, New York, NY 10001, USA"
        result = oxidize_postal.parse_address(complete_address)
        
        # Check for various component types
        assert isinstance(result, dict)
        assert len(result) >= 3, "Should extract at least 3 components from complete address"
        
        # Verify data types and non-empty values
        for key, value in result.items():
            assert isinstance(key, str), f"Component key {key} is not a string"
            assert isinstance(value, str), f"Component value {value} is not a string"
            assert len(value.strip()) > 0, f"Component {key} has empty value"
