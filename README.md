# Fuel Prices in France - Data Visualization Project

A comprehensive data visualization and analysis project for fuel prices across France using Python.

## Project Overview

On this project Marie and I wanted to create a dashboard that analyzes and visualizes fuel price data from France, providing interactive maps, charts, and detailed analysis tools. It processes real-time fuel price data via API and presents it through a web-based interface with multiple pages and components.

## Project Structure

```
project-data/
├── main.py                          # Main entry point
├── carte.py                         # Map visualization module
├── config.py                        # Configuration settings
├── extractionData.py                # Data extraction utilities
├── requirements.txt                 # Python dependencies
├── prix-des-carburants-en-france-flux-instantane-v2.json  # Fuel price data (JSON)
├── src/
│   ├── components/                  # Reusable UI components
│   │   ├── charts.py               # Chart components
│   │   ├── footer.py               # Footer component
│   │   ├── header.py               # Header component
│   │   └── navbar.py               # Navigation bar component
│   ├── pages/                       # Application pages
│   │   ├── home.py                 # Home page
│   │   ├── about.py                # About page
│   │   ├── city_histogram.py       # City histogram page
│   │   ├── franceMap.py            # France map page
│   │   └── more_complex_page/      # Advanced page features
│   │       ├── layout.py           # Page layout
│   │       └── page_specific_component.py  # Page-specific components
│   └── utils/                       # Utility functions
│       ├── get_data.py             # Data retrieval functions
│       ├── clean_data.py           # Data cleaning utilities
│       └── common_functions.py     # Common utility functions
└── README.md                        # This file
```

## Features

- **Interactive Maps**: Visualization of fuel prices across French cities using `carte.py`
- **Data Analysis**: Extract and analyze fuel price data from JSON and CSV sources
- **Charts & Graphs**: Multiple chart components for data visualization
- **Multi-page Application**: Home, About, City Histogram, and France Map pages
- **Responsive UI**: Header, navbar, and footer components

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd project-data
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main application:
```bash
python main.py
```

## Data Sources

- `prix-des-carburants-en-france.csv`: Historical fuel price data
- `prix-des-carburants-en-france-flux-instantane-v2.json`: Real-time fuel price data

## Configuration

Edit `config.py` to customize:
- Data paths
- API endpoints
- Visualization settings
- Other application parameters

## Dependencies

See `requirements.txt` for all required Python packages.

## Contributing

Feel free to submit issues and pull requests to improve the project.
