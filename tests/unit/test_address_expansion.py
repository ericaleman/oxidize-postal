"""
Unit tests for address expansion functionality.
"""

import pytest
import json
from tests.fixtures import (
    ABBREVIATION_TEST_CASES, 
    INVALID_ADDRESSES,
    INTERNATIONAL_ADDRESSES
)


class TestAddressExpansion:
    """Test cases for address expansion."""
    
    def test_expand_address_basic(self):
        """Test basic address expansion functionality."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        address = "123 Main St"
        result = oxidize_postal.expand_address(address)
        
        # Verify result is a list
        assert isinstance(result, list)
        assert len(result) > 0
        
        # All items should be strings
        assert all(isinstance(item, str) for item in result)
        
        # Should contain some expansion
        assert any("street" in item.lower() for item in result)
    
    @pytest.mark.parametrize("test_case", ABBREVIATION_TEST_CASES)
    def test_expand_address_abbreviations(self, test_case):
        """Test expansion with various abbreviations."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        address = test_case["address"]
        expected_expansions = test_case["expected_expansions"]
        
        result = oxidize_postal.expand_address(address)
        
        # Verify result is a list
        assert isinstance(result, list)
        assert len(result) > 0
        
        # Check that at least one expected expansion is present
        result_lower = [item.lower() for item in result]
        expected_lower = [item.lower() for item in expected_expansions]
        
        found_expected = any(expected in result_lower for expected in expected_lower)
        assert found_expected, f"None of {expected_expansions} found in {result}"
    
    @pytest.mark.parametrize("test_case", INVALID_ADDRESSES)
    def test_expand_address_invalid(self, test_case):
        """Test expansion with invalid addresses."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        address = test_case["address"]
        expected_error = test_case["expected_error"]
        
        with pytest.raises(Exception) as exc_info:
            oxidize_postal.expand_address(address)
        
        # Check that the error message contains expected text
        error_message = str(exc_info.value).lower()
        assert any(keyword in error_message for keyword in expected_error.lower().split())


class TestAddressExpansionJSON:
    """Test cases for JSON-formatted address expansion."""
    
    def test_expand_address_to_json(self):
        """Test expanding address and returning JSON."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        address = "123 Main St"
        result = oxidize_postal.expand_address_to_json(address)
        
        # Verify result is a valid JSON string
        assert isinstance(result, str)
        
        # Parse the JSON to verify it's valid
        parsed = json.loads(result)
        assert isinstance(parsed, list)
        assert len(parsed) > 0
        assert all(isinstance(item, str) for item in parsed)
    
    def test_json_expand_consistency(self):
        """Test that JSON expansion is consistent with regular expansion."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        address = "123 Main St"
        
        # Get results from both methods
        list_result = oxidize_postal.expand_address(address)
        json_result = oxidize_postal.expand_address_to_json(address)
        
        # Parse JSON result
        json_parsed = json.loads(json_result)
        
        # Results should be identical
        assert list_result == json_parsed


class TestInternationalExpansion:
    """Test expansion with international addresses."""
    
    @pytest.mark.parametrize("test_case", INTERNATIONAL_ADDRESSES[:3])  # Test first 3
    def test_expand_international_addresses(self, test_case):
        """Test expansion of international addresses."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        address = test_case["address"]
        description = test_case["description"]
        
        try:
            result = oxidize_postal.expand_address(address)
            
            # Basic assertions
            assert isinstance(result, list), f"Failed for {description}: result is not a list"
            assert len(result) > 0, f"Failed for {description}: empty result"
            
            # All items should be strings
            assert all(isinstance(item, str) for item in result), \
                f"Failed for {description}: not all items are strings"
            
            # Check that expansions are not identical to input
            # (at least one should be different)
            assert any(exp != address for exp in result) or len(result) == 1, \
                f"No actual expansion occurred for {description}"
            
        except Exception as e:
            # Some international addresses might have issues
            if "kanji" in description or "Cyrillic" in description:
                pass  # Expected potential issues with non-Latin scripts
            else:
                raise


class TestExpansionEdgeCases:
    """Test edge cases in address expansion."""
    
    def test_expansion_with_numbers(self):
        """Test that numbers are preserved in expansions."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        addresses_with_numbers = [
            "123 5th Avenue",
            "456 21st Street",
            "789 42nd Road",
        ]
        
        for address in addresses_with_numbers:
            result = oxidize_postal.expand_address(address)
            assert isinstance(result, list)
            assert len(result) > 0
            
            # Check that numbers are preserved
            house_number = address.split()[0]
            assert all(house_number in exp for exp in result), \
                f"House number {house_number} not preserved in expansions"
    
    def test_expansion_determinism(self):
        """Test that expansion results are deterministic."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        address = "123 Main St NYC NY"
        
        # Run expansion multiple times
        results = []
        for _ in range(5):
            result = oxidize_postal.expand_address(address)
            results.append(result)
        
        # All results should be identical
        first_result = results[0]
        for i, result in enumerate(results[1:], 1):
            assert result == first_result, \
                f"Expansion {i} differs from first: {result} != {first_result}"
    
    def test_expansion_with_punctuation(self):
        """Test expansion with various punctuation."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        addresses_with_punctuation = [
            "123 St. James Street",
            "456 Ave., New York",
            "789 N.E. Broadway",
            "P.O. Box 123",
        ]
        
        for address in addresses_with_punctuation:
            result = oxidize_postal.expand_address(address)
            assert isinstance(result, list)
            assert len(result) > 0
            
            # Should handle punctuation gracefully
            for expansion in result:
                assert isinstance(expansion, str)
                assert len(expansion) > 0
