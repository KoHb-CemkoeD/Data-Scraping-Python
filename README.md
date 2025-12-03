# Data-Scraping-Python
This repository contains Python-based web scrapers developed for collecting structured datasets
from real websites (Foxtrot and Multiplex). They demonstrate my experience with HTML parsing, data cleaning, and building
ETL-style pipelines.

---

**Only the data collection and preprocessing logic is stored here.  
All further data analysis, visualization and neural network training are located in the
corresponding Google Colab notebooks.** 

[Foxtrot Data Analysis](https://colab.research.google.com/drive/10STGxWEO3naigRtrDBYrGiVlCX6Tasls?hl=uk)

[Multiplex Data Analysis](https://colab.research.google.com/drive/19C9KnEcdJktk61h1Y8UGhI7xqpEULG-N?hl=uk) 

---

# Table of Contents
1. [Description](#description)  
2. [Project Structure](#project-structure)  
3. [Technologies Used](#technologies-used)  
4. [Implementation](#implementation)  
5. [Key Features](#key-features)  
6. [Database Structure](#database-structure)  
7. [Conclusions](#conclusions)

---

## Description

### 1. Foxtrot Smartphone Scraper

**Goal:** Collect structured smartphone specifications from the Foxtrot online store foxtrot.com.ua.  

**Key features:**
- Parses 20+ attributes: brand, model, RAM/ROM, display, battery, cameras, OS, price, etc.
- Collects product links from paginated catalog pages.
- Normalizes inconsistent vendor data (dimensions, PPI, battery capacity).
- Handles missing fields, basic anti-bot measures (headers, delays, timeouts).
- Saves data to CSV for further analysis / ML tasks.

### 2. Multiplex Movie Scraper

**Goal:** Build a movie dataset from the Multiplex cinema website multiplex.ua.  

**Key features:**
- Iterates over movie IDs and extracts metadata:
  - original title, genre, duration, release year, rental period,
  - country, studio, language, age limit, IMDb rating.
- Computes rental duration using Python `datetime`.
- Uses helper dictionaries and translation to normalize multilingual data.
- Produces a clean CSV dataset for analytics.

## Tech Stack

- **Language:** Python 3.x  
- **Scraping:** `requests`, `BeautifulSoup4`, `lxml`, `user_agent`  
- **Data processing:** `datetime`, standard Python tools  
- **Output formats:** CSV / TXT (easily extendable to SQL / JSON)  

---

## Project Structure

Data-Scraping-Python

```
│
├── foxtrot/
│ ├── DataCollector.py # scraping product pages
│ ├── foxtrot_urls.txt # collected product links
│ ├── foxtrot.txt # final dataset (CSV format)
│ └── main.py # run/organize scrapers
│
├── multiplex/
│ ├── DataCollector.py # scraping movie pages
│ ├── DataCollectorHelper.py # data normalization dictionaries
│ ├── metadata.txt # notes for dataset processing
│ ├── multiplex.txt # final dataset (CSV format)
│ └── main.py # run/organize scrapers
│
└── README.md
```
---

## Technologies Used

### **Python Stack**
- `requests` — HTTP requests  
- `BeautifulSoup4` — HTML parsing  
- `lxml` — fast parser backend  
- `user_agent` — dynamic UA rotation  
- `googletrans` — translation and normalization  
- `datetime` — rental period calculation  
- `csv` / text output

### **Scraping Techniques**
- Pagination crawling  
- ID-based scanning (bruteforce range)  
- Custom parsing of complex HTML structures  
- Error tolerance, timeouts, and safe retries  
- Data cleaning, deduplication and value fixing

---

## Implementation

### **Foxtrot Scraper**
Located in `foxtrot/DataCollector.py`.

- Collects product links from category pages (`foxtrot_urls.txt`)
- Visits each product page
- Extracts 20+ attributes:
  - brand, model, RAM, ROM  
  - display height/width, diagonal, type  
  - CPU cores and max frequency  
  - battery capacity  
  - camera megapixels  
  - OS, material  
  - dimensions, weight  
  - price  
- Automatically fixes inconsistent fields (e.g., missing PPI computation)
- Saves normalized dataset to `foxtrot.txt`
---

### **Multiplex Scraper**
Located in `multiplex/DataCollector.py`.

- Iterates through thousands of movie IDs
- Extracts:
  - original name  
  - genre  
  - country  
  - studio  
  - duration  
  - age limit  
  - release year  
  - rental duration (start–end difference)  
  - IMDb rating  
- Normalizes country/genre/studio values using dictionary maps
- Saves final dataset to `multiplex.txt`
---

## Key Features

- **Fully automated crawling pipeline**
- **UA rotation + timeouts** to reduce blocking
- **Robust HTML parsing** with fallbacks for missing fields
- **Custom normalization layer** (`DataCollectorHelper.py`)
- **Computation of derived fields** (PPI, rental period, etc.)
- **Clean CSV-like datasets ready for ML**

---

## Database Structure

### Foxtrot Smartphone Dataset
| Field | Description |
|-------|-------------|
| brand, model | Device identification |
| ROM, RAM | Memory specs |
| display_h / w / diagonal | Resolution and physical size |
| display_type | AMOLED / IPS |
| ppi | Computed manually if missing |
| cpu_cores, cpu_max_freq | Hardware characteristics |
| battery_cap | Battery mAh |
| camera_main / front | Megapixels |
| OS | Android/iOS |
| price | Final listed price |

---

### Multiplex Movie Dataset
| Field | Description |
|-------|-------------|
| name | Original movie title |
| genre | Primary genre |
| studio | Production studio |
| country | Country of origin |
| duration | In minutes |
| age_limit | Age restriction |
| release | Release year |
| rental_duration | Days in cinema |
| rating | IMDb rating |

---

## Conclusions

This repository demonstrates a complete real-world data collection workflow:
- collecting raw HTML from modern websites,
- parsing complex page structures,
- cleaning and normalizing extracted fields,
- producing structured datasets ready for downstream analytics or neural network training.

The project shows proficiency in **Python scraping**, **data engineering**, and **ETL-style preprocessing**, which are essential skills for data collection, research pipelines, and ML preparation.

---
