# Data-Scraping-Python
This repository contains several production-like web scrapers written in Python.
They demonstrate my experience with HTML parsing, data cleaning, and building
ETL-style pipelines for real-world websites (e.g. Foxtrot, Multiplex).

## Projects

### 1. Foxtrot Smartphone Scraper

**Goal:** Collect structured smartphone specifications from the Foxtrot online store.

**Key features:**
- Parses 20+ attributes: brand, model, RAM/ROM, display, battery, cameras, OS, price, etc.
- Collects product links from paginated catalog pages.
- Normalizes inconsistent vendor data (dimensions, PPI, battery capacity).
- Handles missing fields, basic anti-bot measures (headers, delays, timeouts).
- Saves data to CSV for further analysis / ML tasks.

Source: `src/foxtrot/scraper.py`, `src/foxtrot/postprocess.py`.

### 2. Multiplex Movie Scraper

**Goal:** Build a movie dataset from the Multiplex cinema website.

**Key features:**
- Iterates over movie IDs and extracts metadata:
  - original title, genre, duration, release year, rental period,
  - country, studio, language, age limit, IMDb rating.
- Computes rental duration using Python `datetime`.
- Uses helper dictionaries and translation to normalize multilingual data.
- Produces a clean CSV dataset for analytics.

Source: `src/multiplex/scraper.py`, `src/multiplex/postprocess.py`, `src/common/helpers.py`.

## Tech Stack

- **Language:** Python 3.x  
- **Scraping:** `requests`, `BeautifulSoup4`, `lxml`, `user_agent`  
- **Data processing:** `datetime`, standard Python tools  
- **Output formats:** CSV / TXT (easily extendable to SQL / JSON)  

## Installation
