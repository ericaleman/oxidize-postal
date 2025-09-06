//! Python API bindings for postal address parsing.
//!
//! Provides high-level Python functions for address parsing and expansion
//! with proper error handling and parameter validation.

use pyo3::prelude::*;
use std::collections::HashMap;
use crate::postal::error::PostalError;
use crate::postal::parser::{
    parse_address_string, parse_address_with_options,
    expand_address_string
};

/// Helper macro to reduce boilerplate for functions that release the GIL
macro_rules! with_gil_released {
    ($py:expr, $func:expr) => {
        $py.allow_threads($func).map_err(PyErr::from)
    };
}

/// Helper function to serialize to JSON with consistent error handling
fn to_json<T: serde::Serialize>(data: &T) -> Result<String, PostalError> {
    serde_json::to_string(data).map_err(|e| {
        PostalError::SerializationError {
            message: format!("Failed to serialize to JSON: {}", e),
        }
    })
}

/// Parse an address string into its component parts
/// 
/// Args:
///     address (str): The address string to parse
///     
/// Returns:
///     dict: A dictionary mapping component names to values
///     
/// Raises:
///     ValueError: If the address is empty or invalid
///     RuntimeError: If libpostal encounters an error
#[pyfunction]
#[pyo3(signature = (address))]
pub fn parse_address(
    py: Python<'_>, 
    address: &str
) -> PyResult<HashMap<String, String>> {
    with_gil_released!(py, || parse_address_with_options(address))
}

/// Parse an address string and return as JSON string
/// 
/// Args:
///     address (str): The address string to parse
///     
/// Returns:
///     str: JSON string representation of the parsed components
///     
/// Raises:
///     ValueError: If the address is empty or invalid
///     RuntimeError: If libpostal encounters an error or JSON serialization fails
#[pyfunction]
#[pyo3(signature = (address))]
pub fn parse_address_to_json(py: Python<'_>, address: &str) -> PyResult<String> {
    let parsed = with_gil_released!(py, || parse_address_string(address))?;
    to_json(&parsed).map_err(PyErr::from)
}

/// Expand abbreviations in an address string
/// 
/// Args:
///     address (str): The address string to expand
///     
/// Returns:
///     list[str]: List of possible expansions of the address
///     
/// Raises:
///     ValueError: If the address is empty or invalid
///     RuntimeError: If libpostal encounters an error
#[pyfunction]
#[pyo3(signature = (address))]
pub fn expand_address(
    py: Python<'_>, 
    address: &str
) -> PyResult<Vec<String>> {
    with_gil_released!(py, || expand_address_string(address))
}

/// Expand abbreviations in an address and return as JSON string
/// 
/// Args:
///     address (str): The address string to expand
///     
/// Returns:
///     str: JSON string representation of the expanded addresses
///     
/// Raises:
///     ValueError: If the address is empty or invalid
///     RuntimeError: If libpostal encounters an error or JSON serialization fails
#[pyfunction]
#[pyo3(signature = (address))]
pub fn expand_address_to_json(py: Python<'_>, address: &str) -> PyResult<String> {
    let expanded = with_gil_released!(py, || expand_address_string(address))?;
    to_json(&expanded).map_err(PyErr::from)
}

/// Normalize an address by parsing and reconstructing it
/// 
/// Args:
///     address (str): The address string to normalize
///     
/// Returns:
///     str: Normalized address string
///     
/// Raises:
///     ValueError: If the address is empty or invalid
///     RuntimeError: If libpostal encounters an error
#[pyfunction]
#[pyo3(signature = (address))]
pub fn normalize_address(py: Python<'_>, address: &str) -> PyResult<String> {
    let parsed = with_gil_released!(py, || parse_address_string(address))?;
    
    // Reconstruct address from components in a standard order
    let mut normalized_parts = Vec::new();
    
    // Add components in typical address order
    if let Some(house_number) = parsed.get("house_number") {
        normalized_parts.push(house_number.clone());
    }
    if let Some(road) = parsed.get("road") {
        normalized_parts.push(road.clone());
    }
    if let Some(unit) = parsed.get("unit") {
        normalized_parts.push(format!("Unit {}", unit));
    }
    if let Some(city) = parsed.get("city") {
        normalized_parts.push(city.clone());
    }
    if let Some(state) = parsed.get("state") {
        normalized_parts.push(state.to_uppercase());
    }
    if let Some(postcode) = parsed.get("postcode") {
        normalized_parts.push(postcode.clone());
    }
    if let Some(country) = parsed.get("country") {
        normalized_parts.push(country.to_uppercase());
    }
    
    if normalized_parts.is_empty() {
        return Err(PostalError::LibpostalError {
            message: "Failed to parse any recognizable address components from the input. The address may be malformed or in an unsupported format".to_string(),
        }.into());
    }
    
    Ok(normalized_parts.join(", "))
}

/// Download and setup libpostal data files
/// 
/// Args:
///     force (bool): Force re-download even if data exists
///     
/// Returns:
///     bool: True if successful, False otherwise
///     
/// Note:
///     This function requires the libpostal_data binary to be available.
///     On first use, you may need to run: python -m oxidize_postal.download_data
#[pyfunction]
#[pyo3(signature = (force=false))]
pub fn download_data(force: bool) -> PyResult<bool> {
    use std::process::Command;
    
    let python_cmd = if cfg!(windows) { "python" } else { "python3" };
    
    let mut cmd = Command::new(python_cmd);
    cmd.args(["-c", &format!(
        "import sys; sys.path.insert(0, '.'); from data_manager import download_data; download_data({})",
        if force { "True" } else { "False" }
    )]);
    
    match cmd.output() {
        Ok(output) => {
            if output.status.success() {
                Ok(true)
            } else {
                let stderr = String::from_utf8_lossy(&output.stderr);
                Err(PostalError::ConfigurationError {
                    message: format!("Data download failed: {}. Please check your internet connection and ensure you have write permissions to /usr/local/share/libpostal", stderr),
                }.into())
            }
        }
        Err(e) => {
            Err(PostalError::ConfigurationError {
                message: format!("Failed to run data download script: {}. Ensure Python is installed and the data_manager.py script is accessible", e),
            }.into())
        }
    }
}
