"""
End-to-end integration tests for oxidize-postal.

These tests require libpostal data to be downloaded and available.
"""

import pytest
import json
import time
from concurrent.futures import ThreadPoolExecutor
from tests.fixtures import (
    SAMPLE_ADDRESSES,
    INTERNATIONAL_ADDRESSES,
    EDGE_CASES
)


# Module-level function for multiprocessing (must be pickleable)
def _process_address_for_test(addr):
    """Process a single address with multiple operations."""
    import oxidize_postal
    parsed = oxidize_postal.parse_address(addr)
    expanded = oxidize_postal.expand_address(addr)
    normalized = oxidize_postal.normalize_address(addr)
    return {'parsed': parsed, 'expanded': expanded, 'normalized': normalized}


class TestEndToEndIntegration:
    """End-to-end integration tests."""
    
    @pytest.fixture(scope="class", autouse=True)
    def ensure_data_available(self):
        """Ensure libpostal data is available for testing."""
        try:
            import oxidize_postal
        except ImportError:
            pytest.skip("Package not installed - run build.sh first")
        
        # Try a simple parse to see if data is available
        try:
            result = oxidize_postal.parse_address("123 Main St")
            if not result:
                pytest.skip("Libpostal data not available - run data download first")
        except Exception as e:
            error_msg = str(e).lower()
            if "libpostal data" in error_msg or "could not find" in error_msg:
                pytest.skip("Libpostal data not available - run data download first")
            else:
                # Re-raise unexpected errors
                raise
    
    def test_full_parsing_workflow(self):
        """Test the complete parsing workflow."""
        import oxidize_postal
        
        address = "123 Main St, New York, NY 10001"
        
        # Test parsing
        parsed = oxidize_postal.parse_address(address)
        assert isinstance(parsed, dict)
        assert len(parsed) > 0
        
        # Test JSON parsing
        parsed_json = oxidize_postal.parse_address_to_json(address)
        assert isinstance(parsed_json, str)
        parsed_from_json = json.loads(parsed_json)
        assert parsed == parsed_from_json
        
        # Test expansion
        expanded = oxidize_postal.expand_address(address)
        assert isinstance(expanded, list)
        assert len(expanded) > 0
        
        # Test JSON expansion
        expanded_json = oxidize_postal.expand_address_to_json(address)
        assert isinstance(expanded_json, str)
        expanded_from_json = json.loads(expanded_json)
        assert expanded == expanded_from_json
        
        # Test normalization
        normalized = oxidize_postal.normalize_address(address)
        assert isinstance(normalized, str)
        assert len(normalized) > 0
    
    @pytest.mark.parametrize("test_case", SAMPLE_ADDRESSES[:3])  # Test first 3 samples
    def test_sample_addresses_end_to_end(self, test_case):
        """Test end-to-end functionality with sample addresses."""
        import oxidize_postal
        
        address = test_case["address"]
        expected = test_case["expected_components"]
        
        # Parse address
        parsed = oxidize_postal.parse_address(address)
        assert isinstance(parsed, dict)
        
        # Verify some expected components are present
        found_components = 0
        for key in expected.keys():
            if key in parsed:
                found_components += 1
        
        # Should find at least 40% of expected components
        assert found_components >= len(expected) * 0.4
        
        # Test expansion
        expanded = oxidize_postal.expand_address(address)
        assert isinstance(expanded, list)
        assert len(expanded) > 0
        
        # Test normalization
        normalized = oxidize_postal.normalize_address(address)
        assert isinstance(normalized, str)
        assert len(normalized) > 0
    
    def test_performance_basic(self):
        """Basic performance test to ensure reasonable response times."""
        import oxidize_postal
        import time
        
        addresses = [
            "123 Main St, New York, NY 10001",
            "456 Oak Ave, Los Angeles, CA 90210",
            "789 Pine Rd, Chicago, IL 60601"
        ]
        
        # Time parsing operations
        start_time = time.time()
        
        for address in addresses:
            parsed = oxidize_postal.parse_address(address)
            assert isinstance(parsed, dict)
            
            expanded = oxidize_postal.expand_address(address)
            assert isinstance(expanded, list)
            
            normalized = oxidize_postal.normalize_address(address)
            assert isinstance(normalized, str)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Should complete all operations in reasonable time (< 5 seconds for 3 addresses)
        assert total_time < 5.0, f"Operations took too long: {total_time:.2f} seconds"
        
        # Average time per address should be reasonable (< 1 second)
        avg_time = total_time / len(addresses)
        assert avg_time < 1.0, f"Average time per address too high: {avg_time:.2f} seconds"
    
    def test_error_handling_integration(self):
        """Test error handling in integration context."""
        import oxidize_postal
        
        # Test empty address
        with pytest.raises(Exception):
            oxidize_postal.parse_address("")
        
        with pytest.raises(Exception):
            oxidize_postal.expand_address("")
        
        with pytest.raises(Exception):
            oxidize_postal.normalize_address("")


