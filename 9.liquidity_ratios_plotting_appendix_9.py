import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from plotly.colors import n_colors
import statistics

liquidity_ratios_absolute = pd.read_csv("real_data/LiquidityRatiosFinal.csv")
liquidity_ratios_absolute.rename(columns = {"CurrentRatio": "Current Ratio", "InvDays" : "Inventory Days"}, inplace = True)

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

fig_liquidity_ratios = make_subplots(rows=1, cols = 2, subplot_titles=("Liquidity level", "Working-capital efficiency")).update_layout(
    template = "plotly_dark", 
    title = "VF's Liquidity Ratios", 
    title_x = 0.5, title_font_weight = 600)

def plot_liquidity_ratios(df, fig):
    col_counter = 1
    for col in df.columns[1:]:
        name = df.columns[col_counter]
        if name in ["Current Ratio", "Quick Ratio", "Working Capital to Sales"]:
            fig.add_trace(go.Scatter(x=df["end"], y = df[col], 
                                     name = name, 
                                     line = dict(width = 2),
                                     legendgroup="group 1",
                                     legendgrouptitle_text = "Liquidity level",
                                     legend = "legend1"), row = 1, col = 1)
        else:
            fig.add_trace(go.Scatter(x=df["end"], y = df[col], 
                                     name = name, 
                                     line = dict(width = 2),
                                     legendgroup="group 2",
                                     legendgrouptitle_text = "Working-capital efficiency",
                                     legend = "legend2"), row = 1, col = 2)
        col_counter +=1

fig_liquidity_ratios.update_yaxes(range = [-2, 4], row =1, col =1)
fig_liquidity_ratios.update_yaxes(range = [-2, 4], row =1, col =2)

plot_liquidity_ratios(modify(liquidity_ratios_absolute), fig_liquidity_ratios)

fig_liquidity_ratios.update_layout(width = 750, height = 450,
                                   legend1 = dict(groupclick = "toggleitem", orientation = "h", x= 0.12),
                                   )

fig_liquidity_ratios.update_layout(legend2 = dict(groupclick = "toggleitem", orientation = "h", x= 0.65))

fig_liquidity_ratios.add_annotation(xref = "x1", yref = "y1", x="2009-01-03", y = 0.6, 
                                        text = "A", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=2,
                                        font = dict(color = "yellow", size = 12),
                                        ay = -40, ax = 10) #Management holds extra cash


fig_liquidity_ratios.add_annotation(xref = "x2", yref = "y2", x="2009-01-03", y = 0.6, 
                                        text = "A", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=2,
                                        font = dict(color = "yellow", size = 12),
                                        ay = -40, ax = 10) #Management keeps invs conservative


fig_liquidity_ratios.add_annotation(xref = "x1", yref = "y1", x="2011-06-30", y = 1.2, 
                                        text = "B", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=2,
                                        font = dict(color = "yellow", size = 12),
                                        ay = -40, ax = 10) #Demand stabilizes and forecasting improves


fig_liquidity_ratios.add_annotation(xref = "x2", yref = "y2", x="2011-06-30", y = -0.1, 
                                        text = "B", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=2,
                                        font = dict(color = "yellow", size = 12),
                                        ay = -40, ax = 10) #Efficiency improves



fig_liquidity_ratios.add_annotation(xref = "x1", yref = "y1", x="2011-10-01", y = 0.2, 
                                        text = "C", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=2,
                                        font = dict(color = "yellow", size = 12),
                                        ay = -40, ax = 15) #Timberland aquisition increases debt


fig_liquidity_ratios.add_annotation(xref = "x2", yref = "y2", x="2011-10-01", y = -0.25, 
                                        text = "C", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=2,
                                        font = dict(color = "yellow", size = 12),
                                        ay = 40, ax = 10) #Timberland aquisition adds invs


fig_liquidity_ratios.add_annotation(xref = "x1", yref = "y1", x="2015-10-03", y = -0.3, 
                                        text = "D", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=2,
                                        font = dict(color = "yellow", size = 12),
                                        ay = -40, ax = 15) #Falling inv days pulls WC to sales with it. Buybacks reduce current ratio


fig_liquidity_ratios.add_annotation(xref = "x2", yref = "y2", x="2015-10-03", y = -1, 
                                        text = "D", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=2,
                                        font = dict(color = "yellow", size = 12),
                                        ay = 40, ax = 10) #Learning EOS -> Inventor days fall


fig_liquidity_ratios.add_annotation(xref = "x1", yref = "y1", x="2017-12-30", y = -0.5, 
                                        text = "E", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=2,
                                        font = dict(color = "yellow", size = 12),
                                        ay = 40, ax = 11) #Agreement to buy WD weakens current and quick ratio


fig_liquidity_ratios.add_annotation(xref = "x2", yref = "y2", x="2017-12-30", y = -0.1, 
                                        text = "E", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=2,
                                        font = dict(color = "yellow", size = 12),
                                        ay = -40, ax = -20) #Workwear is inventory heavy, inv days rise

