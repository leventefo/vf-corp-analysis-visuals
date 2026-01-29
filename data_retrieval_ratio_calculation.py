import requests
import pandas as pd
import json
from functools import reduce

def get_ticker_cik(ticker:str, ID:dict):
    companyTickers = requests.get("https://www.sec.gov/files/company_tickers.json", 
                              headers=ID)
    companyData = pd.DataFrame.from_dict(companyTickers.json(), orient = "index")
    companyData["cik_str"] = companyData["cik_str"].astype(str).str.zfill(10)
    ticker_cik = companyData.loc[companyData["ticker"] == ticker]["cik_str"].to_numpy()[0]
    return ticker_cik


def get_line_item_data(ticker_cik:str, line_item_name:str, length_crit:int, ID:dict):
    try:
        line_item_concept = requests.get(
        f"https://data.sec.gov/api/xbrl/companyconcept/CIK{ticker_cik}/us-gaap/{line_item_name}.json",
        headers=ID)
    except:
        print("No such line item found.")

    line_item = pd.DataFrame.from_dict((line_item_concept.json()["units"]["USD"]))
    line_item_10Q_10K = line_item[(line_item.form == "10-Q") | (line_item.form == "10-K")]
    line_item_10Q_10K = line_item_10Q_10K.reset_index(drop=True)
    line_item_10Q_10K = line_item_10Q_10K[line_item_10Q_10K["frame"].str.len() == length_crit]
    line_item_10Q_10K = line_item_10Q_10K[["end", "val", "frame"]]
    line_item_10Q_10K.rename(columns = {"val": line_item_name}, inplace = True)
    line_item_10Q_10K = line_item_10Q_10K[line_item_10Q_10K["frame"].notna()]

    return line_item_10Q_10K


def calculate_ratio(df_1, df_2, col_title_1:str, col_title_2:str, output_col_name:str):
    df_merged = df_1.merge(right = df_2, how = "left", on = "end")
    df_merged[output_col_name] = df_merged.apply(lambda x: x[col_title_1]/x[col_title_2], axis = 1)
    return df_merged


def simplify2(lst:list):
    df_counter = 0
    for element in lst:
        for col in element[0].columns:
            element[0] = element[0][element[0][col].notna()]
        element[0] = element[0][["end", lst[df_counter][1]]]
        df_counter +=1
    return lst


def recursive_df_merge(lst):
    if len(lst) == 1:
        return lst[0]
    else:
        lst[1] = lst[0].merge(right=lst[1], how = "left", on = "end")
        lst.pop(0)
        return recursive_df_merge(lst)


def create_csv(simplified_df_list):
    profitability_ratios = ["ROTA", "ROS", "AssetTurnover", "ROE"]
    pr_rs = []
    liquidity_ratios = ["CurrentRatio", "Quick Ratio", "Working Capital to Sales", "InvDays"
    "Debtor Days", "Creditor Days"]
    lq_rs = []
    financial_strength_ratios = ["Interest Coverage", "Debt to Equity", "Financial Leverage"]
    fs_rs = []

    for element in simplified_df_list:
        fs_rs.append(element[0])
    
    df_fs_rs = recursive_df_merge(fs_rs)


