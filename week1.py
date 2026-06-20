import pandas as pd
import glob

listing_files = glob.glob("CRMLSListing*.csv")

listings_list = []
total_rows_list = 0
for files in listing_files:
    data_frame = pd.read_csv(files, low_memory = False)
    total_rows_list = total_rows_list + len(data_frame)
    listings_list.append(data_frame)

print("Listings before concatenation:", total_rows_list)

combined_listings = pd.concat(listings_list, ignore_index = True)
print("Listings after concatenation:", len(combined_listings)) #row count after concatenation
print("Listings before Residential filter:", len(combined_listings)) #row count before filter

combined_listings = combined_listings[combined_listings["PropertyType"] == "Residential"]
print("Listings after Residential filter:", len(combined_listings)) #row count after filter

combined_listings.to_csv("listings.csv", index = False)


sold_files = glob.glob("CRMLSSold*.csv")

sold_list = []
total_rows_sold = 0
for files in sold_files:
    data_frame = pd.read_csv(files, low_memory = False)
    total_rows_sold = total_rows_sold + len(data_frame)
    sold_list.append(data_frame)

print("Listings before concatenation:", total_rows_sold)

combined_sold = pd.concat(sold_list, ignore_index = True)
print("Listings after concatenation:", len(combined_sold))
print("Listings before Residential filter:", len(combined_sold))

combined_sold = combined_sold[combined_sold["PropertyType"] == "Residential"]
print("Listings after Residential filter:", len(combined_sold))

combined_sold.to_csv("sold.csv", index = False)
