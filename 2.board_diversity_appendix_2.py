import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

d = {"Diversity" : ["USA" for i in range(714)] + ["Europe" for i in range(214)] + ["Oceana" for i in range(72)]}

df_like = pd.DataFrame(data = d)

fig = make_subplots().update_layout()

colors = ["#3B82F6", "#22C55E", "#EC4899"]

def get_values(ser):
    return ser.value_counts()

table_like = get_values(df_like["Diversity"])

fig.add_trace(go.Pie(labels = table_like.index.to_numpy(), values = table_like.values,
                     pull = [0, 0, 0]))
fig.update_traces(textfont_size = 17, 
                  marker = dict(colors = colors, 
                                line = dict(color = "#FFFFFF", width = 3)))
fig.update_layout(font_family = "Bodoni MT")
fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color = "white", font_weight = 600)
fig.update_layout(width = 600, height = 600)
fig.update_layout(legend = dict(orientation = "h", x= 0.24), font_size = 20)
fig.update_layout(margin=dict(t=5, b=0, l=0, r=0))
fig.write_image("diversity.png",  width = 450, height = 450, scale = 20)
fig.show(renderer = "browser")
