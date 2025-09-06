use pyo3::prelude::*;

pub mod postal;

// Import from the postal parsing module
use postal::python_api::{
    parse_address, parse_address_to_json, expand_address,
    expand_address_to_json, normalize_address, download_data
};
use postal::constants;

#[pymodule]
fn oxidize_postal(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Core parsing and expansion functions
    m.add_function(wrap_pyfunction!(parse_address, m)?)?;
    m.add_function(wrap_pyfunction!(parse_address_to_json, m)?)?;
    m.add_function(wrap_pyfunction!(expand_address, m)?)?;
    m.add_function(wrap_pyfunction!(expand_address_to_json, m)?)?;
    m.add_function(wrap_pyfunction!(normalize_address, m)?)?;
    m.add_function(wrap_pyfunction!(download_data, m)?)?;
    
    // Address component constants
    m.add("ADDRESS_NONE", constants::ADDRESS_NONE)?;
    m.add("ADDRESS_ANY", constants::ADDRESS_ANY)?;
    m.add("ADDRESS_NAME", constants::ADDRESS_NAME)?;
    m.add("ADDRESS_HOUSE_NUMBER", constants::ADDRESS_HOUSE_NUMBER)?;
    m.add("ADDRESS_STREET", constants::ADDRESS_STREET)?;
    m.add("ADDRESS_UNIT", constants::ADDRESS_UNIT)?;
    m.add("ADDRESS_LEVEL", constants::ADDRESS_LEVEL)?;
    m.add("ADDRESS_STAIRCASE", constants::ADDRESS_STAIRCASE)?;
    m.add("ADDRESS_ENTRANCE", constants::ADDRESS_ENTRANCE)?;
    m.add("ADDRESS_CATEGORY", constants::ADDRESS_CATEGORY)?;
    m.add("ADDRESS_NEAR", constants::ADDRESS_NEAR)?;
    m.add("ADDRESS_TOPONYM", constants::ADDRESS_TOPONYM)?;
    m.add("ADDRESS_POSTAL_CODE", constants::ADDRESS_POSTAL_CODE)?;
    m.add("ADDRESS_PO_BOX", constants::ADDRESS_PO_BOX)?;
    m.add("ADDRESS_ALL", constants::ADDRESS_ALL)?;
    
    Ok(())
}