fig_liquidity_ratios.add_annotation(xref = "x1", yref = "y1", x="2019-06-29", y = -0.1, 
                                        text = "F", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=2,
                                        font = dict(color = "yellow", size = 12),
                                        ay = 40, ax = 15) #Kontoor Brands sepration completed -> WC falls and current ratio increases


fig_liquidity_ratios.add_annotation(xref = "x2", yref = "y2", x="2019-06-29", y = -1, 
                                        text = "F", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=2,
                                        font = dict(color = "yellow", size = 12),
                                        ay = 40, ax = -15) #Slow paying customers falls, debtor days improves.

fig_liquidity_ratios.add_annotation(xref = "x1", yref = "y1", x="2020-03-28", y = 0.24, 
                                        text = "G", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=2,
                                        font = dict(color = "yellow", size = 12),
                                        ay = -40, ax = -15) #Post Kontoor, with more premium, higher-turning brand mix, VF runs tighter WC


fig_liquidity_ratios.add_annotation(xref = "x2", yref = "y2", x="2020-03-28", y = -0.6, 
                                        text = "G", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=2,
                                        font = dict(color = "yellow", size = 12),
                                        ay = 40, ax = 15) #Inv days follow



fig_liquidity_ratios.add_annotation(xref = "x1", yref = "y1", x="2020-12-26", y = 3.4, 
                                        text = "H", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=2,
                                        font = dict(color = "yellow", size = 12),
                                        ay = 40, ax = -25) #WHO declares pandemic, VF closes all owned NA owned stores, sales collapse WC to sales jumps. VF takes on massive debt with limited immediate payables. Current ratio quick jumps


fig_liquidity_ratios.add_annotation(xref = "x2", yref = "y2", x="2020-12-26", y = 2.2, 
                                        text = "H", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=2,
                                        font = dict(color = "yellow", size = 12),
                                        ay = -40, ax = -15) #Inv days jump, incomes falls, customers pay slower, debtor days rise.



fig_liquidity_ratios.add_annotation(xref = "x1", yref = "y1", x="2021-07-03", y = 2, 
                                        text = "I", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=2,
                                        font = dict(color = "yellow", size = 12),
                                        ay = 40, ax = 25) #Supreme acquisition reduced current and quick ratio


fig_liquidity_ratios.add_annotation(xref = "x2", yref = "y2", x="2022-01-01", y = -1.2, 
                                        text = "I", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=2,
                                        font = dict(color = "yellow", size = 12),
                                        ay = 40, ax = 25) #Added supreme stock increases inv days


fig_liquidity_ratios.add_annotation(xref = "x2", yref = "y2", x="2021-07-03", y = 0.86, 
                                        text = "J", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=2,
                                        font = dict(color = "yellow", size = 12),
                                        ay = -60, ax = -35) #Agrrement to sell occupational workwar completes, inv days falls and debtor days improve



fig_liquidity_ratios.add_annotation(xref = "x1", yref = "y1", x="2023-07-01", y = -1.6, 
                                        text = "K", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=2,
                                        font = dict(color = "yellow", size = 12),
                                        ay = -40, ax = 5) #Weak earnings and high stock levels force VF to lean on vendors. Limited spare cash current and quick raio fall


fig_liquidity_ratios.add_annotation(xref = "x2", yref = "y2", x="2023-07-01", y = 0.4, 
                                        text = "K", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=2,
                                        font = dict(color = "yellow", size = 12),
                                        ay = 40, ax = 5) #Creditor days jump


fig_liquidity_ratios.add_annotation(xref = "x1", yref = "y1", x="2024-09-28", y = -1.3, 
                                        text = "L", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=2,
                                        font = dict(color = "yellow", size = 12),
                                        ay = -40, ax = 5) #Cash proceeds prove a small lift to current and quick ratios


fig_liquidity_ratios.add_annotation(xref = "x2", yref = "y2", x="2024-09-28", y = 2.1, 
                                        text = "L", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=2,
                                        font = dict(color = "yellow", size = 12),
                                        ay = -60, ax = 5) #Supreme sold -> inv days edge down




fig_liquidity_ratios.add_annotation(xref = "x1", yref = "y1", x="2025-09-27", y = -1, 
                                        text = "M", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=2,
                                        font = dict(color = "yellow", size = 12),
                                        ay = -40, ax = 5) #agreement to sell dickies, pushes current and quick ratio up


fig_liquidity_ratios.add_annotation(xref = "x2", yref = "y2", x="2025-09-27", y = 2, 
                                        text = "M", 
                                        showarrow=True, 
                                        arrowhead=1,
                                        arrowcolor="yellow",
                                        arrowwidth=2,
                                        font = dict(color = "yellow", size = 12),
                                        ay = 50, ax = 0) #reduced inventories


fig_liquidity_ratios.update_layout(margin=dict(t=70, b=20, l=30, r=30))

fig_liquidity_ratios.write_image("LQRS5.png", width = 750, height = 450, scale = 6)
