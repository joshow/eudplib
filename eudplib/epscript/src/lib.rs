#![allow(non_snake_case)]
#![feature(once_cell)]
use pyo3::prelude::*;
use std::collections::HashSet;
use std::str;
use std::sync::atomic::{AtomicBool, Ordering};
use std::{lazy::SyncLazy, sync::Mutex};

static MAP_DEBUG: AtomicBool = AtomicBool::new(false);
static BUILTIN_CONSTSET: SyncLazy<Mutex<HashSet<String>>> =
    SyncLazy::new(|| Mutex::new(HashSet::new()));

/// Set debug mode.
#[pyfunction]
fn setDebugMode(set: bool) {
    MAP_DEBUG.store(set, Ordering::SeqCst);
}

/// Register eudplib constants.
#[pyfunction]
fn registerPlibConstants(zeroSeperatedStrings: &[u8]) {
    let iter = zeroSeperatedStrings.split(|byte| *byte == 0u8);
    for bytes in iter {
        BUILTIN_CONSTSET
            .lock()
            .unwrap()
            .insert(str::from_utf8(bytes).unwrap().to_owned());
    }
}

/// Get compile error count.
#[pyfunction]
fn getErrorCount() -> i32 {
    0
}

/// Compile string.
#[pyfunction]
fn compileString(filename: &[u8], rawcode: &[u8]) -> PyResult<String> {
    Ok("".to_owned())
}

/// epScript compiler Python module implemented in Rust.
#[pymodule]
fn epscript(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(setDebugMode, m)?)?;
    m.add_function(wrap_pyfunction!(registerPlibConstants, m)?)?;
    m.add_function(wrap_pyfunction!(getErrorCount, m)?)?;
    m.add_function(wrap_pyfunction!(compileString, m)?)?;
    Ok(())
}
