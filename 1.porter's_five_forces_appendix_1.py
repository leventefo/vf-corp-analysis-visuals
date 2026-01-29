import plotly.graph_objects as go
import pandas as pd

fig = go.Figure().update_layout(template = "plotly_dark")

fig.add_trace(go.Scatterpolar(r = [5,4,3,4,3],
                              theta=["Rivalry", "Buyer power", 
                                     "Supplier power", 
                                     "Threat of substitutes",
                                     "Threat of new entrants"],
                                     fill = "toself", 
                                     marker_line_width = 2,
                                     marker = dict(color = "#FF0000")), )

fig.update_layout(width = 750, height = 450, showlegend = False)
fig.update_layout(margin=dict(t=30, b=30, l=30, r=30))
fig.update_layout(font_family = "Bodoni MT", font_size = 20, font_weight = 600)
fig.update_layout(paper_bgcolor="black")
fig.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, 5], 
      showline = True,
      gridcolor = "white",
      gridwidth = 3
    ), angularaxis = dict(linewidth = 4, showline = True,
                          linecolor = "white")),
  showlegend=False
)
fig.write_image("Polar_management.png",  width = 750, height = 450, scale = 20)

#fig.show(renderer = "browser")