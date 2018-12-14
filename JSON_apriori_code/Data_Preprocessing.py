'''
Anthony Olvera
CSCI 4502
Data Mining Project
Predicting Adverse Drug Reactions Based on Patient Demographics
JSON Preprocessing Script

This script is for pre-processing all JSON files residing in the directory 
specified below, it will processes each file and append the data to a data 
frame which will be exported as a csv to the same directory this script is 
ran in, this will take quite a while to run typically 6-8 hours depending on 
the machine its run on.   
'''
# Import all nessasary utilities
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import json
from os import listdir 
import gc 

# Load all the files in this directory
directory = 'G:/'

# count for progress
count = 0

# create inital datafrome
out_data = pd.DataFrame(columns=['patient.patientonsetage', 'patient.patientsex',	
                                 'patient.patientweight', 'primarysource.reportercountry',	
                                 'serious',	'transmissiondate',	'receivedate', 'drug_0',	
                                 'reaction_0', 'reaction_1', 'reaction_2'])

for filename in listdir(directory):
    if(filename != '$RECYCLE.BIN' and filename != 'System Volume Information'):
        filename = directory + filename
        count += 1
        print('Processing ', filename, 'number', count, 'of 788')
        data = json.load(open(filename))
        patient_info = json_normalize(data['results'])
        patient_info = pd.DataFrame(patient_info)

        # Most intersting attibutes include all patient related attributes, 
        # primary source, seriousness measures
        # and transmission information, all other attributes will be droped.

        patient_info = patient_info.drop(columns = ['companynumb', # if data exists
                                'fulfillexpeditecriteria',         # ignore errors if  
                                'primarysource','receiptdate',     # column is missing
                                'receiptdateformat', 'receivedateformat', 
                                'receiver', 'safetyreportid',
                                'sender.senderorganization',
                                'transmissiondateformat',
                                'patient.patientdeath.patientdeathdateformat',
                                'patient.patientonsetageunit','duplicate', 
                                'occurcountry', 'primarysourcecountry',
                                'receiver.receiverorganization', 
                                'receiver.receivertype',
                                'reportduplicate.duplicatenumb', 
                                'reportduplicate.duplicatesource',
                                'reporttype', 'safetyreportversion', 
                                'sender.sendertype' ], errors = 'ignore')

        # it can be seen that patient.drug and patient.reaction need to be expanded
        # create two new data frames for each attribute filter/reduce then merge with original 

        # create a new reaction dataframe
        data = []
        for row in range(len(patient_info['patient.reaction'])):
            reactions = []
            for list_index in range(len(patient_info['patient.reaction'][row])):
                reactions.append(patient_info['patient.reaction'][row][list_index].get('reactionmeddrapt'))
            data.append(reactions)
        reaction = pd.DataFrame(data)

        # create a new drug dataframe 
        data = []
        for row in range(len(patient_info['patient.drug'])):
            drugs = []
            for list_index in range(len(patient_info['patient.drug'][row])):
                drugs.append(patient_info['patient.drug'][row][list_index].get('medicinalproduct'))
            data.append(drugs)
        drug = pd.DataFrame(data)

        # give columns appropriate names  
        for column in reaction.columns:
            reaction = reaction.rename(columns = {column : 'reaction_' + str(column)})
    
        for column in drug.columns:
            drug = drug.rename(columns = {column : 'drug_' + str(column)})
    
        # Now drop the nested columns and merge with new dataframes
        patient_info = patient_info.drop(columns = ['patient.drug','patient.reaction'])
        patient_info = pd.concat([patient_info, drug, reaction], axis=1, join='inner')

        #some more column filtering
        patient_info = patient_info[['patient.patientonsetage',	'patient.patientsex',
                                      'patient.patientweight', 
                                      'primarysource.reportercountry','serious',
                                      'transmissiondate', 'receivedate','drug_0', 
                                      'reaction_0', 'reaction_1', 'reaction_2']]
        
        # convert age, weight and sex to numeric
        patient_info['patient.patientonsetage'] = pd.to_numeric(patient_info['patient.patientonsetage'])
        patient_info['patient.patientweight'] = pd.to_numeric(patient_info['patient.patientweight'])
        patient_info['patient.patientsex'] = pd.to_numeric(patient_info['patient.patientsex'])

        # convert all other attributes to the appropriate data type
        patient_info['primarysource.reportercountry'] = patient_info['primarysource.reportercountry'].astype(str)
        patient_info['serious'] = patient_info['serious'].astype(int)
        patient_info['transmissiondate'] = patient_info['transmissiondate'].astype(int)
        patient_info['receivedate'] = patient_info['receivedate'].astype(int)
        patient_info['drug_0'] = patient_info['drug_0'].astype(str)
        patient_info['reaction_0'] = patient_info['reaction_0'].astype(str)
        patient_info['reaction_1'] = patient_info['reaction_1'].astype(str)
        patient_info['reaction_2'] = patient_info['reaction_2'].astype(str)

        # Now eliminate outliers on age and weight
        age_q1 = patient_info['patient.patientonsetage'].quantile(0.25)
        age_q3 = patient_info['patient.patientonsetage'].quantile(0.75)
        age_IQR = age_q3 - age_q1
        weight_q1 = patient_info['patient.patientweight'].quantile(0.25)
        weight_q3 = patient_info['patient.patientweight'].quantile(0.75)
        weight_IQR = weight_q3 - weight_q1
        age_upperbound = age_q3 + 1.5*age_IQR
        age_lowerbound = age_q1 - 1.5*age_IQR
        weight_upperbound = weight_q3 + 1.5*weight_IQR
        weight_lowerbound = weight_q3 - 1.5*weight_IQR
        patient_info = patient_info.drop(
            patient_info[patient_info['patient.patientonsetage'] < age_lowerbound].index)
        patient_info = patient_info.drop(
            patient_info[patient_info['patient.patientonsetage'] > age_upperbound].index)
        patient_info = patient_info.drop(
            patient_info[patient_info['patient.patientweight'] < weight_lowerbound].index)
        patient_info = patient_info.drop(
            patient_info[patient_info['patient.patientweight'] > weight_upperbound].index)

        # convert weight in kilograms to weight in pounds
        patient_info['patient.patientweight'] = patient_info['patient.patientweight'] * 2.205

        # drop all rows with null patient demographic info 
        patient_info = patient_info.dropna(subset=['patient.patientonsetage', 
                                                    'patient.patientsex',
                                                    'patient.patientweight',])

        # drop rows with patientsex = 0 and rename to male and female
        patient_info = patient_info[patient_info['patient.patientsex'] != 0]
        patient_info.loc[(patient_info['patient.patientsex'] == 1), 
                                                'patient.patientsex'] = 'male'
        patient_info.loc[(patient_info['patient.patientsex'] == 2), 
                                                'patient.patientsex'] = 'female'

        # reset indexing from 0 through number of data objects
        patient_info = patient_info.reset_index(drop=True)

        # Discretize age and weight into 6 equal sized bins
        # Age: child, adolecent, young_adult, adult, senior, elderly
        # Weight: light, medium_light, medium, medium_heavy, heavy, very_heavy

        # Age
        patient_info['patient.patientonsetage'] = pd.cut(patient_info['patient.patientonsetage'], 6, 
                    labels = ['child','adolescent','young_adult','adult','senior','elderly'])
        # Weight
        patient_info['patient.patientweight'] = pd.cut(patient_info['patient.patientweight'], 6, 
                    labels = ['light','medium_light','medium','medium_heavy','heavy','very_heavy'])

        # append each processed file to existing data frame
        out_data = out_data.append(patient_info, ignore_index = True)

# export to a single csv file
out_data.to_csv('patient_info.csv')