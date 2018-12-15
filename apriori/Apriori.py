'''
Anthony Olvera
CSCI 4502
Data Mining Project
Predicting Adverse Drug Reactions Based on Patient Demographics
Apriori Algorithm Implementation

This script will run the apriori algorithm on the preprocessed file 
patient_info.csv generated by Data_Preprocessing.py script.
'''

# Import all nessasary utilities
import numpy as np
import pandas as pd
#import scipy.stats as stats

# Import the file
patient_info = pd.read_csv('patient_info.csv')

# Implement the apriori algorithm

# Experiment with this value
min_support = 0.1

def create_C1(data_frame): # function to create 1 itemset of each distinct data entry
    C1 = []                # this step takes the longest may be wise to write to a file
    for row in data_frame.index: # loop over each row in the data frame
        print('processing row', row, 'of', len(data_frame.index))
        for column_value in data_frame.iloc[[row]]: # loop over each entry per row
            if(not [data_frame.iloc[row][column_value]] in C1): # in data not already in set  
                C1.append([data_frame.iloc[row][column_value]]) # then add it
    return list(map(frozenset, C1)) #use frozen set so we can use it as a key in a dict

def scan_data(data_frame, Ck, min_support): # function to run succesive scans of the data
    ssCnt = {}
    data_frame = list(map(set, data_frame.as_matrix()))
    for row in data_frame: # loop over each data object
        for candidate in Ck:
            if candidate.issubset(row):
                if not candidate in ssCnt:
                    ssCnt[candidate] = 1
                else:
                    ssCnt[candidate] += 1
    num_items = float(len(data_frame))
    ret_list = []
    support_data = {}
    for key in ssCnt:
        support = ssCnt[key] / num_items
        if support >= min_support:
            ret_list.insert(0, key)
        support_data[key] = support
    return ret_list, support_data

def apriori_gen(Fk, k): # generate next successive candidate set of size k
    candidate_set = []  # helper funtion for main function below 
    for i in range(len(Fk)): # loop over current frequent itemset Fk 
        for j in range(i+1, len(Fk)):  
            F1 = list(Fk[i])[:k-2] 
            F2 = list(Fk[j])[:k-2]
            if F1 == F2: # if first k-2 elements are equal
                candidate_set.append(Fk[i] | Fk[j]) # set union
    return candidate_set

def apriori(data_frame, min_support): # returns all frequent itemsets that meet the minimum support
    C1 = create_C1(data_frame) # create itemset of all unique data 
    F1, sup_data = scan_data(data_frame, C1, min_support) # call scan_data on C1
    F = [F1]
    k = 2
    while (len(F[k-2]) > 0):
        Ck = apriori_gen(F[k-2], k)
        Fk, sup_k = scan_data(data_frame, Ck, min_support) # scan DB to get Fk
        sup_data.update(sup_k)
        F.append(Fk)
        k += 1
    return F, sup_data

F2, sup_data2 = apriori(patient_info, 0.2)
F1, sup_data1 = apriori(patient_info, 0.1)
F07, sup_data07 = apriori(patient_info, 0.07)
F05, sup_data05 = apriori(patient_info, 0.05)
F03, sup_data03 = apriori(patient_info, 0.03)
F01, sup_data01 = apriori(patient_info, 0.01)

# flatten the lists
F2 = [item for sublist in F2 for item in sublist]
F1 = [item for sublist in F1 for item in sublist]
F07 = [item for sublist in F07 for item in sublist]
F05 = [item for sublist in F05 for item in sublist]
F03 = [item for sublist in F03 for item in sublist]
F01 = [item for sublist in F01 for item in sublist]


# No need to keep subset of previous itemset
F2 = sorted(F2, key = len)
F1 = np.setdiff1d(F1, F2, assume_unique = True)
F1 = sorted(F1, key = len)
F07 = list(set(F07) - set(F1) - set(F2))
F07 = sorted(F07, key = len)
F05 = list(set(F05) - set(F07) - set(F1) - set(F2))
F05 = sorted(F05, key = len)
F03 = list(set(F03) - set(F05) - set(F07) - set(F1) - set(F2))
F03 = sorted(F03, key = len)
F01 = list(set(F01) - set(F03) - set(F05) - set(F07) - set(F1) - set(F2))
F01 = sorted(F01, key = len)

print('All Itemsets Have Been Generated')

# print the data
print('F2 is', F2)
print('F1 is', F1)
print('F07 is', F07)
print('F05 is', F05)
print('F03 is', F03)
print('F01 is', F01)
print('sup_data2 is', sup_data2)
print('sup_data1 is', sup_data1)
print('sup_data07 is', sup_data07)
print('sup_data05 is', sup_data05)
print('sup_data03 is', sup_data03)
print('sup_data01 is', sup_data01)

# print data line by line for ease of analysis
for item in F01: # change as needed
    print(str(item)+',')

# calculate confidence for association rules
def confidence(data_frame, attribute_A, attribute_B):
    a_count = 0
    banda_count = 0
    for row in data_frame.index:
        a_inrow = False
        b_inrow = False
        for column_value in data_frame.iloc[[row]]:
            #print(data_frame.iloc[row][column_value])
            if(data_frame.iloc[row][column_value] == attribute_A):
                a_count+=1
                a_inrow = True
            if(data_frame.iloc[row][column_value] == attribute_B):
                b_inrow = True
        if(a_inrow and b_inrow):
            banda_count+=1
    return(banda_count/a_count)
            
# check confidence of given association a->b(sup, conf), change as needed
print(confidence(patient_info, 'INSOMNIA', 'DRUG INEFFECTIVE'))

# search for support data,  change as needed
print(sup_data01.get(frozenset({'DRUG INEFFECTIVE', 'INSOMNIA'})))     