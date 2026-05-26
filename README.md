# Advanced Python API Scraper with Pagination

A production-grade Python script designed to automatically fetch, handle pagination, and extract structured product information from the DummyJSON dynamic API.

## Features
- **Automated Pagination:** Implements dynamic loop logic using `limit` and `skip` parameters to exhaustively collect all records.
- **Robust Error Handling:** Features complete exception handling for timeouts, HTTP errors, and JSON decoding faults.
- **Defensive Programming:** Safely parses deeply nested JSON response dictionaries using safe `.get()` fallbacks.

## Tech Stack
- Python 3
- Requests Library
