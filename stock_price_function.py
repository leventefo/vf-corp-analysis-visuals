import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from plotly.colors import n_colors

df_net_income_stock_date = pd.read_csv("VF_net_income_stock_price_new.csv")

def simplify(df):
    for col in df.columns:
        df = df[df[col].notna()]

    return df[df.columns[1:]].reset_index()

def rolling_mean(df):
    for col in df.columns[1:]:
        temp_array, temp_averages = [], []
        for value in df[col].values:
            temp_array.append(value)
            temp_averages.append(sum(temp_array) / len(temp_array))
        df[col] = temp_averages
    return df

df_net_income_stock_date = df_net_income_stock_date[["Date", "val", "Close"]]
df_net_income_stock_date = rolling_mean(df_net_income_stock_date)
df_net_income_stock_date = df_net_income_stock_date.iloc[4:]
fig = go.Figure().update_layout(template = "plotly_dark")

fig.add_trace(go.Scatter3d(x=df_net_income_stock_date["Date"], 
                           z=df_net_income_stock_date["Close"],
                           y=df_net_income_stock_date["val"],
                           marker = dict(size=4, colorscale = "viridis"), 
                           line = dict(color = "red", width = 2)))

fig.update_layout(
                  scene = dict(xaxis=dict(title = "Date"),
                  yaxis = dict(title = "Net Income $"),
                  zaxis = dict(title = "Stock price $")))

fig.update_layout(scene = dict(annotations = [
    dict(showarrow=True, x = "10/3/2011", y = 1.510768e+08, z = 13.666109, text = "Timberland acquisition",
         arrowcolor="yellow", font = dict(color = "yellow"), ay = -40),
         dict(showarrow=True, x = "10/2/2017", y = 2.276406e+08, z = 29.989839, text = "Williamson-Dickie deal",
         arrowcolor="yellow", font = dict(color = "yellow"), ax = 20, ay = -40),
         dict(showarrow=True, x = "7/1/2019", y = 2.249896e+08, z = 35.354262, text = "Post-Kontoor spin-off",
         arrowcolor="yellow", font = dict(color = "yellow"), ay = -60, ax = 20),
         dict(showarrow=True, x = "12/28/2020", y = 2.172711e+08, z = 38.751643, text = "Supreme deal",
         arrowcolor="yellow", font = dict(color = "yellow"), ay = -60, ax = -40)]))

fig.update_layout(width = 850, height = 600, autosize = False)

fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))

fig.write_html("3d_graph.html")

fig.show(renderer = "browser")