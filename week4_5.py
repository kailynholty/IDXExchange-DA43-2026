import pandas as pd

listings_with_rates = pd.read_csv("listings_with_rates.csv", low_memory = False)
sold_with_rates = pd.read_csv("sold_with_rates.csv", low_memory = False)

print("Listings: " + str(listings_with_rates.shape[0]) + " rows x " + str(listings_with_rates.shape[1]) + " columns")
print("Sold: " + str(sold_with_rates.shape[0]) + " rows x " + str(sold_with_rates.shape[1]) + " columns")

#removes unnecessary columns (>90% null value)
def drop_unnecessary_columns(df, label, threshold = 0.9):
    total_rows = len(df)
    missing_count = df.isnull().sum()
    missing_percent = missing_count / total_rows
    flagged = missing_percent[missing_percent > threshold]

    print(label + " Columns with >90% missing: ")
    print(flagged)

    df = df.drop(columns = flagged.index)

    return df

sold_with_rates = drop_unnecessary_columns(sold_with_rates, "Sold")
listings_with_rates = drop_unnecessary_columns(listings_with_rates, "Listings")

#remove duplicate columns
listing_01 = []
for columns in listings_with_rates.columns:
    if columns.endswith(".1"):
        listing_01.append(columns)

listing_duplicates = []
for columns in listing_01:
    original = columns.replace(".1", "")
    if listings_with_rates[columns].equals(listings_with_rates[original]):
        listing_duplicates.append(columns)

print("Duplicate columns in Listings: " + str(listing_duplicates))
listings_with_rates = listings_with_rates.drop(columns = listing_duplicates)

#remove columns with unnecessary information
#unnecessary_columns = ["BuyerOfficeAOR", "BuyerAgentAOR", "ListAgentAOR", "OriginatingSystemSubName"]

#convert date fields to datetime format
date_fields = ["CloseDate", "PurchaseContractDate", "ListingContractDate", "ContractStatusChangeDate"]

for field in date_fields:
    if field in sold_with_rates.columns:
        sold_with_rates[field] = pd.to_datetime(sold_with_rates[field])
    if field in listings_with_rates.columns:
        listings_with_rates[field] = pd.to_datetime(listings_with_rates[field])

#make sure numeric fields are the proper type
numeric_fields = ["ClosePrice", "ListPrice", "OriginalListPrice", "LivingArea", "LotSizeAcres",
                  "BedroomsTotal", "BathroomsTotalInteger", "DaysOnMarket", "YearBuilt"]

for field in numeric_fields:
    if field in sold_with_rates.columns:
        sold_with_rates[field] = pd.to_numeric(sold_with_rates[field])
    if field in listings_with_rates.columns:
        listings_with_rates[field] = pd.to_numeric(listings_with_rates[field])

#flags invalid numeric types
sold_with_rates["invalid_closeprice_flag"] = sold_with_rates["ClosePrice"] <= 0
listings_with_rates["invalid_closeprice_flag"] = listings_with_rates["ClosePrice"] <= 0
print("Sold Invalid ClosePrice: " + str(sold_with_rates["invalid_closeprice_flag"].sum()))
print("Listings Invalid ClosePrice: " + str(listings_with_rates["invalid_closeprice_flag"].sum()))

sold_with_rates["invalid_livingarea_flag"] = sold_with_rates["LivingArea"] <= 0
listings_with_rates["invalid_livingarea_flag"] = listings_with_rates["LivingArea"] <= 0
print("Sold Invalid LivingArea: " + str(sold_with_rates["invalid_livingarea_flag"].sum()))
print("Listings Invalid LivingArea: " + str(listings_with_rates["invalid_livingarea_flag"].sum()))

sold_with_rates["invalid_daysonmarket_flag"] = sold_with_rates["DaysOnMarket"] < 0
listings_with_rates["invalid_daysonmarket_flag"] = listings_with_rates["DaysOnMarket"] < 0
print("Sold Invalid DaysOnMarket: " + str(sold_with_rates["invalid_daysonmarket_flag"].sum()))
print("Listings Invalid DaysOnMarket: " + str(listings_with_rates["invalid_daysonmarket_flag"].sum()))

