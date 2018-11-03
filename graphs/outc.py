import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# - Generates a temporal graph of outcomes broken out by type
# - Data is from FAERS database between 2016 Q1 - 2018 Q1
# - Sample CSV used for testing

csv_file = pd.read_csv('outcomes_final.csv')

dict = { "CA": [], "DE": [], "DS": [], "HO": [], "LT": [], "OT": [], "RI": [] }
for index, row in csv_file.iterrows():
    for code in ["CA", "DE", "DS", "HO", "LT", "OT", "RI"]:
        if row['outcome code'] == code:
            dict[code].append((datetime.datetime.strptime(row['date_formatted'], "%m/%d/%Y").date(), row['count']))

label_dict = { "CA": "Congenital Anomaly", "DE": "Death", "DS": "Disability", "HO": "Hospitalization", "LT": "Life Threatening", "OT": "Other Serious Event", "RI": "Required Intervention To Prevent Permanent Damage" }

for code in ["CA", "DE", "DS", "HO", "LT", "OT", "RI"]:
    x = [tup[0] for tup in dict[code]]
    y = [tup[1] for tup in dict[code]]
    x2,y2 = zip(*sorted(zip(x,y),key=lambda x: x[0]))
    plt.plot(x2,y2, label=label_dict[code])

plt.xlabel('Time')
plt.ylabel('Number of Outcomes')
plt.title("FAERS Outcomes By Type Over Time")
plt.legend(title='Outcome Types')
plt.show()
