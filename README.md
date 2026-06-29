# IDX Exchange - Data Analyst Internship (Summer 2026)
This repository contains my Python scripts, documentation, and work from the IDX Exchange real estate data analytics internship over the course of twelve weeks.

## Project Overview
The project focuses on transforming monthly MLS listing and sold transaction data into cleaned datasets that can be used to analyze real estate market trends and communicate housing market insights in Tableau Dashboard.

## Requirements
- Python 3.x
- Pandas (data processing)
- Glob (file handling)

## Week 0
Extract monthly MLS data from the scripts ```crmls_listed.py``` and ```crmls_sold.py```. This will provide the datasets, in structured CSV format, for analysis.
### Running the Scripts
To generate monthly sold or listed data, update the data range in the filter statement for the specific month of data needed.
```python
'$filter': f"ListingContractDate ge {datetime(2026, 1, 1).isoformat(timespec='milliseconds')}Z and ListingContractDate lt {datetime(2026, 6, 1).isoformat(timespec='milliseconds')}Z",
```
The first data point represents the target month while the second data point is the beginning of the next month. Make sure to update the output filename.
```python
csv_file = 'CRMLSListing202601.csv'
```
## Week 1
Load and concatenate monthly CSV data from January 2024 to May 2026 into two master tables: ```listings.csv``` and ```sold.csv```. Filter for Residential property types only.
### Running the Script
Place the script in the same directory as the monthly CRMLS files. 

The script will locate all ```CRMLS.listing*.csv``` and ```CRMLS.sold*.csv``` files. Then, it will load each CSV file into a pandas Dataframe to concatenate monthly files into either listings or sold. Both datasets will then be filtered for ```PropertyType == "Residential"```. Cleaned datasets will be saved as ```listings.csv``` and ```sold.csv```.
## Week 2
