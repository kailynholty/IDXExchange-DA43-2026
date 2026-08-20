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

Script will print row counts before and after concatenation and before and after the residential filter in the following format:
```
Listings before concatenation: XXX,XXX
Listings after concatenation: XXX,XXX
Listings before Residential filter: XXX,XXX
Listings after Residential filter: XXX,XXX
```
## Weeks 2 and 3
Filter data for only relevant residential property records by analyzing missing column values and review key numeric fields for statistical relevance. Enriches dataset by merging FRED, the national 30-year fixed mortgage rate, with the combined sold and listings datasets.
### Running the Script
The script will print the dataset size, including row and column count, column data types, and the first couple rows of the datasets. Then it will calculate missing counts and percentages per column, flagging and dropping columns with >90% missing values. The script will produce a numeric distribution summary (min, max, mean, median, percentiles) for ```ClosePrice```, ```LivingArea```, and ```DaysOnMarket```.

The script will then merge FRED mortgage rate data onto both combined datasets using a ```year_month``` key.

### Key Findings
**Dataset Size**
- Listings: 572,122 rows x 84 columns
- Sold: 491,086 rows x 84 columns

**Missing Values**
- Listings: 13 columns with >90% missing values, 71 columns with at least one missing value
- Sold: 15 columns with >90% missing values, 73 columns with at least one missing value

**Numeric Field EDA Analysis**
- Close Price: $823,000 median and $1,185,313 mean from sold data
- Days On Market: 18 days median and 36.9 days mean from sold data
- Counties with Highest Median Prices: Del Norte, San Mateo, Santa Clara, San Francisco, Santa Cruz

**FRED MORTGAGE30US**
- 30-year fixed mortgage rate from the St. Louis Federal Reserve
- Resampled weekly data into monthly average before merging datasets using a ```year_month``` key
- Zero null mortgage rates for sold data and listing data, confirming a complete join of datasets

## Weeks 4 and 5
Prepares datasets for reliable analysis by fixing formatting inconsistencies, performing date consistency checks, handling missing or redundant information, and doing geographic data checks.
### Running the Script
The script converts date fields to date time format, removes duplicate columns, and flags invalid numeric values. The script also performs date consistency checks, flagging errors, and performs geographic data checks that flags missing coordinates, null values, and implausible coordinates.

### Key Findings
**Invalid Numeric Values**
- Sold: 1 entry where ```ClosePrice``` <= 0, 166 entries where ```LivingArea``` <= 0, 67 entries where ```DaysOnMarket``` < 0, and 0 entries where ```BedroomsTotal``` and ```BathroomsTotalInteger``` are negative
- Listings: 0 entries where ```ClosePrice``` <= 0, 384 entries where ```LivingArea``` <= 0, 31 entries where ```DaysOnMarket``` < 0, and 0 entries where ```BedroomsTotal``` and ```BathroomsTotalInteger``` are negative

## Week 6
Engineer key market indicators to prepare for Tableau dashboards.
### Running the Script
Creates the following key metrics: ```PriceRatio```, ```PricePerSqFt```, ```DaysOnMarketMetric```, ```YrMo```, ```CloseOriginalListRatio```, ```ListingContractDays```, and ```ContractCloseDays```. The script additionally adds school district information and segment analysis.

### Key Findings
- Sold unified school districts found: 325
- Listings unified school districts found: 337
- Sold properties with district assigned: 170085
- Listing properties with district assigned: 379274

## Week 7
Filters key numeric fields for outliers and removes extreme values.
### Running the Script
Uses the Interquartile Range method to remove records that fall out of a defined statistical range. Saves a csv file with flagged outliers and removed outliers.

### Key Findings
**Outliers**
- Sold: ```ClosePrice``` = 17,066, ```LivingArea``` = 10,041, ```DaysOnMarket``` = 17,455
- Listings: ```ClosePrice``` = 11,857, ```LivingArea``` = 28,286, ```DaysOnMarket``` = 55,392

**Rows Before and After Filtering**
- Sold: before = 226,304, after = 190,409
- Listings: before = 572,122, after = 484,728

**Sold Median Values Before and After Filtering**
- ```ClosePrice```: before = 825,000, after = 790,000
- ```LivingArea```: before = 1,640, after = 1,566
- ```DaysOnMarket```: before = 17, after = 14

**Listings Median Values Before and After Filtering**
- ```ClosePrice```: before = 851,000, after = 825,000
- ```LivingArea```: before = 1,670, after = 1,610
- ```DaysOnMarket```: before = 11, after = 10
