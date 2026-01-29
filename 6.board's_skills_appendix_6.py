import pandas as pd
import plotly.graph_objects as go

directors = [
    "Carucci",
    "Cho",
    "Chugg",
    "Darrell",
    "Edwards",
    "Grossman",
    "Hoplamazian",
    "Lang",
    "Otis Jr.",
    "Roberts",
    "Shattock",
    "Tanner"]

skills = [
    "Talent and Culture",
    "Design and Product Innovation",
    "Operations and Process Transformation",
    "Finance",
    "Portfolio Management/M&A",
    "Apparel/Footwear/Consumer Products",
    "Retail/Direct to Consumer",
    "Brand Growth and Management",
    "Digital, Data Insights and Analytics",
    "Environmental/Sustainability/Climate Change",
    "Global Perspective",
    "IT/Cybersecurity/Privacy",
    "Public Company Executive"]

has_skill = [
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # Talent and Culture
    [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1],  # Design and Product Innovation
    [1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1],  # Operations and Process Transformation
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # Finance
    [1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1],  # Portfolio Management/M&A
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1],  # Apparel/Footwear/Consumer Products
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1],  # Retail/Direct to Consumer
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],  # Brand Growth and Management
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1],  # Digital, Data Insights and Analytics
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1],  # Environmental/Sustainability/Climate Change
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],  # Global Perspective
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
    [1 for i in range(12)],  # IT/Cybersecurity/Privacy# Public Company Executive
]

fig = go.Figure().update_layout(template = "plotly_dark", 
                                title = "Director skills", 
                                title_font_weight = 1000, title_x = 0.5, title_font_size = 30)


fig.add_trace(go.Heatmap(y=skills, x=directors, z = has_skill, 
                         colorscale="OrRd"))


fig.update_layout(font_family = "Bodoni MT", font_size = 20, font_weight = 800, paper_bgcolor="black")
fig.update_yaxes(tickangle  = 45)
fig.update_layout(width = 1200, height = 1200)
fig.show(renderer = "browser")