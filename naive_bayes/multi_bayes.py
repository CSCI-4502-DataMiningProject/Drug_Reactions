import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics

# Read in Data
df = pd.read_csv('SAMPLE_demo_reac_outc.csv', sep=',')

# Clean and Preprocess
df['life_threatening_outcome'] = df.outc_cod.map({
    'LT': 1,
    'DE': 1,
    'OT': 0,
    'HO': 0,
    'RI': 0,
    'DS': 0 ,
    'CA': 0
})

df["country_cleaned"] = df.occr_country.map({
    'AU': 11,
    'CA': 6,
    'CH': 8,
    'CN': 5,
    'CO': 9,
    'DE': 4,
    'ES': 13,
    'GB': 3,
    'IT': 10,
    'JP': 7,
    'RO': 12,
    'TR': 2,
    'US': 1
})

def clean_weights(row):
    if row['wt_cod'] == 'KG':
        return row['wt']
    elif row['wt_cod'] == 'LBS':
        return row['wt'] / 2.2
    else:
        return None

df = df[pd.notnull(df['wt_cod'])]

df['weight_cleaned'] = df.apply(clean_weights, axis=1)

df = df[pd.notnull(df['sex'])]
df = df[pd.notnull(df['wt'])]
df = df[pd.notnull(df['weight_cleaned'])]
df = df[pd.notnull(df['occr_country'])]
df = df[pd.notnull(df['age'])]

# Remove outliers from age
age_q1 = df['age'].quantile(0.25)
age_q3 = df['age'].quantile(0.75)
boundary = 1.5 * (age_q3 - age_q1)
df = df[df['age'] < (age_q3 + boundary)]
df = df[df['age'] > (age_q1 - boundary)]

# Remove outliers from weight
weight_q1 = df['weight_cleaned'].quantile(0.25)
weight_q3 = df['weight_cleaned'].quantile(0.75)
boundary = 1.5 * (weight_q3 - weight_q1)
df = df[df['weight_cleaned'] < (weight_q3 + boundary)]
df = df[df['weight_cleaned'] > (weight_q1 - boundary)]

df['country_cleaned'] = df['country_cleaned'].fillna(14)

df['demo_gender'] = np.where(df["sex"] == "M",1,0)

df = df[[
    "demo_gender",
    "age",
    "wt",
    "wt_cod",
    "weight_cleaned",
    "country_cleaned",
    "life_threatening_outcome"
]]

df = df[pd.notnull(df['life_threatening_outcome'])]
df = df.reset_index()

# Prepare model
used_features =[
    "demo_gender",
    "age",
    "weight_cleaned",
    "country_cleaned"
]

features = df[used_features].values
labels = np.array(df["life_threatening_outcome"].values)

# Split into training and test sets
features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.4, random_state=1)

# Train Model
mnb = GaussianNB()
mnb.fit(features_train, labels_train)
labels_pred = mnb.predict(features_test)

# Print Report
print("GaussianNB model accuracy:", metrics.accuracy_score(labels_test, labels_pred)*100)

# Example Patient Profile
print("Given US male, 60 yrs old, 80kg:")
weight, age, is_male, country_int_code = 80, 60, 1, 1
input = [is_male, age, weight, country_int_code]
patient_prob = mnb.predict_proba([input])
print("% probability of serious outcome:", patient_prob[0][1]*100)
