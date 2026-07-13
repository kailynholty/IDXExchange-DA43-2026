import pandas as pd

listings = pd.read_csv("listings.csv", low_memory = False)
sold = pd.read_csv("sold.csv", low_memory = False)

#finds the total number of rows and columns in the Listings and Sold datasets
print("Listings: " + str(listings.shape[0]) + " rows x " + str(listings.shape[1]) + " columns")
print("Sold: " + str(sold.shape[0]) + " rows x " + str(sold.shape[1]) + " columns")

#finds column data types for the Listings and Sold datasets
print("\n--- Listings Column Data Types ---")
print(listings.dtypes)

print("\n--- Sold Column Data Types ---")
print(sold.dtypes)

#shows the first couple rows of the Listings and Sold datasets
print("\n--- Listings Preview ---")
print(listings.head(2))

print("\n--- Sold Preview ---")
print(sold.head(2))

#function to create a report of columns with missing values >90%
def missing_value_report(df, dataset_name):
    total_rows = len(df)
    missing_count = df.isnull().sum()
    missing_percent = (missing_count / total_rows * 100 ).round(2)

    report = pd.DataFrame({"Missing Count": missing_count, "Missing Percent": missing_percent})
    report = report[report["Missing Count"] > 0]
    report = report.sort_values("Missing Percent", ascending = False)
    report["flag_90percent"] = report["Missing Percent"] > 90

    print("\n---" + dataset_name + " Missing Value Report ---")
    print("Total Number of Columns with Missing Values: " + str(len(report)))
    print("Columns with >90% Missing Values: " + str(report["flag_90percent"].sum()))
    print(report.head(15))

    return report

#creates reports for listings and sold files on columns with missing values
listings_missing = missing_value_report(listings, "Listings")
sold_missing = missing_value_report(sold, "Sold")

#drops columns with >90% missing values and creates new cleaned datasets
listings_columns_drop = listings_missing[listings_missing["Missing Percent"] > 90].index
listings_cleaned = listings.drop(columns = listings_columns_drop)
listings_cleaned.to_csv("listings_cleaned.csv", index = False)

#Listings Columns Dropped:
#                              Missing Count  Missing Percent  flag_90percent
#FireplacesTotal                      572122           100.00            True
#TaxYear                              572122           100.00            True
#TaxAnnualAmount                      572122           100.00            True
#CoveredSpaces                        572122           100.00            True
#BusinessType                         572122           100.00            True
#MiddleOrJuniorSchoolDistrict         572122           100.00            True
#AboveGradeFinishedArea               572122           100.00            True
#ElementarySchoolDistrict             572122           100.00            True
#BelowGradeFinishedArea               568835            99.43            True
#CoBuyerAgentFirstName                555696            97.13            True
#BuilderName                          545587            95.36            True
#LotSizeDimensions                    542223            94.77            True
#BuildingAreaTotal                    521643            91.18            True

sold_columns_drop = sold_missing[sold_missing["Missing Percent"] > 90].index
sold_cleaned = sold.drop(columns = sold_columns_drop)
sold_cleaned.to_csv("sold_cleaned.csv", index = False)

#Sold Columns Dropped:
#                              Missing Count  Missing Percent  flag_90percent
#BusinessType                         491086           100.00            True
#CoveredSpaces                        491086           100.00            True
#TaxAnnualAmount                      491086           100.00            True
#TaxYear                              491086           100.00            True
#ElementarySchoolDistrict             491086           100.00            True
#FireplacesTotal                      491086           100.00            True
#AboveGradeFinishedArea               491086           100.00            True
#MiddleOrJuniorSchoolDistrict         491086           100.00            True
#WaterfrontYN                         490773            99.94            True
#BelowGradeFinishedArea               488248            99.42            True
#BasementYN                           481524            98.05            True
#LotSizeDimensions                    467385            95.17            True
#BuilderName                          466864            95.07            True
#BuildingAreaTotal                    456773            93.01            True
#CoBuyerAgentFirstName                446159            90.85            True

#review numeric fields for statistical relevance
numeric_fields = ["ClosePrice", "ListPrice", "OriginalListPrice", "LivingArea", "LotSizeAcres",
                  "BedroomsTotal", "BathroomsTotalInteger", "DaysOnMarket", "YearBuilt"]

#function to create a statistic summary of each numeric field
def numeric_summary(df, field_name):
    print("\n---" + field_name + " Distribution Summary ---")
    print("Minimum:" + str(df[field_name].min()))
    print("Maximum:" + str(df[field_name].max()))
    print("Mean:" + str(df[field_name].mean()))
    print("Median:" + str(df[field_name].median()))
    print("Percentiles:" + str(df[field_name].quantile([0.25, 0.5, 0.75])))

#creates a report for listings and sold statistic summary of each numeric field
for field in numeric_fields:
    numeric_summary(sold, field)

for field in numeric_fields:
    numeric_summary(listings, field)

#determines counties with the highest medians
county_medians = sold.groupby("CountyOrParish")["ClosePrice"].median()
county_medians = county_medians.sort_values(ascending = False)
print(county_medians.head(5))
