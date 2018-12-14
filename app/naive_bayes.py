import pandas as pd
import pdb
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

COUNTRY_OPTS = {
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
}

OUTCOME_OPTS = {
    'LT': 1,
    'DE': 1,
    'OT': 0,
    'HO': 0,
    'RI': 0,
    'DS': 0 ,
    'CA': 0
}

class nbayes:
    def __init__(self):
        self.data_file = open('app/SAMPLE_demo_reac_outc.csv')
        self.df = pd.read_csv(self.data_file, sep=',')
        self.data_file.close()
        self.mnb = MultinomialNB()
        self.clean_data()
        self.remove_nulls()
        self.prepare_dataframe()
        self.prepare_model()

    def clean_data(self):
        self.df['life_threatening_outcome'] = self.df.outc_cod.map(COUNTRY_OPTS)
        self.df["country_cleaned"] = self.df.occr_country.map(OUTCOME_OPTS)

    def remove_nulls(self):
        self.df = self.df[pd.notnull(self.df['wt_cod'])]
        self.df = self.df[pd.notnull(self.df['sex'])]
        self.df = self.df[pd.notnull(self.df['wt'])]
        self.df = self.df[pd.notnull(self.df['occr_country'])]
        self.df = self.df[pd.notnull(self.df['age'])]
        self.df = self.df[self.df['age'] < 120]
        self.df = self.df[self.df['age'] > 0]

    def prepare_dataframe(self):
        self.df['weight_cleaned'] = self.df.apply(self.clean_weights, axis=1)
        self.df = self.df[pd.notnull(self.df['weight_cleaned'])]
        self.df = self.df[self.df['weight_cleaned'] < 500]
        self.df = self.df[self.df['weight_cleaned'] > 0]
        self.df['country_cleaned'] = self.df['country_cleaned'].fillna(14)
        self.df['binned_age'] = self.df['age'].values.round(-1)
        self.df['binned_weight'] = self.df['wt'].values.round(-1)
        self.df['demo_gender'] = np.where(self.df["sex"] == "M",1,0)

        self.df = self.df[[
            "demo_gender",
            "age",
            "wt",
            "wt_cod",
            "binned_weight",
            "binned_age",
            "country_cleaned",
            "life_threatening_outcome"
        ]]

        self.df = self.df[pd.notnull(self.df['life_threatening_outcome'])]
        self.df = self.df.reset_index()

    def prepare_model(self):
        features =[
            "demo_gender",
            "binned_age",
            "binned_weight",
            "country_cleaned"
        ]

        X = self.df[features].values
        Y = np.array(self.df["life_threatening_outcome"].values)

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.4, random_state=1)
        self.mnb.fit(X_train, Y_train)

    def calculate(self, age, weight, is_male, country):
        if is_male:
            is_male = 1
        else:
            is_male = 0

        arr = [1, 60, 70, 14]
        # arr = [is_male, age, weight, country]
        prob = self.mnb.predict_proba([arr])
        print(prob)
        print("Prob of serious outcome (in %):", prob[0][1]*100)
        return prob[0][1]*100

    def clean_weights(self, row):
        if row['wt_cod'] == 'KG':
            return row['wt']
        elif row['wt_cod'] == 'LBS':
            return row['wt'] / 2.2
        else:
            return None
