import pandas as pd
import plotly.graph_objects as go

industries = [
    "Foodservice & Hospitality",
    "Consumer & Retail Brands",
    "Technology",
    "Financial & Investment Services",
    "Industrial & Manufacturing",
]

counts = [4, 4, 1, 2, 1]


fig = go.Figure().update_layout(template = "plotly_dark", 
                                title = "Industry prevalence in the board", 
                                title_font_weight = 900, title_x = 0.5, title_font_size = 30)


fig.add_trace(go.Bar(x=counts, y = industries, orientation= "h"))

fig.update_layout(xaxis_title = "Occurence", yaxis_title = "Industry")
fig.update_layout(font_family = "Bodoni MT", font_size = 20, font_weight = 800)
fig.update_xaxes(showgrid = False)
fig.update_yaxes(showgrid = False)
fig.update_layout(yaxis = dict(zeroline = False))
fig.update_layout(xaxis = dict(zeroline = False))
fig.update_layout(width = 600, height = 600)
fig.write_image("industry_occurence.png",  width = 600, height = 600, scale = 20)