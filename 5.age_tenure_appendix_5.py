import pandas as pd
import plotly.graph_objects as go

ages = [68, 52, 57, 62, 62, 67, 61, 69, 69, 65, 62, 57]

years_of_membership = [16, 3, 16, 2, 2, 1, 10, 14, 21, 8, 12, 1]


fig = go.Figure().update_layout(template = "plotly_dark", 
                                title = "Age/Tenure", 
                                title_font_weight = 900, title_x = 0.5, title_font_size = 30)

fig.add_trace(go.Scatter(x=years_of_membership, y = ages, mode = "markers", 
                         marker = dict(color = "red", size = 13)))
fig.update_layout(xaxis_title = "Years of tenure", yaxis_title = "Age")
fig.update_layout(font_family = "Bodoni MT", font_size = 20, font_weight = 800)
fig.update_xaxes(showgrid = False)
fig.update_yaxes(showgrid = False)
fig.update_layout(yaxis = dict(zeroline = False))
fig.update_layout(xaxis = dict(zeroline = False))
fig.update_layout(width = 600, height = 600)
fig.write_image("age_tenure.png",  width = 600, height = 600, scale = 20)
fig.show(renderer = "browser")