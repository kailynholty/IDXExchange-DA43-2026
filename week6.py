import pandas as pd
import geopandas as gpd

listings = pd.read_csv("listings_week4_5.csv", low_memory = False)
sold = pd.read_csv("sold_week4_5.csv", low_memory = False)

#convert to datetime
date_fields = ["CloseDate", "PurchaseContractDate", "ListingContractDate"]

for field in date_fields:
    if field in sold.columns:
        sold[field] = pd.to_datetime(sold[field])
    if field in listings.columns:
        listings[field] = pd.to_datetime(listings[field])

#creating engineered metrics
sold["PriceRatio"] = (sold["ClosePrice"] / sold["OriginalListPrice"])
sold["PricePerSqFt"] = (sold["ClosePrice"] / sold["LivingArea"])

sold["DaysOnMarketMetric"] = sold["DaysOnMarket"]
listings["DaysOnMarketMetric"] = sold["DaysOnMarket"]

sold["Year"] = sold["CloseDate"].dt.year
sold["Month"] = sold["CloseDate"].dt.month
sold["YrMo"] = sold["CloseDate"].dt.to_period("M")

listings["Year"] = listings["CloseDate"].dt.year
listings["Month"] = listings["CloseDate"].dt.month
listings["YrMo"] = listings["CloseDate"].dt.to_period("M")

sold["CloseOriginalListRatio"] = (sold["ClosePrice"] / sold["OriginalListPrice"])
sold["ListingContractDays"] = (sold["PurchaseContractDate"] - sold["ListingContractDate"])
sold["ContractCloseDays"] = (sold["CloseDate"] - sold["PurchaseContractDate"])

#preview engineered columns
print(sold[["ClosePrice", "OriginalListPrice", "LivingArea", "PriceRatio", "PricePerSqFt", "DaysOnMarketMetric",
            "YrMo", "ListingContractDays", "ContractCloseDays"]].head(3))

#adding school districts
schools = gpd.read_file("DistrictAreas2526_-284845464123469011.geojson")
schools = schools[schools["DistrictType"] == "Unified"]

sold_geo = gpd.GeoDataFrame(sold, geometry = gpd.points_from_xy(sold["Longitude"], sold["Latitude"]),
                            crs = "EPSG:4326")
listings_geo = gpd.GeoDataFrame(listings, geometry = gpd.points_from_xy(listings["Longitude"], listings["Latitude"]),
                            crs = "EPSG:4326")
schools = schools.to_crs(sold_geo.crs)

sold_school = gpd.sjoin(sold_geo, schools[["DistrictName", "geometry"]], how = "left", predicate = "within")
listings_school = gpd.sjoin(listings_geo, schools[["DistrictName", "geometry"]], how = "left", predicate = "within")

sold["DistrictName"] = sold_school["DistrictName"].values
listings["DistrictName"] = listings_school["DistrictName"].values

print("Sold unified school districts found:", sold["DistrictName"].nunique())
print("Listings unified school districts found:", listings["DistrictName"].nunique())

print("Sold properties with district assigned:", sold["DistrictName"].notna().sum())
print("Listing properties with district assigned:", listings["DistrictName"].notna().sum())

# Sold unified school districts found: 325
# Listings unified school districts found: 337
# Sold properties with district assigned: 170085
# Listing properties with district assigned: 379274

#segment analysis
property_summary = (sold.groupby("PropertyType").agg({
    "ClosePrice":["mean", "median"],
    "PriceRatio":["mean", "median"],
    "PricePerSqFt":["mean", "median"],
    "DaysOnMarketMetric":["mean", "median"],
    "ListingContractDays":["mean", "median"],
    "ContractCloseDays":["mean", "median"]
}))

county_summary = (sold.groupby("CountyOrParish").agg({
    "ClosePrice":["mean", "median"],
    "PriceRatio":["mean", "median"],
    "PricePerSqFt":["mean", "median"],
    "DaysOnMarketMetric":["mean", "median"],
    "ListingContractDays":["mean", "median"],
    "ContractCloseDays":["mean", "median"]
}))

#save to new csv
sold.to_csv("sold_week6", index = False)
listings.to_csv("listings_week6", index = False)
