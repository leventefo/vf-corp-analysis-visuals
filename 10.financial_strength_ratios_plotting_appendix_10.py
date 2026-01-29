import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from plotly.colors import n_colors
import statistics

financial_strength_ratios_absolute = pd.read_csv("real_data/FinancialStrengthRatiosFinal2.csv")
financial_strength_ratios_absolute.drop(columns=["Debt to Equity"], inplace= True)

def z_score_conversion(df):
    for col in df.columns[1:]:
        df[col] = (df[col] - df[col].mean())/ df[col].std()
    return df

def simplify(df):
    for col in df.columns:
        df = df[df[col].notna()]

    return df[df.columns[1:]].reset_index().drop(columns = ["index"])

def cumulative_moving_average_transformation(df):
    for col in df.columns[2:]:
        temp_array, temp_averages = [], []
        for value in df[col].values:
            temp_array.append(value)
            temp_averages.append(sum(temp_array) / len(temp_array))
        df[col] = temp_averages
    return df

def four_quarter_rolling_mean_transformation(df):
    for col in df.columns[1:]:
        temp_array, temp_average, mean_counter, counter = [], [], 1, 1
        for value in df[col].values:
            if counter >=5:
                mean_counter +=1
            temp_array.append(value)
            temp_average.append(sum(temp_array[mean_counter-1:mean_counter +3])/len(temp_array[mean_counter-1:mean_counter +3]))
            counter += 1
        df[col] = temp_average
    return df

def modify(df):
    return z_score_conversion(four_quarter_rolling_mean_transformation(simplify(df)))

fig_financial_strength_ratios = go.Figure().update_layout(template = "plotly_dark", title = "VF's Financial Strength Ratios", title_x = 0.5, title_font_weight = 600)

col_counter_color = {1:"lime", 2:"red"}

def plot_financial_strength_ratios(df, fig):
    col_counter = 1
    for col in df.columns[1:]:
        name = df.columns[col_counter]

        if name == "Interest Coverage":
            fig.add_trace(go.Scatter(x = df["end"], y = df[col],
                                 name = name, 
                                 line = dict(width = 3, color = col_counter_color[col_counter]),
                                 mode = "lines+markers", marker_symbol = "square"))
        else:
            fig.add_trace(go.Scatter(x = df["end"], y = df[col],
                                 name = name, 
                                 line = dict(width = 3, color = col_counter_color[col_counter]),
                                 mode = "lines+markers", marker_symbol = "diamond", marker_size = 7))
        col_counter +=1

plot_financial_strength_ratios(modify((financial_strength_ratios_absolute)), fig_financial_strength_ratios)

fig_financial_strength_ratios.update_layout(width = 750, height = 450,
                                   legend = dict(groupclick = "toggleitem", 
                                                 orientation = "h", x= 0.27))

fig_financial_strength_ratios.update_layout(margin=dict(t=70, b=20, l=30, r=30))

fig_financial_strength_ratios.add_annotation(xref = "x1", yref = "y1", x="2011-06-30", y = 0.4, 
                                        text = "A", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=3,
                                        font = dict(color = "yellow", size = 14, weight = 600),
                                        ay = -60, ax = -20) #Timberland Acquisition


fig_financial_strength_ratios.add_annotation(xref = "x1", yref = "y1", x="2012-09-29", y = 0.75, 
                                        text = "B", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=3,
                                        font = dict(color = "yellow", size = 14, weight = 600),
                                        ay = -60, ax = -20) #Strong autumn peaks

fig_financial_strength_ratios.add_annotation(xref = "x1", yref = "y1", x="2017-09-30 ", y = -0.6, 
                                        text = "C", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=3,
                                        font = dict(color = "yellow", size = 14, weight = 600),
                                        ay = 60, ax = -20) #Williamson-Dickie acquisition


fig_financial_strength_ratios.add_annotation(xref = "x1", yref = "y1", x="2019-06-29", y = -0.5, 
                                        text = "D", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=3,
                                        font = dict(color = "yellow", size = 14, weight = 600),
                                        ay = 60, ax = -20) #Spin-off deleveraging


fig_financial_strength_ratios.add_annotation(xref = "x1", yref = "y1", x="2018-03-31", y = 0.4, 
                                        text = "E", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=3,
                                        font = dict(color = "yellow", size = 14, weight = 600),
                                        ay = -60, ax = 25) #Coverage turns more volatile

fig_financial_strength_ratios.add_annotation(xref = "x1", yref = "y1", x="2020-12-26", y = -0.3, 
                                        text = "F", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=3,
                                        font = dict(color = "yellow", size = 14, weight = 600),
                                        ay = -80, ax =15) #Coverage turns more volatile


fig_financial_strength_ratios.add_annotation(xref = "x1", yref = "y1", x="2021-10-02", y = -0.5, 
                                        text = "G", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=3,
                                        font = dict(color = "yellow", size = 14, weight = 600),
                                        ay = 80, ax =15) # IC recovers as stores reopen


fig_financial_strength_ratios.add_annotation(xref = "x1", yref = "y1", x="2022-10-01", y = -0.8, 
                                        text = "H", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=3,
                                        font = dict(color = "yellow", size = 14, weight = 600),
                                        ay = 80, ax =15) #Supreme issues and inflation

fig_financial_strength_ratios.add_annotation(xref = "x1", yref = "y1", x="2022-12-31", y = 0.7, 
                                        text = "I", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=3,
                                        font = dict(color = "yellow", size = 14, weight = 600),
                                        ay = -80, ax =-5) #Supreme issues and inflation



fig_financial_strength_ratios.add_annotation(xref = "x1", yref = "y1", x="2024-09-28", y = -1.65, 
                                        text = "J", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=3,
                                        font = dict(color = "yellow", size = 14, weight = 600),
                                        ay = -80, ax =0) #High interest rates and impairements sharply weaken earings,


fig_financial_strength_ratios.add_annotation(xref = "x1", yref = "y1", x="2024-09-28", y = 2, 
                                        text = "K", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=3,
                                        font = dict(color = "yellow", size = 14, weight = 600),
                                        ay = 80, ax =25) #High interest rates and impairements sharply weaken earings,


fig_financial_strength_ratios.write_image("FSR.png", width = 750, height = 450, scale = 6)