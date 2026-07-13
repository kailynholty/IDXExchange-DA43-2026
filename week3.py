import pandas as pd

listings_cleaned = pd.read_csv("listings_cleaned.csv", low_memory = False)
sold_cleaned = pd.read_csv("sold_cleaned.csv", low_memory = False)

#FRED Mortgage Data
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage = pd.read_csv(url, parse_dates = ["observation_date"])
mortgage.columns = ["date", "rate_30yr_fixed"]

#Resample from weeks to monthly averages
mortgage["year_month"] = mortgage["date"].dt.to_period("M")
mortgage_monthly = (mortgage.groupby("year_month")["rate_30yr_fixed"].mean().reset_index())

#Creates a year_month column in cleaned sold and listings datasets
sold_cleaned["CloseDate"] = pd.to_datetime(sold_cleaned["CloseDate"])
sold_cleaned["year_month"] = sold_cleaned["CloseDate"].dt.to_period("M")

listings_cleaned["CloseDate"] = pd.to_datetime(listings_cleaned["CloseDate"])
listings_cleaned["year_month"] = listings_cleaned["CloseDate"].dt.to_period("M")

#Merges mortgage column to the sold and listings datasets
sold_with_rates = sold_cleaned.merge(mortgage_monthly, on = "year_month", how = "left")
listings_with_rates = listings_cleaned.merge(mortgage_monthly, on = "year_month", how = "left")

#Checks for null values
print("Null mortgage rates for sold:", sold_with_rates["rate_30yr_fixed"].isnull().sum())
print("Null mortgage rates for listings:", listings_with_rates["rate_30yr_fixed"].isnull().sum())

#Prints a preview of the merge
print("\nPreview Merge")
print(sold_with_rates[["CloseDate", "year_month", "ClosePrice", "rate_30yr_fixed"]].head())

#saves updated datasets
sold_with_rates.to_csv("sold_with_rates.csv", index = False)
listings_with_rates.to_csv("listings_with_rates.csv", index = False)