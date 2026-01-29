import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

d = {"Structure" : ["Institutional" for i in range(73)] + ["Other" for i in range(21)] + ["Individual" for i in range(6)]}

df_like = pd.DataFrame(data = d)

fig = go.Figure()

colors = ["#3B82F6", "#22C55E", "#F97316"]


def get_values(ser):
    return ser.value_counts()

table_like = get_values(df_like["Structure"])

fig.add_trace(go.Pie(labels = table_like.index.to_numpy(), values = table_like.values,
                     pull = [0, 0, 0]))

fig.update_traces(textfont_size = 17, 
                  marker = dict(colors = colors, 
                                line = dict(color = "#FFFFFF", width = 3)))

fig.update_layout(font_family = "Bodoni MT")

fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color = "white", font_weight = 600)
fig.update_layout(width = 600, height = 600)
fig.update_layout(legend = dict(orientation = "v", y= 0.5), font_size = 20)
fig.update_layout(margin=dict(t=15, b=15, l=15, r=15))
fig.write_image("ownership.png",  width = 450, height = 450, scale = 20)
