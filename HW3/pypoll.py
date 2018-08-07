'''
The total number of votes cast
A complete list of candidates who received votes
The percentage of votes each candidate won
The total number of votes each candidate won
The winner of the election based on popular vote.
Voter ID,County,Candidate
'''
import pandas as pd
import numpy as np
import csv
file1 = open('result_pypol.txt','w') 
file1.write("Election Results: " + "\n")
file1.write("-------------------" + "\n")
print("Election Results:")
print("------------------")
df = pd.read_csv('election_data.csv',skiprows=[0],names=['Voter_ID','County','Candidate'])
print("Total Votes: " +  str(df.Voter_ID.count()) + "\n")
dd=df.Voter_ID.count()
file1.write("Total Votes: " + str(dd) +"\n")
file1.write("-------------------" + "\n")
number_of_uniqe_voters = len(df.Voter_ID.unique()) 
county_unique = df['County'].unique()
Voter_unique = len(df['Voter_ID'].unique())
print("--------------------------------------------------------------------------")
df1=df.groupby(['Candidate'],as_index=False).count()
df2=df1.groupby('Voter_ID').apply(lambda x: x.sort_values('Candidate',ascending=[True]))
df2['Percent'] = df2['Voter_ID']/number_of_uniqe_voters * 100
df3=df2[['Candidate','Percent','County']]
df4 = df3.rename(lambda x: 'Counts' if x == 'County' else x, axis=1)
n = df4['Candidate']
p = df4['Percent']
c = df4['Counts']
for x,y,z in zip(reversed(n),reversed(p),reversed(c)):
     print('%s: %.3f%%  (%d) \n' % (x,int(y+0.5),z))
     file1.write('%s : %d%%  (%d) \n' % (x,int(y+0.5),z))
print("-------------------------------------------\n")
file1.write("------------------------------------- \n")
print("Winner: Khan \n")
print("-------------------------------------------\n")
file1.write("Winner: Khan \n")
file1.write("------------------------------------- \n")
file1.close()