sold_with_rates["invalid_bedroomstotal_flag"] = sold_with_rates["BedroomsTotal"] < 0
listings_with_rates["invalid_bedroomstotal_flag"] = listings_with_rates["BedroomsTotal"] < 0
print("Sold Invalid BedroomsTotal: " + str(sold_with_rates["invalid_bedroomstotal_flag"].sum()))
print("Listings Invalid BedroomsTotal: " + str(listings_with_rates["invalid_bedroomstotal_flag"].sum()))

sold_with_rates["invalid_bathroomstotalinteger_flag"] = sold_with_rates["BathroomsTotalInteger"] < 0
listings_with_rates["invalid_bathroomstotalinteger_flag"] = listings_with_rates["BathroomsTotalInteger"] < 0
print("Sold Invalid BathroomsTotalInteger: " + str(sold_with_rates["invalid_bathroomstotalinteger_flag"].sum()))
print("Listings Invalid BathroomsTotalInteger: " + str(listings_with_rates["invalid_bathroomstotalinteger_flag"].sum()))


#flag date consistency errors
sold_with_rates["listing_after_close_flag"] = (sold_with_rates["ListingContractDate"] > sold_with_rates["CloseDate"])
sold_with_rates["purchase_after_close_flag"] = (sold_with_rates["PurchaseContractDate"] > sold_with_rates["CloseDate"])
sold_with_rates["negative_timeline_flag"] = (sold_with_rates["PurchaseContractDate"] < sold_with_rates["ListingContractDate"])

print("Listing after Close Errors: " + str(sold_with_rates["listing_after_close_flag"].sum()))
print("Purchase after Close Errors: " + str(sold_with_rates["purchase_after_close_flag"].sum()))
print("Negative Timeline Errors: " + str(sold_with_rates["negative_timeline_flag"].sum()))


#flag geographic data errors
sold_with_rates["missing_coordinates_flag"] = (sold_with_rates["Latitude"].isnull() | sold_with_rates["Longitude"].isnull())
listings_with_rates["missing_coordinates_flag"] = (listings_with_rates["Latitude"].isnull() | listings_with_rates["Longitude"].isnull())
print("Sold Missing Coordinates: " + str(sold_with_rates["missing_coordinates_flag"].sum()))
print("Listings Missing Coordinates: " + str(listings_with_rates["missing_coordinates_flag"].sum()))

sold_with_rates["zero_coordinate_flag"] = ((sold_with_rates["Latitude"] == 0) | (sold_with_rates["Longitude"] == 0))
listings_with_rates["zero_coordinate_flag"] = ((listings_with_rates["Latitude"] == 0) | (listings_with_rates["Longitude"] == 0))
print("Sold Zero Coordinate: " + str(sold_with_rates["zero_coordinate_flag"].sum()))
print("Listings Zero Coordinate: " + str(listings_with_rates["zero_coordinate_flag"].sum()))

sold_with_rates["longitude_error_flag"] = (sold_with_rates["Longitude"] > 0)
listings_with_rates["longitude_error_flag"] = (listings_with_rates["Longitude"] > 0)
print("Sold Longitude Errors: " + str(sold_with_rates["longitude_error_flag"].sum()))
print("Listings Longitude Errors: " + str(listings_with_rates["longitude_error_flag"].sum()))

sold_with_rates["implausible_coordinates_flag"] = (
    (sold_with_rates["Latitude"] <= 32.53) | (sold_with_rates["Latitude"] >= 42) |
    (sold_with_rates["Longitude"] <= -124.44) | (sold_with_rates["Longitude"] >= -114.13)
)
print("Sold Out-of-State Coordinates: " + str(sold_with_rates["implausible_coordinates_flag"].sum()))

listings_with_rates["implausible_coordinates_flag"] = (
    (listings_with_rates["Latitude"] <= 32.53) | (listings_with_rates["Latitude"] >= 42) |
    (listings_with_rates["Longitude"] <= -124.44) | (listings_with_rates["Longitude"] >= -114.13)
)
print("Listings Out-of-State Coordinates: " + str(listings_with_rates["implausible_coordinates_flag"].sum()))


#save CSV files
sold_with_rates.to_csv("sold_week4_5.csv", index = False)
listings_with_rates.to_csv("listings_week4_5.csv", index = False)
