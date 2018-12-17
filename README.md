# Drug_Reactions
This repository is for data and code related to group2's CSCI 4502 data mining project for fall of 2018.

## Project Code and Description
### Project Title
Predicting Adverse Drug Reactions Based on Patient Demographics

### Team Members
Annie Lydens and Anthony Olvera

### Description of the Project
This project analyzed the FDA FAERS data set, specifically examining links between various demographic attributes or drug characteristics and subsequent adverse outcomes. We set out to find interesting correlations and relationships between demographic characteristics and their likelihood of having an adverse drug reaction. We also sought to resolve whether there are pairs of frequently occurring sets of specific patient demographic attributes. In addition, we also paired sets of common multiple reactions with certain medications which tend to occur together in the treatment process.

### Summary of Questions Sought & Answers
We sought to answer the following questions in our research:
- Given a patient’s demographic information (age, sex, weight, reported location), can we predict the likelihood of a significant medical outcome?
- What are the most common set of patient characteristics and adverse drug reactions?
- Do certain medical reactions occur together frequently? If so, what are those reactions?  

In the course of our research, we found specific patient profiles that had a higher predicted probability of having a life-threatening reaction after taking a drug. Older men outside of the US tended to have a higher likelihood of serious, life-threatening adverse reactions. Of the profiles we examined, older Italian men were the most likely to experience life threatening reactions, while younger women were the least likely, with a predicted probability of life threatening reactions at around half of their elderly male counterparts'.

We also found that among all adverse reactions, the most common is that drug used for treatment being ineffective. The most common patient demographic paired with drug reactions are the drug ineffectiveness among females as well as drug ineffectiveness among individuals in the US. Lastly, the most frequent combination of drug and reaction found together is drug ineffectiveness and the drug Lunesta. The most common pair of reactions is drug ineffectiveness and insomnia.

### Applications

Our research could help reduce adverse drug reactions by bringing awareness to common adverse reactions that occur together. Knowing common pairs of reactions from specific drugs could help physicians and other medical professionals prepare patients for treatment, as well as make more educated treatment decisions.

Additionally, this research could be beneficial for medical staff and pharmaceutical companies in allowing them to develop a more nuanced understanding of previously unidentified demographic factors that may contribute to adverse reactions in patients. It could also help identify groups of patients who may have previously been considered low-risk for a life-threatening outcome, and correctly reclassify them as higher risk.

An interesting software application of this research could be to build a web application that allows medical professionals to either enter patient demographic characteristics and view the patient's predicted probability of a life-threatening outcome, or input drugs or adverse reactions and see common co-occurring reactions.

### Final Paper
[Final Paper is available here](/02_DrugReactionPrediction_Part4.pdf)

### Video Presentation
[Video is available here](/02_DrugReactionPrediction_Part6_Video.mp4)

# Database Information

The FAERS database files are located here:
http://data.nber.org/fda/faers/

We have downloaded all the files for Q1 2016 through Q1 2018, and loaded them into a Postgresql relational database. The schema for this database is located in `db/schema.sql`

There are 7 tables:

- indi (indications) - 7,901,564 records
- outc (outcomes) - 2,122,914 records
- reac (reactions/adverse events) - 9,007,602 records
- rpsr (report sources) - 113,657 records
- ther (drug therapy start/end dates) - 4,200,330 records
- demo (patient demographic information) - 3,088,728 records
- drug (drug/biologic information) - 11,312,890 records

We have created a gzipped database you can use to recreate the database on your own machine. This database has not yet undergone data cleaning, so there may be duplicate records. The gzipped file is 448 MB.

#### Steps to create the DB
1. Install Postgresql if you do not already have it.

2. Create a database named `faers` by running the following on the command line:
```createdb faers```

3. Download the `faersdb.gz` file. You can [download it here](https://drive.google.com/file/d/198NkzdTuvAOdGDbFzPGY8Vv0JoWvGZvi/view?usp=sharing). (Click "Download".)

3. Unzip the `faersdb.gz` file and dump it into the db by running the following on the command line inside the directory where you downloaded the file:
```gunzip -c faersdb.gz | psql faers```

This may take a while. Just let it do its thing.

You should see output similar to the following image. You can check final counts to verify that the database was recreated successfully.

<img src="/docs/db-restore.png" alt="DB Restore output" height="500">

#### Other Helpful Commands

Drop into psql console:

```psql```

Drop into psql console within faers database:

```psql -d faers```

You can then write SQL as you normally would.

Clear a table (in psql console within faers db):

```delete from indi;```

Drop database (in psql console):
```DROP DATABASE faers;```
