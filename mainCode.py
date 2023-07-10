import pandas as pd
import glob
import os
import plotly.express as px
import matplotlib.pyplot as plt

path1 = "concatedFilePath"
path2 = "concatedFilePath"
path3 = "concatedFilePath"
path4 = "concatedFilePath"

paths = ["folderPath",
         "folderPath",
         "folderPath",
          "folderPath"] 

for path in paths:
    all_files = glob.glob(os.path.join(path , "*.csv"))
    li = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True)
    frame.to_csv(path + "concated.csv")

df1 = pd.read_csv(path1)
df2 = pd.read_csv(path2)
df3 = pd.read_csv(path3)
df4 = pd.read_csv(path4)

for x in df1.columns:
    for y in df2.columns:
        if x == y:
            if x != "Order ID":
                df2 = df2.drop(columns= y)
df1 = pd.merge(df1, df2, on="Order ID")

for x in df1.columns:
    for y in df3.columns:
        if x == y:
            if x!= "Order ID":
                df3 = df3.drop(columns= y)
df = pd.merge(df1,df3, on="Order ID")


#for col in df.columns:
#    print( df[col].value_counts())

states = df["Ship State"].value_counts()
states = states.reset_index(drop=False)
for state in range((states["index"].size)-1):
    if len(states['index'][state]) > 2:
        states = states.drop(index=state)
#print(states)

fig = px.choropleth(states,
                    locations='index',
                    locationmode='USA-states',
                    scope='usa',
                    color='Ship State',
                    color_continuous_scale="Viridis_r",

)
#print(df4["Amount"].sum())

df["Sale Date"] = pd.to_datetime(df["Sale Date"])
dates = df["Sale Date"].value_counts()
dates = dates.reset_index(drop=False)
dates = dates.sort_values(by='index')
dates = dates.reset_index(drop=True)
start = dates["index"][0]
end = dates["index"][len(dates)-1]
new_dates = pd.date_range(start=start, end=end,freq='D')
for x in dates["index"]:
    for y in new_dates:
        if x == y:
            new_dates = new_dates.drop(y)

for x in new_dates:
    dates = dates.append({"index": x, "Sale Date": 0}, ignore_index = True)

dates = dates.sort_values(by='index')
dates = dates.reset_index(drop=True)
print(dates)

#dates = pd.concat([dates,new_dates])
#dates = dates.append(new_dates)
#print(dates)
plt.plot(dates["index"], dates["Sale Date"])
plt.show()


df["Sale Day"] = df["Sale Date"].dt.day_name()
days = df["Sale Day"].value_counts()
days = days.reset_index(drop=False)
#print(days.columns)

fig2 = plt.figure(figsize=(10,5))
plt.bar(days["index"],days["Sale Day"])


plt.show()
fig.show()