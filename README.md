# Geospatial File Measurement API

A simple FastAPI service that accepts KML files or ZIP files containing Shapefiles and returns feature information and measurements.

## Features

- Upload KML files
- Upload ZIP files containing Shapefiles
- Read feature geometry and properties
- Detect CRS
- Calculate polygon area
- Calculate LineString length
- Handle Point geometry without measurement
- Transform geographic CRS before measurement
- View uploaded file information
- View measurements for each feature

## Technologies Used

- Python
- FastAPI
- GeoPandas
- Shapely
- PyProj
- Uvicorn

## Project Structure

```text
geospatial-api/
│
├── main.py
├── processor.py
├── requirements.txt
├── README.md
├── .gitignore
├── uploads/
└── venv/