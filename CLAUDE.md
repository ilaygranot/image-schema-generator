# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Streamlit web application that generates schema.org ImageObject structured data for web scraping. The app takes URLs as input, scrapes images from those pages, and generates JSON-LD schema markup that can be used for SEO and search engine optimization.

## Core Architecture

- **Single-file Streamlit app** (`app.py`) - Main application logic
- **Web scraping pipeline**: URLs → HTTP requests → HTML parsing → Image extraction → Schema generation
- **Data flow**: User input → BeautifulSoup parsing → JSON-LD schema → CSV export
- **Schema.org compliance**: Generates ImageObject structured data following schema.org guidelines

## Development Commands

### Running the Application
```bash
streamlit run app.py
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Installing Additional Dependencies
The requirements.txt is incomplete. To run the app, you'll need:
```bash
pip install streamlit requests beautifulsoup4 pandas
```

## Key Components

### Schema Generation Logic
- Extracts `img` tags from HTML using BeautifulSoup
- Maps HTML attributes to schema.org ImageObject properties:
  - `alt` attribute → `name` and `description` fields
  - `src` attribute → `contentUrl` field
  - Optional `height` and `width` attributes when present
- Generates nested schema structure with page URL and array of image objects

### User Agent Strategy
Uses mobile Googlebot user agent string to ensure consistent crawling behavior and avoid bot blocking.

### Data Export
Results are formatted as CSV with columns: `url`, `img_schema` and made available for download with date-stamped filenames.

## Technical Notes

- Uses `@st.cache_data` decorator for DataFrame caching
- Session state management for download functionality
- Handles missing image attributes gracefully with `.get()` method
- Filters out blurred image duplicates (images containing "blur_" in URL)
- Cleans alt text by removing "Writer:" prefix for cleaner schema output
- No error handling for failed HTTP requests or invalid URLs