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