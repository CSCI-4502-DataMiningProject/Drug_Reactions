import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB
from sklearn import metrics

# Read in Data
df = pd.read_csv('SAMPLE_demo_reac_outc.csv', sep=',')

# Clean and Preprocess
# Code values as binary options
df['life_threatening_outcome'] = df.outc_cod.map({
    'LT': 1,
    'DE': 1,
    'OT': 0,
    'HO': 0,
    'RI': 0,
    'DS': 0 ,
    'CA': 0
})

df["in_US"] = df.occr_country.map({'US': 1})
df['in_US'] = df['in_US'].fillna(0)

df = df[pd.notnull(df['sex'])]
df['demo_gender'] = np.where(df["sex"] == "M", 1, 0)

df = df[[
    "demo_gender",
    "in_US",
    "life_threatening_outcome"
]]

df = df[pd.notnull(df['life_threatening_outcome'])]
df = df.reset_index()

# Prepare model
features =[
    "demo_gender",
    "in_US"
]

features = df[features].values
labels = np.array(df["life_threatening_outcome"].values)

# Split into training and test sets
features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.4, random_state=1)

mnb = BernoulliNB()
mnb.fit(features_train, labels_train)

labels_pred = mnb.predict(features_test)

# Report
print("BernoulliNB model accuracy:", metrics.accuracy_score(labels_test, labels_pred)*100)

# Example profiles
us_male       = [1,1]
non_us_male   = [1,0]
us_female     = [0,1]
non_us_female = [0,0]

us_male_prob = mnb.predict_proba([us_male])
non_us_male_prob = mnb.predict_proba([non_us_male])
us_female_prob = mnb.predict_proba([us_female])
non_us_female_prob = mnb.predict_proba([non_us_female])

print("Prob of a MALE US serious outcome (in %):", us_male_prob[0][1]*100)
print("Prob of MALE NON US serious outcome (in %):", non_us_male_prob[0][1]*100)
print("Prob of FEMALE US serious outcome (in %):", us_female_prob[0][1]*100)
print("Prob of FEMALE NON US serious outcome (in %):", non_us_female_prob[0][1]*100)
