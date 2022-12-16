import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt

# Data sources
url_climate_change = "https://data.humdata.org/dataset/b4ffadbf-1fee-4a7d-aa4c-a12b3f78a4b6/resource/bc9c06ab-fc50-427a-9ce3-9c91767514f8/download/climate-change_ukr.csv"
url_food_price = "https://data.humdata.org/dataset/9b95de1b-d4e9-4c81-b2bb-db35bd9620e8/resource/1730560f-8e9f-4999-bec8-72118ac0ee5f/download/wfp_food_prices_ukr.csv"
# Preparing the information
df_climate = pd.read_csv(url_climate_change)
df_food = pd.read_csv(url_food_price)

names = ['Cereal yield (kg per hectare)', 'Agricultural land (% of land area)']
df_climate_agricultures = df_climate[df_climate["Indicator Name"].isin(names)].iloc[:, [2,3,5]]
df_climate_agricultures["Year"] = pd.to_datetime(df_climate_agricultures["Year"], format = "%Y")
df_climate_agricultures["Value"] = df_climate_agricultures["Value"].astype("float64")
df_climate_agricultures.set_index("Year", inplace = True)
df_climate_agricultures = df_climate_agricultures.loc["2018":]
df_climate_agricultures.reset_index(inplace= True)
df_climate_agricultures["Year"] = df_climate_agricultures["Year"].dt.year
df_agricult_land = df_climate_agricultures[df_climate_agricultures["Indicator Name"] == "Agricultural land (% of land area)"]
df_yield = df_climate_agricultures[df_climate_agricultures["Indicator Name"] == "Cereal yield (kg per hectare)"]


df_food_cereals = df_food[df_food["category"] == "cereals and tubers"].iloc[:,[0,3,6,7,8,11,12,13]]
cereals = ["Barley","Rice", "Buckwheat", "Millet", "Semolina"]
df_food_cereals = df_food_cereals[df_food_cereals["commodity"].isin(cereals) & (df_food_cereals["market"] != "National Average")].iloc[:, [0,1,3,4,5,6,7]]
df_food_cereals["date"] = pd.to_datetime(df_food_cereals["date"], format = "%Y-%m-%d")
df_food_cereals.set_index("date", inplace = True)
df_food_cereals["usdprice"] = df_food_cereals["usdprice"].astype("float64")
df_food_cereals.rename(columns = {"commodity":"Grain variety"},inplace=True)
df_food_cereals = df_food_cereals.loc["2018":"2020"]

df_foods = df_food_cereals.groupby([df_food_cereals.index.year, df_food_cereals["Grain variety"]])["usdprice"].median()
df_foods = df_foods.reset_index()
df_foods.rename(columns = {"date":"Year"},inplace =True)

# Plotting
fig, (ax1,ax2,ax3) = plt.subplots(1,3,sharex=True)
fig.set_size_inches(15.5, 10.5)
sns.set_palette("husl")
sns.lineplot(data = df_foods, x = "Year", y = "usdprice", hue = "Grain variety",ax = ax1)
ax1.set(xlabel = "", ylabel = "", title = "Price(USD) for cereals per year")
ax1.grid(axis = "y")
sns.lineplot(data = df_yield, x ="Year", y = "Value", ax = ax2,color="r")
ax2.set(xlabel = "YEAR", ylabel = "", title = "Cereal Yield(kg per hectare)") 
ax2.grid(axis = "y")
sns.lineplot(data = df_agricult_land, x = "Year", y = "Value", ax= ax3,color = "g" )
ax3.set(xlabel = "", ylabel = "", title = "Agricultural land (% of land area)")
ax3.grid(axis = "y")
plt.setp([ax1,ax2,ax3], xticks = [2018,2019,2020], xticklabels = ["2018", "2019","2020"])
sns.despine()
plt.savefig("plot.png", dpi = 300)
plt.show()
