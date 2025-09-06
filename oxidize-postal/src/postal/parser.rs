//! Core postal address parsing functionality - thin wrapper around libpostal

use libpostal_rust::{ParseAddressOptions, ExpandAddressOptions, parse_address, expand_address};
use std::collections::HashMap;
use crate::postal::error::PostalError;

/// Parse an address string into its component parts
pub fn parse_address_string(address: &str) -> Result<HashMap<String, String>, PostalError> {
    parse_address_with_options(address)
}

/// Parse an address string into its component parts
pub fn parse_address_with_options(
    address: &str
) -> Result<HashMap<String, String>, PostalError> {
    if address.trim().is_empty() {
        return Err(PostalError::InvalidInput {
            message: "Address string is empty or contains only whitespace".to_string(),
            context: "Valid address parsing requires a non-empty string with actual address content".to_string(),
        });
    }

    let options = ParseAddressOptions::default();
    
    parse_address(address, &options).map_err(|e| PostalError::LibpostalError {
        message: format!("Failed to parse address: {}", e),
    })
}

/// Expand abbreviations in an address string
pub fn expand_address_string(address: &str) -> Result<Vec<String>, PostalError> {
    if address.trim().is_empty() {
        return Err(PostalError::InvalidInput {
            message: "Address string is empty or contains only whitespace".to_string(),
            context: "Address expansion requires a valid address string to process abbreviations".to_string(),
        });
    }

    let options = ExpandAddressOptions::default();

    expand_address(address, &options).map_err(|e| {
        PostalError::LibpostalError {
            message: format!("Failed to expand address: {}", e),
        }
    })
}