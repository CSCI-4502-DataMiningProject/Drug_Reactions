import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import math
import numbers

# - Generates a stacked bar chart
# - Shows life threatening outcome reports vs other serious outcome reports by country
# - Data is from FAERS database between 2016 Q1 - 2018 Q1
# - Subset sample CSV used for testing

csv_file = pd.read_csv('SAMPLE2_distinct_demo_reac_outc_drug.csv')

country_counts = {}
for index, row in csv_file.iterrows():
    country_code = row['occr_country']
    if isinstance(country_code, numbers.Number) and math.isnan(country_code):
        continue

    if country_code not in country_counts:
        country_counts[country_code] = { "SERIOUS": 0, "OTHER": 0 }

    outcome = row['outc_cod']
    if outcome == "LT" or outcome == "DE":
        country_counts[country_code]["SERIOUS"] += 1
    else:
        country_counts[country_code]["OTHER"] += 1


country_labels = []
outc_dict = { "SERIOUS": [], "OTHER": [] }

for country_code in country_counts:
    country_labels.append(country_code)
    for outcome in country_counts[country_code]:
        outc_dict[outcome].append(country_counts[country_code][outcome])

N = len(country_labels)

SERIOUS = outc_dict["SERIOUS"]
OTHER = outc_dict["OTHER"]

ind = np.arange(N)
p1 = plt.bar(ind, SERIOUS)
p2 = plt.bar(ind, OTHER, bottom=SERIOUS)

plt.xticks(ind, country_labels, rotation=90)
plt.title("Life Threatening vs. Serious Outcome Reports by Country")
plt.xlabel("Country")
plt.ylabel("Adverse Outcome Count")
plt.legend(("Death/Life Threatening Outcome", "Other Serious Outcome"))

plt.show()
