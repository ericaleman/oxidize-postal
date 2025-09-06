//! Address component constants and types.
//!
//! Provides constants for address components matching pypostal's API.

/// Address component constants (bit flags)
pub const ADDRESS_NONE: u64 = 0;
pub const ADDRESS_ANY: u64 = 0xFFFFFFFFFFFFFFFF;
pub const ADDRESS_NAME: u64 = 1 << 0;
pub const ADDRESS_HOUSE_NUMBER: u64 = 1 << 1;
pub const ADDRESS_STREET: u64 = 1 << 2;
pub const ADDRESS_UNIT: u64 = 1 << 3;
pub const ADDRESS_LEVEL: u64 = 1 << 4;
pub const ADDRESS_STAIRCASE: u64 = 1 << 5;
pub const ADDRESS_ENTRANCE: u64 = 1 << 6;
pub const ADDRESS_CATEGORY: u64 = 1 << 7;
pub const ADDRESS_NEAR: u64 = 1 << 8;
pub const ADDRESS_TOPONYM: u64 = 1 << 9;
pub const ADDRESS_POSTAL_CODE: u64 = 1 << 10;
pub const ADDRESS_PO_BOX: u64 = 1 << 11;
pub const ADDRESS_ALL: u64 = ADDRESS_ANY;

/// String normalization options (bit flags)
pub const NORMALIZE_STRING_LATIN_ASCII: u32 = 1 << 0;
pub const NORMALIZE_STRING_TRANSLITERATE: u32 = 1 << 1;
pub const NORMALIZE_STRING_STRIP_ACCENTS: u32 = 1 << 2;
pub const NORMALIZE_STRING_DECOMPOSE: u32 = 1 << 3;
pub const NORMALIZE_STRING_LOWERCASE: u32 = 1 << 4;
pub const NORMALIZE_STRING_TRIM: u32 = 1 << 5;
pub const NORMALIZE_STRING_REPLACE_HYPHENS: u32 = 1 << 6;
pub const NORMALIZE_STRING_SIMPLE_LATIN_ASCII: u32 = 1 << 7;
pub const NORMALIZE_STRING_REPLACE_NUMEX: u32 = 1 << 8;

/// Default string normalization options
pub const NORMALIZE_DEFAULT_STRING_OPTIONS: u32 = 
    NORMALIZE_STRING_LATIN_ASCII | 
    NORMALIZE_STRING_LOWERCASE | 
    NORMALIZE_STRING_TRIM;

/// Token normalization options (bit flags)
pub const NORMALIZE_TOKEN_REPLACE_HYPHENS: u32 = 1 << 0;
pub const NORMALIZE_TOKEN_DELETE_HYPHENS: u32 = 1 << 1;
pub const NORMALIZE_TOKEN_DELETE_FINAL_PERIOD: u32 = 1 << 2;
pub const NORMALIZE_TOKEN_DELETE_ACRONYM_PERIODS: u32 = 1 << 3;
pub const NORMALIZE_TOKEN_DROP_ENGLISH_POSSESSIVES: u32 = 1 << 4;
pub const NORMALIZE_TOKEN_DELETE_OTHER_APOSTROPHE: u32 = 1 << 5;
pub const NORMALIZE_TOKEN_SPLIT_ALPHA_FROM_NUMERIC: u32 = 1 << 6;
pub const NORMALIZE_TOKEN_REPLACE_DIGITS: u32 = 1 << 7;

/// Default token normalization options
pub const NORMALIZE_DEFAULT_TOKEN_OPTIONS: u32 = 
    NORMALIZE_TOKEN_DELETE_FINAL_PERIOD | 
    NORMALIZE_TOKEN_DELETE_ACRONYM_PERIODS;

/// Token type constants
pub const TOKEN_TYPE_WORD: &str = "word";
pub const TOKEN_TYPE_ABBREVIATION: &str = "abbreviation";
pub const TOKEN_TYPE_NUMBER: &str = "number";
pub const TOKEN_TYPE_ALPHANUMERIC: &str = "alphanumeric";
pub const TOKEN_TYPE_PUNCTUATION: &str = "punctuation";
pub const TOKEN_TYPE_WHITESPACE: &str = "whitespace";
pub const TOKEN_TYPE_OTHER: &str = "other";

/// Address component types as strings
pub const COMPONENT_HOUSE_NUMBER: &str = "house_number";
pub const COMPONENT_ROAD: &str = "road";
pub const COMPONENT_UNIT: &str = "unit";
pub const COMPONENT_LEVEL: &str = "level";
pub const COMPONENT_STAIRCASE: &str = "staircase";
pub const COMPONENT_ENTRANCE: &str = "entrance";
pub const COMPONENT_PO_BOX: &str = "po_box";
pub const COMPONENT_POSTCODE: &str = "postcode";
pub const COMPONENT_SUBURB: &str = "suburb";
pub const COMPONENT_CITY_DISTRICT: &str = "city_district";
pub const COMPONENT_CITY: &str = "city";
pub const COMPONENT_ISLAND: &str = "island";
pub const COMPONENT_STATE_DISTRICT: &str = "state_district";
pub const COMPONENT_STATE: &str = "state";
pub const COMPONENT_COUNTRY_REGION: &str = "country_region";
pub const COMPONENT_COUNTRY: &str = "country";
pub const COMPONENT_WORLD_REGION: &str = "world_region";
pub const COMPONENT_CATEGORY: &str = "category";
pub const COMPONENT_NEAR: &str = "near";
pub const COMPONENT_TOPONYM: &str = "toponym";

/// Get all available component types
pub fn get_all_component_types() -> Vec<&'static str> {
    vec![
        COMPONENT_HOUSE_NUMBER,
        COMPONENT_ROAD,
        COMPONENT_UNIT,
        COMPONENT_LEVEL,
        COMPONENT_STAIRCASE,
        COMPONENT_ENTRANCE,
        COMPONENT_PO_BOX,
        COMPONENT_POSTCODE,
        COMPONENT_SUBURB,
        COMPONENT_CITY_DISTRICT,
        COMPONENT_CITY,
        COMPONENT_ISLAND,
        COMPONENT_STATE_DISTRICT,
        COMPONENT_STATE,
        COMPONENT_COUNTRY_REGION,
        COMPONENT_COUNTRY,
        COMPONENT_WORLD_REGION,
        COMPONENT_CATEGORY,
        COMPONENT_NEAR,
        COMPONENT_TOPONYM,
    ]
}

/// Check if a component type is valid
pub fn is_valid_component_type(component_type: &str) -> bool {
    get_all_component_types().contains(&component_type)
}
