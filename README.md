# Drug_Reactions
This repository is for data and code related to group2's CSCI 4502 data mining project for fall of 2018.

# Database Information

The FAERS database files are located here:
http://data.nber.org/fda/faers/

We have downloaded all the files for Q1 2016 through Q1 2018, and loaded them into a Postgresql relational database. The schema for this database is located in `db/schema.sql`

There are 7 tables:

- indi - 7,901,564 records
- outc - 2,122,914 records
- reac - 9,007,602 records
- rpsr - 113,657 records
- ther - 4,200,330 records
- demo - 3,088,728 records
- drug - 11,312,890 records

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
