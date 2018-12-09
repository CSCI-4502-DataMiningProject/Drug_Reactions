import pandas as pd
import pdb
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

# Read in Data
df = pd.read_csv('SAMPLE_demo_reac_outc.csv', sep=',')

# Clean and Preprocess
df['life_threatening_outcome'] = df.outc_cod.map({'LT': 1, 'DE': 1, 'OT': 0, 'HO': 0, 'RI': 0, 'DS': 0 , 'CA': 0 })

df["country_cleaned"] = df.occr_country.map({
    'AU': 11, 'CA': 6, 'CH': 8, 'CN': 5, 'CO': 9, 'DE': 4, 'ES': 13, 'GB': 3, "IT": 10, "JP": 7, "RO": 12, "TR": 2, "US": 1
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
df = df[df['age'] < 120]
df = df[df['age'] > 0]
df = df[df['weight_cleaned'] < 500]
df = df[df['weight_cleaned'] > 0]
df['country_cleaned'] = df['country_cleaned'].fillna(14)

df['binned_age'] = df['age'].values.round(-1)
df['binned_weight'] = df['wt'].values.round(-1)

df['demo_gender'] = np.where(df["sex"] == "M",1,0)

df = df[[
    "demo_gender",
    "age",
    "wt",
    "wt_cod",
    "binned_weight",
    "binned_age",
    "country_cleaned",
    "life_threatening_outcome"
]]

df = df[pd.notnull(df['life_threatening_outcome'])]
df = df.reset_index()

# Prepare model
used_features =[
    "demo_gender",
    "binned_age",
    "binned_weight",
    "country_cleaned"
]

X = df[used_features].values
Y = np.array(df["life_threatening_outcome"].values)

# Split Data into training sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.4, random_state=1)

# Initialize and train model
mnb = MultinomialNB()
mnb.fit(X_train, Y_train)

Y_pred = mnb.predict(X_test)

# Print Report
print(df.groupby('life_threatening_outcome').size())
print(df.groupby('demo_gender').size())

print("Multinomial Naive Bayes model accuracy(in %):", metrics.accuracy_score(Y_test, Y_pred)*100)

print("Given male, 60, 70kg, US, probability of a serious outcome:")
male = [1, 60, 70, 14]
prob = mnb.predict_proba([male])
print(prob)
print("Prob of serious outcome (in %):", prob[0][1]*100)
