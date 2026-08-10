import pandas as pd

listings = pd.read_csv("listings_week6", low_memory = False)
sold = pd.read_csv("sold_week6", low_memory = False)

#identify IQR outliers
def iqr_bounds(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    return lower, upper

lower, upper = iqr_bounds(sold, "ClosePrice")
print("Close Price Sold lower bound: ", lower)
print("Close Price Sold upper bound: ", upper)

lower, upper = iqr_bounds(listings, "ClosePrice")
print("Close Price Listings lower bound: ", lower)
print("Close Price Listings upper bound: ", upper)

lower, upper = iqr_bounds(sold, "LivingArea")
print("Living Area Sold lower bound: ", lower)
print("Living Area Sold upper bound: ", upper)

lower, upper = iqr_bounds(listings, "LivingArea")
print("Living Area Listings lower bound: ", lower)
print("Living Area Listings upper bound: ", upper)

lower, upper = iqr_bounds(sold, "DaysOnMarket")
print("Days On Market Sold lower bound: ", lower)
print("Days On Market Sold upper bound: ", upper)

lower, upper = iqr_bounds(listings, "DaysOnMarket")
print("Days On Market Listings lower bound: ", lower)
print("Days On Market Listings upper bound: ", upper)


#create an outlier flag column
for column in ["ClosePrice", "LivingArea", "DaysOnMarket"]:
    lower, upper = iqr_bounds(sold, column)

    sold[str(column) + "_sold_outlier_flag"] = ((sold[column] < lower) | (sold[column] > upper))

for column in ["ClosePrice", "LivingArea", "DaysOnMarket"]:
    lower, upper = iqr_bounds(listings, column)

    listings[str(column) + "_listings_outlier_flag"] = ((listings[column] < lower) | (listings[column] > upper))


#print number of outliers
print("Close Price Sold outliers: " + str(sold["ClosePrice_sold_outlier_flag"].sum()))
print("Living Area Sold outliers: " + str(sold["LivingArea_sold_outlier_flag"].sum()))
print("Days On Market Sold outliers: " + str(sold["DaysOnMarket_sold_outlier_flag"].sum()))

print("Close Price Listings outliers: " + str(listings["ClosePrice_listings_outlier_flag"].sum()))
print("Living Area Listings outliers: " + str(listings["LivingArea_listings_outlier_flag"].sum()))
print("Days On Market Listings outliers: " + str(listings["DaysOnMarket_listings_outlier_flag"].sum()))

#save flagged csv file
sold.to_csv("sold_flagged_outliers.csv", index = False)
listings.to_csv("listings_flagged_outliers.csv", index = False)

#filter dataset of outliers
sold_clean = sold[(sold["ClosePrice_sold_outlier_flag"] == False) &
                  (sold["LivingArea_sold_outlier_flag"] == False) &
                  (sold["DaysOnMarket_sold_outlier_flag"] == False)].copy()

listings_clean = listings[(listings["ClosePrice_listings_outlier_flag"] == False) &
                          (listings["LivingArea_listings_outlier_flag"] == False) &
                          (listings["DaysOnMarket_listings_outlier_flag"] == False)].copy()

#compare dataset size before and after filtering
print("Sold Rows before filtering: " + str(len(sold)))
print("Sold Rows after filtering: " + str(len(sold_clean)))

print("Listings Rows before filtering: " + str(len(listings)))
print("Listings Rows after filtering: " + str(len(listings_clean)))

#compare median values before and after filtering
for column in ["ClosePrice", "LivingArea", "DaysOnMarket"]:
    print(column, "before:", sold[column].median())
    print(column, "after:", sold_clean[column].median())

for column in ["ClosePrice", "LivingArea", "DaysOnMarket"]:
    print(column, "before:", listings[column].median())
    print(column, "after:", listings_clean[column].median())

#save cleaned and filtered dataset
sold_clean.to_csv("sold_filtered_outliers.csv", index = False)
listings_clean.to_csv("listings_filtered_outliers.csv", index = False)