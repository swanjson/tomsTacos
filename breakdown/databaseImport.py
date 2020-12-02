import duckdb
import csv
import pandas as pd 


# starts the database in default memory
con = duckdb.connect(database=':memory:', read_only=False)

# initiates the pandas df loaded from the saved csv file
df = pd.read_csv('rankedCSV.csv')

# registers the df and selects
con.register('df_view', df)
con.execute('SELECT * FROM df_view')
con.fetchall()

#creates the SQL table from the registered pandas dataframe
con.execute('CREATE TABLE df_table AS SELECT * FROM df_view')

# fetches the created dataframe and converts it to a python readable?
dfEX = con.execute('SELECT * FROM df_table').fetchdf()
print(dfEX)










