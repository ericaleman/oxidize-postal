"""
Example usage of oxidize-postal address parsing library.

This demonstrates the key functionality:
- Downloading libpostal data
- Parsing addresses into components
- Expanding abbreviations
- Normalizing addresses
"""

import oxidize_postal


def setup_data():
    """Setup libpostal data if not already available."""
    print("=== Setting up libpostal data ===")
    
    try:
        # Try to download data (this will be a no-op if already exists)
        success = oxidize_postal.download_data(force=False)  # Download libpostal data
        if success:
            print("✓ Data setup completed successfully")
            return True
        else:
            print("❌ Data setup failed")
            return False
    except Exception as e:
        print(f"❌ Error setting up data: {e}")
        print("\nTo manually setup data, run:")
        print("python -c 'import oxidize_postal; oxidize_postal.download_data()'")
        return False


def main():
    print("=== oxidize-postal Demo ===\n")
    
    # Setup data first
    if not setup_data():
        print("\n⚠️  Data setup failed. Please install libpostal data manually.")
        return
    
    print("\n=== Testing Address Parsing ===\n")
    
    # Example addresses to test
    test_addresses = [
        "781 Franklin Ave Crown Heights Brooklyn NYC NY 11216 USA",
        "123 Main St, New York, NY 10001",
        "1600 Pennsylvania Ave NW, Washington, DC 20500",
        "350 5th Ave, NYC, NY 10118",
    ]
    
    for i, address in enumerate(test_addresses, 1):
        print(f"--- Example {i} ---")
        print(f"Original: {address}")
        
        try:
            # Parse address into components
            parsed = oxidize_postal.parse_address(address)
            print(f"Parsed components: {parsed}")
            
            # Expand abbreviations
            expanded = oxidize_postal.expand_address(address)
            print(f"Expansions ({len(expanded)}): {expanded[:3]}{'...' if len(expanded) > 3 else ''}")
            
            # Normalize address
            normalized = oxidize_postal.normalize_address(address)
            print(f"Normalized: {normalized}")
            
        except Exception as e:
            print(f"Error processing address: {e}")
        
        print()
    
    # Demonstrate JSON output
    print("--- JSON Output Example ---")
    address = test_addresses[0]
    try:
        json_parsed = oxidize_postal.parse_address_to_json(address)
        json_expanded = oxidize_postal.expand_address_to_json(address)
        
        print(f"Parsed as JSON: {json_parsed}")
        print(f"Expanded as JSON: {json_expanded}")
        
    except Exception as e:
        print(f"Error with JSON output: {e}")


if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("Error: oxidize_postal module not found.")
        print("Please build and install the module first:")
        print("  maturin develop")
        print("Or install from PyPI:")
        print("  pip install oxidize-postal")
