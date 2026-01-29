import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

fig = go.Figure().update_layout(template = "plotly_dark")

names = [
    "Richard T. Carucci",
    "Alexander K. Cho",
    "Juliana L. Chugg",
    "Bracken Darrell",
    "Trevor A. Edwards",
    "Mindy F. Grossman",
    "Mark S. Hoplamazian",
    "Laura W. Lang",
    "Clarence Otis, Jr.",
    "Carol L. Roberts",
    "Matthew J. Shattock",
    "Kirk C. Tanner",
]
roles = [
    "Audit Committee",
    "Talent and Compensation Committee",
    "Governance and Corporate Responsibility Committee",
    "Finance Committee",
]

roles_matrix = [
    [1, 0, 0, 1],  # Richard T. Carucci
    [1, 0, 1, 0],  # Alexander K. Cho
    [0, 2, 1, 0],  # Juliana L. Chugg
    [0, 0, 0, 1],  # Bracken Darrell
    [0, 1, 1, 0],  # Trevor A. Edwards
    [0, 1, 1, 0],  # Mindy F. Grossman
    [0, 1, 0, 2],  # Mark S. Hoplamazian
    [0, 0, 1, 1],  # Laura W. Lang
    [1, 0, 0, 1],  # Clarence Otis, Jr.
    [0, 2, 0, 1],  # Carol L. Roberts
    [0, 1, 2, 0],  # Matthew J. Shattock
    [0, 1, 1, 0],  # Kirk C. Tanner
]

data = [roles, names, roles_matrix]

fig.add_trace(go.Heatmap(y=names, x=roles, z = roles_matrix, 
                         colorscale="OrRd"))
fig.update_layout(font_family = "Bodoni MT", font_size = 20, font_weight = 800, paper_bgcolor="black")
fig.update_layout(width = 1000, height = 1000)
fig.show(renderer = "browser")