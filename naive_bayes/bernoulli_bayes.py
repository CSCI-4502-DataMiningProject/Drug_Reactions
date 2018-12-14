import pandas as pd
import pdb
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn import metrics

# Read in Data
df = pd.read_csv('FINAL_demo_reac_outc.csv', sep=',')

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

df["in_US"] = df.occr_country.map({
    'US': 1
})

df['in_US'] = df['in_US'].fillna(0)

df = df[pd.notnull(df['sex'])]
df['demo_gender'] = np.where(df["sex"] == "M",1,0)

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

X = df[features].values
Y = np.array(df["life_threatening_outcome"].values)

# Split Data into training sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.4, random_state=1)

mnb = BernoulliNB()
mnb.fit(X_train, Y_train)

Y_pred = mnb.predict(X_test)

# Print Report
print("Multinomial Naive Bayes model accuracy(in %):", metrics.accuracy_score(Y_test, Y_pred)*100)

us_male = [1,1]
non_us_male = [1,0]
us_female = [0,1]
non_us_female = [0,0]

prob1 = mnb.predict_proba([us_male])
prob2 = mnb.predict_proba([non_us_male])
prob3 = mnb.predict_proba([us_female])
prob4 = mnb.predict_proba([non_us_female])

print("Prob of a MALE US serious outcome (in %):", prob1[0][1]*100)
print("Prob of MALE NON US serious outcome (in %):", prob2[0][1]*100)
print("Prob of FEMALE US serious outcome (in %):", prob3[0][1]*100)
print("Prob of FEMALE NON US serious outcome (in %):", prob4[0][1]*100)
