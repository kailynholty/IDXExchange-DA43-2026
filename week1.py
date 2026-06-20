import pandas as pd
import glob

#LISTINGS:
listing_files = glob.glob("CRMLSListing*.csv")

#converting the listings into data frames before concatenation
listings_list = []
total_rows_list = 0
for files in listing_files:
    data_frame = pd.read_csv(files, low_memory = False)
    total_rows_list = total_rows_list + len(data_frame)
    listings_list.append(data_frame)

print("Listings before concatenation:", total_rows_list) #row count before concatenation

#concatenating the listings using pandas
combined_listings = pd.concat(listings_list, ignore_index = True)
print("Listings after concatenation:", len(combined_listings)) #row count after concatenation
print("Listings before Residential filter:", len(combined_listings)) #row count before filter

#filtering for residential listings only
combined_listings = combined_listings[combined_listings["PropertyType"] == "Residential"]
print("Listings after Residential filter:", len(combined_listings)) #row count after filter

#creating a new listings.csv file
combined_listings.to_csv("listings.csv", index = False)

#SOLD:
sold_files = glob.glob("CRMLSSold*.csv")

#converting the sold files into data frames before concatenation
sold_list = []
total_rows_sold = 0
for files in sold_files:
    data_frame = pd.read_csv(files, low_memory = False)
    total_rows_sold = total_rows_sold + len(data_frame)
    sold_list.append(data_frame)

print("Listings before concatenation:", total_rows_sold) #row count before concatenation

#concatenating the sold files using pandas
combined_sold = pd.concat(sold_list, ignore_index = True)
print("Listings after concatenation:", len(combined_sold)) #row count after concatenation
print("Listings before Residential filter:", len(combined_sold)) #row count before applying residential filter

#filtering for residential listings only
combined_sold = combined_sold[combined_sold["PropertyType"] == "Residential"]
print("Listings after Residential filter:", len(combined_sold)) #row count after apply residential filter

#creating a new sold.csv file
combined_sold.to_csv("sold.csv", index = False)