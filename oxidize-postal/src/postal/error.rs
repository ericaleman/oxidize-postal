//! Error types and handling for the postal address parser.
//!
//! Provides structured error types with detailed context for address parsing failures.

use pyo3::prelude::*;
use pyo3::exceptions::{PyValueError, PyRuntimeError};

/// Structured error types for postal address parsing
#[derive(Debug)]
pub enum PostalError {
    InvalidInput { message: String, context: String },
    LibpostalError { message: String },
    SerializationError { message: String },
    ConfigurationError { message: String },
}

impl std::fmt::Display for PostalError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            PostalError::InvalidInput { message, context } => {
                write!(f, "Invalid input: {}. Context: {}. Please ensure the input is a valid, non-empty string.", message, context)
            }
            PostalError::LibpostalError { message } => {
                write!(f, "Libpostal processing error: {}. This may indicate missing data files or an internal parsing issue.", message)
            }
            PostalError::SerializationError { message } => {
                write!(f, "JSON serialization error: {}. The parsed data could not be converted to JSON format.", message)
            }
            PostalError::ConfigurationError { message } => {
                write!(f, "Configuration error: {}. Please check your libpostal installation and data files.", message)
            }
        }
    }
}

impl std::error::Error for PostalError {}

impl From<PostalError> for PyErr {
    fn from(err: PostalError) -> Self {
        match err {
            PostalError::InvalidInput { .. } => PyValueError::new_err(err.to_string()),
            PostalError::LibpostalError { .. } => PyRuntimeError::new_err(err.to_string()),
            PostalError::SerializationError { .. } => PyRuntimeError::new_err(err.to_string()),
            PostalError::ConfigurationError { .. } => PyRuntimeError::new_err(err.to_string()),
        }
    }
}

impl From<libpostal_rust::Error> for PostalError {
    fn from(err: libpostal_rust::Error) -> Self {
        PostalError::LibpostalError {
            message: format!("libpostal error: {}", err),
        }
    }
}

impl From<serde_json::Error> for PostalError {
    fn from(err: serde_json::Error) -> Self {
        PostalError::SerializationError {
            message: format!("JSON serialization error: {}", err),
        }
    }
}