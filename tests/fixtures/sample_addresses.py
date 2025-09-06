"""
Test fixtures containing sample addresses for testing oxidize-postal.
"""

# Sample US addresses with expected parsing results
SAMPLE_ADDRESSES = [
    {
        "address": "123 Main St, New York, NY 10001",
        "expected_components": {
            "house_number": "123",
            "road": "main st",
            "city": "new york",
            "state": "ny",
            "postcode": "10001"
        },
        "description": "Simple NYC address"
    },
    {
        "address": "1600 Pennsylvania Ave NW, Washington, DC 20500",
        "expected_components": {
            "house_number": "1600",
            "road": "pennsylvania ave nw",
            "city": "washington",
            "state": "dc",
            "postcode": "20500"
        },
        "description": "White House address"
    },
    {
        "address": "781 Franklin Ave Crown Heights Brooklyn NYC NY 11216 USA",
        "expected_components": {
            "house_number": "781",
            "road": "franklin ave",
            "suburb": "crown heights",
            "city_district": "brooklyn",
            "city": "nyc",
            "state": "ny",
            "postcode": "11216",
            "country": "usa"
        },
        "description": "Complex address with multiple locality components"
    },
    {
        "address": "350 5th Ave, NYC, NY 10118",
        "expected_components": {
            "house_number": "350",
            "road": "5th ave",
            "city": "nyc",
            "state": "ny",
            "postcode": "10118"
        },
        "description": "Empire State Building"
    },
    {
        "address": "1 Apple Park Way, Cupertino, CA 95014",
        "expected_components": {
            "house_number": "1",
            "road": "apple park way",
            "city": "cupertino",
            "state": "ca",
            "postcode": "95014"
        },
        "description": "Apple headquarters"
    }
]

# Addresses with abbreviations for expansion testing
ABBREVIATION_TEST_CASES = [
    {
        "address": "123 Main St",
        "expected_expansions": ["123 main street"],
        "description": "Street abbreviation"
    },
    {
        "address": "456 Oak Ave",
        "expected_expansions": ["456 oak avenue"],
        "description": "Avenue abbreviation"
    },
    {
        "address": "789 Pine Rd",
        "expected_expansions": ["789 pine road"],
        "description": "Road abbreviation"
    }
]

# Invalid addresses for error testing
INVALID_ADDRESSES = [
    {
        "address": "",
        "expected_error": "Address cannot be empty",
        "description": "Empty address"
    },
    {
        "address": "   ",
        "expected_error": "Address cannot be empty",
        "description": "Whitespace-only address"
    }
]

# Expected normalized formats
NORMALIZATION_TEST_CASES = [
    {
        "address": "123 Main St, New York, NY 10001",
        "expected_normalized": "123, main st, new york, NY, 10001",
        "description": "Standard normalization"
    },
    {
        "address": "1600 Pennsylvania Ave NW, Washington, DC 20500",
        "expected_normalized": "1600, pennsylvania ave nw, washington, DC, 20500",
        "description": "Government address normalization"
    }
]

# International address edge cases
INTERNATIONAL_ADDRESSES = [
    {
        "address": "221B Baker Street, London NW1 6XE, United Kingdom",
        "expected_components": {
            "house_number": "221b",
            "road": "baker street",
            "city": "london",
            "postcode": "nw1 6xe",
            "country": "united kingdom"
        },
        "description": "UK address with alphanumeric house number"
    },
    {
        "address": "Champs-Élysées 75008 Paris France",
        "expected_components": {
            "road": "champs-élysées",
            "postcode": "75008",
            "city": "paris",
            "country": "france"
        },
        "description": "French address with accented characters"
    },
    {
        "address": "Alexanderplatz 1, 10178 Berlin, Deutschland",
        "expected_components": {
            "road": "alexanderplatz",
            "house_number": "1",
            "postcode": "10178",
            "city": "berlin",
            "country": "deutschland"
        },
        "description": "German address"
    },
    {
        "address": "東京都千代田区丸の内1-9-1 東京駅",
        "expected_components": {
            "city": "東京都千代田区",
            "suburb": "丸の内"
        },
        "description": "Japanese address with kanji characters"
    },
    {
        "address": "Москва, Красная площадь, дом 1",
        "expected_components": {
            "city": "москва",
            "road": "красная площадь",
            "house_number": "1"
        },
        "description": "Russian address with Cyrillic script"
    },
    {
        "address": "Rua Copacabana, 123, Rio de Janeiro, RJ, 22070-011, Brasil",
        "expected_components": {
            "road": "rua copacabana",
            "house_number": "123",
            "city": "rio de janeiro",
            "state": "rj",
            "postcode": "22070-011",
            "country": "brasil"
        },
        "description": "Brazilian address with hyphenated postal code"
    },
    {
        "address": "1 Queen's Road Central, Hong Kong",
        "expected_components": {
            "house_number": "1",
            "road": "queen's road central",
            "city": "hong kong"
        },
        "description": "Hong Kong address with apostrophe"
    },
    {
        "address": "Burj Khalifa, 1 Sheikh Mohammed bin Rashid Blvd, Dubai, UAE",
        "expected_components": {
            "house": "burj khalifa",
            "house_number": "1",
            "road": "sheikh mohammed bin rashid blvd",
            "city": "dubai",
            "country": "uae"
        },
        "description": "UAE address with landmark and long street name"
    }
]

# Edge cases for address parsing
EDGE_CASES = [
    {
        "address": "123",
        "expected_components": {
            "house_number": "123"
        },
        "description": "Just a number"
    },
    {
        "address": "Main Street",
        "expected_components": {
            "road": "main street"
        },
        "description": "Just a street name"
    },
    {
        "address": "New York",
        "expected_components": {
            "city": "new york"
        },
        "description": "Just a city name"
    },
    {
        "address": "90210",
        "expected_components": {
            "postcode": "90210"
        },
        "description": "Just a postal code"
    },
    {
        "address": "Apt 4B",
        "expected_components": {
            "unit": "apt 4b"
        },
        "description": "Just an apartment number"
    },
    {
        "address": "Floor 23, Suite 2301",
        "expected_components": {
            "level": "floor 23",
            "unit": "suite 2301"
        },
        "description": "Just floor and suite"
    },
    {
        "address": "!!!@#$%^&*()",
        "expected_components": {},
        "description": "Special characters only"
    },
    {
        "address": "123 Main St " * 100,  # Very long address
        "expected_components": {
            "house_number": "123",
            "road": "main st"
        },
        "description": "Very long repeated address"
    },
    {
        "address": "123 Main St\nNew York\nNY 10001",
        "expected_components": {
            "house_number": "123",
            "road": "main st",
            "city": "new york",
            "state": "ny",
            "postcode": "10001"
        },
        "description": "Address with newlines"
    },
    {
        "address": "123 Main St\tNew York\tNY\t10001",
        "expected_components": {
            "house_number": "123",
            "road": "main st",
            "city": "new york",
            "state": "ny",
            "postcode": "10001"
        },
        "description": "Address with tabs"
    }
]

# JSON serialization test cases
JSON_TEST_CASES = [
    {
        "address": "123 Main St, New York, NY 10001",
        "description": "JSON parsing test"
    },
    {
        "address": "1600 Pennsylvania Ave NW, Washington, DC 20500",
        "description": "JSON expansion test"
    }
]