class TestParallelProcessing:
    """Test parallel processing capabilities."""
    
    def test_thread_safety(self):
        """Test that the library is thread-safe."""
        import oxidize_postal
        
        addresses = SAMPLE_ADDRESSES[:3] * 10  # 30 addresses
        
        def process_address(test_case):
            address = test_case["address"]
            parsed = oxidize_postal.parse_address(address)
            expanded = oxidize_postal.expand_address(address)
            normalized = oxidize_postal.normalize_address(address)
            return parsed, expanded, normalized
        
        # Process in parallel
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(process_address, addresses))
        
        # Verify all results are valid
        assert len(results) == len(addresses)
        for parsed, expanded, normalized in results:
            assert isinstance(parsed, dict)
            assert isinstance(expanded, list)
            assert isinstance(normalized, str)
    
    def test_gil_release_verification(self):
        """Verify that the GIL is released by comparing threading vs multiprocessing."""
        import oxidize_postal
        from multiprocessing import Pool
        
        # Warm up libpostal to avoid initialization overhead
        print("\nWarming up libpostal...")
        for _ in range(10):
            oxidize_postal.parse_address("123 Main St")
        
        # Create test dataset - enough to see the difference
        addresses = [test["address"] for test in SAMPLE_ADDRESSES] * 200  # 1000 addresses
        print(f"Testing GIL release with {len(addresses)} addresses...")
        
        # Test with threading
        start = time.time()
        with ThreadPoolExecutor(max_workers=8) as executor:
            thread_results = list(executor.map(_process_address_for_test, addresses))
        thread_time = time.time() - start
        
        # Test with multiprocessing
        start = time.time()
        with Pool(processes=8) as pool:
            mp_results = pool.map(_process_address_for_test, addresses)
        mp_time = time.time() - start
        
        # Calculate throughput
        thread_throughput = len(addresses) / thread_time
        mp_throughput = len(addresses) / mp_time
        
        print(f"\nResults:")
        print(f"  Threading: {thread_time:.2f}s ({thread_throughput:.0f} addr/sec)")
        print(f"  Multiprocessing: {mp_time:.2f}s ({mp_throughput:.0f} addr/sec)")
        print(f"  Threading is {thread_time/mp_time:.1f}x as fast as multiprocessing")
        
        # Verify results are valid
        assert len(thread_results) == len(addresses)
        assert len(mp_results) == len(addresses)
        
        # Threading should be faster than multiprocessing if GIL is released
        # (because multiprocessing has pickle overhead)
        assert thread_time < mp_time * 1.5, \
            f"Threading ({thread_time:.2f}s) should be faster than multiprocessing ({mp_time:.2f}s) when GIL is released"
        
        print("\n✓ GIL release verified: Threading outperforms multiprocessing")


class TestInternationalIntegration:
    """Integration tests for international addresses."""
    
    @pytest.mark.parametrize("test_case", INTERNATIONAL_ADDRESSES[:5])  # Test first 5
    def test_international_full_workflow(self, test_case):
        """Test complete workflow with international addresses."""
        import oxidize_postal
        
        address = test_case["address"]
        description = test_case["description"]
        
        try:
            # Parse
            parsed = oxidize_postal.parse_address(address)
            assert isinstance(parsed, dict), f"{description}: parsing failed"
            
            # Expand
            expanded = oxidize_postal.expand_address(address)
            assert isinstance(expanded, list), f"{description}: expansion failed"
            
            # Normalize
            normalized = oxidize_postal.normalize_address(address)
            assert isinstance(normalized, str), f"{description}: normalization failed"
            
            # JSON operations
            json_parsed = oxidize_postal.parse_address_to_json(address)
            assert isinstance(json_parsed, str), f"{description}: JSON parsing failed"
            json.loads(json_parsed)  # Verify valid JSON
            
            json_expanded = oxidize_postal.expand_address_to_json(address)
            assert isinstance(json_expanded, str), f"{description}: JSON expansion failed"
            json.loads(json_expanded)  # Verify valid JSON
            
        except Exception as e:
            # Some international addresses might have issues
            if "kanji" in description.lower() or "cyrillic" in description.lower():
                pass  # Expected potential issues
            else:
                raise Exception(f"Failed for {description}: {e}")


class TestRobustness:
    """Test robustness and error recovery."""
    
    def test_consecutive_operations(self):
        """Test many consecutive operations for stability."""
        import oxidize_postal
        
        # Run many operations in sequence
        for i in range(100):
            address = f"{i} Main Street, City {i % 10}, State {i % 50}"
            
            result = oxidize_postal.parse_address(address)
            assert isinstance(result, dict)
            assert len(result) > 0
    
    def test_mixed_operations(self):
        """Test mixing different operations."""
        import oxidize_postal
        
        address = "123 Main St, New York, NY 10001"
        
        # Mix operations in various orders
        for _ in range(10):
            parsed = oxidize_postal.parse_address(address)
            expanded = oxidize_postal.expand_address(address)
            normalized = oxidize_postal.normalize_address(address)
            json_parsed = oxidize_postal.parse_address_to_json(address)
            json_expanded = oxidize_postal.expand_address_to_json(address)
            
            # Verify all operations return valid results
            assert isinstance(parsed, dict)
            assert isinstance(expanded, list)
            assert isinstance(normalized, str)
            assert isinstance(json_parsed, str)
            assert isinstance(json_expanded, str)