def main():
    ID = {"User-Agent": "fo.levente@gmail.com"}
    ticker_cik = get_ticker_cik("VFC", ID)
    df_OperatingIncomeLoss = get_line_item_data(ticker_cik, "OperatingIncomeLoss", 8, ID)
    df_Assets = get_line_item_data(ticker_cik, "Assets", 9, ID)
    df_ROTA = calculate_ratio(df_OperatingIncomeLoss, df_Assets, "OperatingIncomeLoss", "Assets", "ROTA")
    df_Revenue = get_line_item_data(ticker_cik, "Revenues", 8, ID)
    df_RevenueFromContractWithCustomerExcludingAssessedTax = get_line_item_data(ticker_cik, "RevenueFromContractWithCustomerExcludingAssessedTax", 8, ID)
    df_Revenue_last_date = df_Revenue.iloc[-1]["end"]
    df_RevenueFromContractWithCustomerExcludingAssessedTax_Filtered = df_RevenueFromContractWithCustomerExcludingAssessedTax[df_RevenueFromContractWithCustomerExcludingAssessedTax["end"] > df_Revenue_last_date]
    df_RevenueFromContractWithCustomerExcludingAssessedTax_Filtered.rename(columns={"RevenueFromContractWithCustomerExcludingAssessedTax":"Revenues"}, inplace = True)
    df_revenuePlus = pd.concat([df_Revenue, df_RevenueFromContractWithCustomerExcludingAssessedTax_Filtered])
    df_ROS = calculate_ratio(df_OperatingIncomeLoss, df_revenuePlus, "OperatingIncomeLoss", "Revenues", "ROS")
    df_AssetTurnover = calculate_ratio(df_revenuePlus, df_Assets, "Revenues", "Assets", "AssetTurnover")
    df_NetIncome = get_line_item_data(ticker_cik, "NetIncomeLoss", 8, ID)
    df_Owners_funds = get_line_item_data(ticker_cik, "StockholdersEquity", 9, ID)
    df_ROE = calculate_ratio(df_NetIncome, df_Owners_funds, "NetIncomeLoss", "StockholdersEquity", "ROE")
    df_Current_Assets = get_line_item_data(ticker_cik, "AssetsCurrent", 9, ID)
    df_Current_Liabilities = get_line_item_data(ticker_cik, "LiabilitiesCurrent", 9, ID)
    df_Current_Ratio = calculate_ratio(df_Current_Assets, df_Current_Liabilities, "AssetsCurrent", "LiabilitiesCurrent", "CurrentRatio")
    df_Inventories = get_line_item_data(ticker_cik, "InventoryNet", 9, ID)
    df_temp = df_Current_Assets.merge(right = df_Inventories, how = "left", on = "end")
    df_temp["Quick"] = df_temp.apply(lambda x: x["AssetsCurrent"] - x["InventoryNet"], axis = 1)
    df_Quick_Ratio = calculate_ratio(df_temp, df_Current_Liabilities, "Quick", "LiabilitiesCurrent", "Quick Ratio")
    df_Working_Capital = df_Current_Assets.merge(right=df_Current_Liabilities, how = "left", on = "end")
    df_Working_Capital["WorkingCapital"] = df_Working_Capital.apply(lambda x: x["AssetsCurrent"] - x["LiabilitiesCurrent"], axis = 1)
    df_Working_Capital = df_Working_Capital[["end", "WorkingCapital", "frame_x"]]
    df_Working_Capital_to_Sales_Ratio = calculate_ratio(df_Working_Capital, df_revenuePlus, "WorkingCapital", "Revenues", "Working Capital to Sales")
    df_Inventory_Days = calculate_ratio(df_Inventories, df_revenuePlus, "InventoryNet", "Revenues", "InvDays")
    df_Inventory_Days["InvDays"] = df_Inventory_Days.apply(lambda x: x["InvDays"] *365, axis = 1)
    df_AccountsReceivableNetCurrent = get_line_item_data(ticker_cik, "AccountsReceivableNetCurrent", 9, ID)
    df_ReceivablesNetCurrent = get_line_item_data(ticker_cik, "ReceivablesNetCurrent", 9, ID)
    df_ReceivablesNetCurrent_last_date = df_ReceivablesNetCurrent.iloc[-1]["end"]
    df_AccountsReceivableNetCurrent = df_AccountsReceivableNetCurrent[df_AccountsReceivableNetCurrent["end"]>df_ReceivablesNetCurrent_last_date]
    df_AccountsReceivableNetCurrent.rename(columns = {"AccountsReceivableNetCurrent": "Accounts Receivable"}, inplace = True)
    df_ReceivablesNetCurrent.rename(columns = {"ReceivablesNetCurrent": "Accounts Receivable"}, inplace = True)
    df_AccountsReceivable_Extended = pd.concat([df_ReceivablesNetCurrent, df_AccountsReceivableNetCurrent])
    df_Debtor_Days = calculate_ratio(df_AccountsReceivable_Extended, df_revenuePlus, "Accounts Receivable", "Revenues", "Debtor Days")
    df_Debtor_Days["Debtor Days"] = df_Debtor_Days.apply(lambda x: x["Debtor Days"] *365, axis = 1)
    df_Accounts_Payable = get_line_item_data(ticker_cik, "AccountsPayableCurrent", 9, ID)
    df_Creditor_Days = calculate_ratio(df_Accounts_Payable, df_revenuePlus, "AccountsPayableCurrent", "Revenues", "Creditor Days")
    df_Creditor_Days["Creditor Days"] = df_Creditor_Days.apply(lambda x: x["Creditor Days"] *365, axis = 1)
    df_Creditor_Days = df_Creditor_Days[["end", "Creditor Days"]]
    df_InterestAndDebtExpense = get_line_item_data(ticker_cik, "InterestAndDebtExpense", 8, ID)
    df_InterestAndDebtExpense_last_date = df_InterestAndDebtExpense.iloc[-1]["end"]
    df_Interest_Expense = get_line_item_data(ticker_cik, "InterestExpense", 8, ID)
    df_Interest_Expense = df_Interest_Expense[df_Interest_Expense["end"]>df_InterestAndDebtExpense_last_date]
    df_InterestAndDebtExpense.rename(columns = {"InterestAndDebtExpense":"Interest Expenses"}, inplace = True)
    df_Interest_Expense.rename(columns = {"InterestExpense":"Interest Expenses"}, inplace = True)
    df_Interest_Expense_Extended = pd.concat([df_InterestAndDebtExpense,df_Interest_Expense])
    df_continuer = pd.read_csv("InterestExpenses.csv")
    df_Interest_Expense_Extended = pd.concat([df_Interest_Expense_Extended, df_continuer])
    df_Interest_Coverage_Ratio = calculate_ratio(df_OperatingIncomeLoss, df_Interest_Expense_Extended, "OperatingIncomeLoss", "Interest Expenses", "Interest Coverage")
    df_stock_holders_equity = get_line_item_data(ticker_cik, "StockholdersEquity", 9, ID)
    df_total_liabilities = df_stock_holders_equity.merge(right = df_Assets, how = "left", on = "end")
    df_total_liabilities["Total Liabilities"] = df_total_liabilities.apply(lambda x: x["Assets"] - x["StockholdersEquity"], axis = 1)
    df_debt_to_equity = df_total_liabilities
    df_debt_to_equity["Debt to Equity"] = df_total_liabilities.apply(lambda x: x["Total Liabilities"] - x["StockholdersEquity"], axis = 1)
    df_debt_to_equity["Debt to Equity"] = df_debt_to_equity.apply(lambda x: x["Debt to Equity"]/x["StockholdersEquity"], axis = 1)
    df_financial_leverage = df_Assets.merge(right = df_stock_holders_equity, how = "left", on = "end")
    df_financial_leverage["Financial Leverage"] = df_financial_leverage.apply(lambda x: x["Assets"]/x["StockholdersEquity"], axis = 1)
    
    financial_metrics_lst = [[df_Interest_Coverage_Ratio,"Interest Coverage"],
                   [df_debt_to_equity,"Debt to Equity"], [df_financial_leverage,"Financial Leverage"]]
    
    financial_metrics_lst_simplified = simplify2(financial_metrics_lst)


    create_csv(financial_metrics_lst_simplified)

main()











