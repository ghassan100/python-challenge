
import pandas as pd
import numpy as np
file1 = open('result_pybank.txt','w') 
df = pd.read_csv('budget_data.csv',names=['Date','Revenue'],skiprows=[0])
dd=df.count()
a=dd[1]

df.Date = df.Date.str.replace('-','-20')
def positive(value):
    return max(value, 0)

def negative(value):
    return min(value, 0)

df["Positive"] = df["Revenue"].map(positive)
df["Negative"] = df["Revenue"].map(negative)
Total = df['Positive'].sum()

maxy=df['Revenue'].max()    
locmax=df.loc[df['Revenue'].idxmax()]
locmin=df.loc[df['Revenue'].idxmin()]

miny=df['Revenue'].min()
maxmax=df[df['Revenue']==maxy]['Date']
minmin=df[df['Revenue']==miny]['Date']
average=Total/a

print("Finiancial Analysis: " + "\n")
print("-------------------" + "\n")
print("Total Months: " + str(a) +"\n")
print("Total: " + "$"+str(Total)+"\n")
print("Average Change: " + "$"+str(average) +"\n")
print("Greatest Increase in Profit: " +str(maxmax.iloc[0])+ "  " + "($"+str(maxy)+")" +"\n")
print("Greatest Derease in Profit:  " +str(minmin.iloc[0])+ "  " + "($"+str(miny)+")" +"\n")
print("-------------------" + "\n")

file1.write("Finiancial Analysis: " + "\n")
file1.write("-------------------" + "\n")
file1.write("Total Months: " + str(a) +"\n")
file1.write("Total: " + "$"+str(Total)+"\n")
file1.write("Average Change: " + "$"+str(average) +"\n")
file1.write("Greatest Increase in Profit: " +str(maxmax.iloc[0])+ "  " + "($"+str(maxy)+")" +"\n")
file1.write("Greatest Derease in Profit:  " +str(minmin.iloc[0])+ "  " + "($"+str(miny)+")" +"\n")
file1.write("-------------------" + "\n")

