# ============================================
# SECTION 1: PULL DATA FROM SEC EDGAR API
# ============================================
import requests #The requests library lets my program send HTTP requests

headers = { #header is my browser introducing itself to the SEC
    "User-Agent": "Usain usain@example.com" #identifying myself to the SEC so that it can provide me the data i need
}

def get_annual_value(concept, target_years): #creating a function to get the annual value of a specific concept for the target years
    url = f"https://data.sec.gov/api/xbrl/companyconcept/CIK0001336917/us-gaap/{concept}.json" #f string that allows us to replace whatever is inside {} with the value we need
    response = requests.get(url, headers=headers)
    data = response.json()
    
    results = {}
    for entry in data["units"]["USD"]:
        if entry.get("form") == "10-K" and entry.get("fp") == "FY": #10K is annual filing as opposed to 10Q which is quarterly
            year = entry["end"][:4]
            if int(year) in target_years:
                results[year] = entry["val"]
    
    return results

years_needed = [2013, 2014, 2015, 2016]

#TAG FINDER
# def find_debt_tags():
#     url = "https://data.sec.gov/api/xbrl/companyfacts/CIK0001336917.json"
#     response = requests.get(url, headers=headers)
#     data = response.json()
    
#     for tag in data["facts"]["us-gaap"]:
#         if "debt" in tag.lower():
#             print(tag)

# find_debt_tags()

#calculating all values for each ratio in the beneish m-score formula
total_assets = get_annual_value("Assets", years_needed)
rev_main = get_annual_value("Revenues", years_needed)
rev_backup = get_annual_value("SalesRevenueNet", years_needed)
receivables = get_annual_value("AccountsReceivableNetCurrent", years_needed)
cost_of_goods_sold = get_annual_value("CostOfGoodsSold", years_needed)
current_assets = get_annual_value("AssetsCurrent", years_needed)
net_pp_and_e = get_annual_value("PropertyPlantAndEquipmentNet", years_needed)
depreciation = get_annual_value("DepreciationAndAmortization", years_needed)
long_term_debt = get_annual_value("LongTermDebt", years_needed)
sga_expenses = get_annual_value("SellingGeneralAndAdministrativeExpense", years_needed)
operating_cash_flow = get_annual_value("NetCashProvidedByUsedInOperatingActivities", years_needed)
net_income_loss = get_annual_value("NetIncomeLoss", years_needed)

#printing the values
total_revenue = {**rev_backup, **rev_main} # Merge: start with backup, then overwrite with main where available
print("Total Revenue:", total_revenue) #total sales
print("Total Assets:", total_assets)#total assets
print("Receivables:", receivables) #customer payments
print("Cost of Goods Sold:", cost_of_goods_sold)
print("Current Assets:", current_assets) #current assets
print("Net Property, Plant and Equipment:", net_pp_and_e) #net pp&e
print("Depreciation:", depreciation) #depreciation
print("Long Term Debt:", long_term_debt) #long term debt
print("Selling, General and Administrative Expenses:", sga_expenses) #selling, general and administrative expenses
print("Operating Cash Flow:", operating_cash_flow) #operating cash flow
print("Net Income Loss:", net_income_loss) #net income loss
print("---------------------------------")

# ============================================
# SECTION 2: CALCULATING ALL RATIOS
# ============================================
#FIRST RATIO: DSRI (Days Sales in Receivables Index)
DSRI_2014 = (receivables["2014"]/total_revenue["2014"])/(receivables["2013"]/total_revenue["2013"]) #calculating DSRI for 2014
DSRI_2016 = (receivables['2016']/total_revenue['2016'])/(receivables['2015']/total_revenue['2015']) #calculating DSRI for 2016
print("DSRI 2014:", DSRI_2014)
print("DSRI 2016:", DSRI_2016)
print("---------------------------------")
#SECOND RATIO: GMI (Gross Margin Index)
Gross_Margin_2013 = (total_revenue['2013']-cost_of_goods_sold['2013'])/(total_revenue['2013'])
Gross_Margin_2014 = (total_revenue['2014']-cost_of_goods_sold['2014'])/(total_revenue['2014'])
Gross_Margin_2015 = (total_revenue['2015']-cost_of_goods_sold['2015'])/(total_revenue['2015'])
Gross_Margin_2016 = (total_revenue['2016']-cost_of_goods_sold['2016'])/(total_revenue['2016'])
GMI_2014 = Gross_Margin_2013/Gross_Margin_2014
GMI_2016 = Gross_Margin_2015/Gross_Margin_2016
print("GMI 2014:", GMI_2014)
print("GMI 2016:", GMI_2016)
print("---------------------------------")
#THIRD RATIO: AQI (Asset Quality Index)
Asset_Quality_2013 = 1 - (current_assets['2013'] + net_pp_and_e['2013'])/(total_assets['2013'])
Asset_Quality_2014 = 1 - (current_assets['2014'] + net_pp_and_e['2014'])/(total_assets['2014'])
Asset_Quality_2015 = 1 - (current_assets['2015'] + net_pp_and_e['2015'])/(total_assets['2015'])
Asset_Quality_2016 = 1 - (current_assets['2016'] + net_pp_and_e['2016'])/(total_assets['2016'])
AQI_2014 = Asset_Quality_2014/Asset_Quality_2013
AQI_2016 = Asset_Quality_2016/Asset_Quality_2015
print("AQI 2014:", AQI_2014)
print("AQI 2016:", AQI_2016)
print("---------------------------------")
#FOURTH RATIO: SGI (Sales Growth Index)
SGI_2014 = total_revenue['2014']/total_revenue['2013']
SGI_2016 = total_revenue['2016']/total_revenue['2015']
print("SGI 2014:", SGI_2014)
print("SGI 2016:", SGI_2016)
print("---------------------------------")
#FIFTH RATIO: DEPI (Depreciation Index)
Dep_Rate_2013 = depreciation['2013'] / (depreciation['2013'] + net_pp_and_e['2013'])
Dep_Rate_2014 = depreciation['2014'] / (depreciation['2014'] + net_pp_and_e['2014'])
Dep_Rate_2015 = depreciation['2015'] / (depreciation['2015'] + net_pp_and_e['2015'])
Dep_Rate_2016 = depreciation['2016'] / (depreciation['2016'] + net_pp_and_e['2016'])
DEPI_2014 = Dep_Rate_2013 / Dep_Rate_2014
DEPI_2016 = Dep_Rate_2015 / Dep_Rate_2016
print("DEPI 2014:", DEPI_2014)
print("DEPI 2016:", DEPI_2016)
print("---------------------------------")
#SIXTH RATIO: SGAI (Sales, General and Administrative Expenses Index)
SGAI_2014 = (sga_expenses['2014']/total_revenue['2014'])/(sga_expenses['2013']/total_revenue['2013'])
SGAI_2016 = (sga_expenses['2016']/total_revenue['2016'])/(sga_expenses['2015']/total_revenue['2015'])
print("SGAI 2014:", SGAI_2014)
print("SGAI 2016:", SGAI_2016)
print("---------------------------------")
#SEVENTH RATIO: LVGI (Leverage Index)
LVGI_2014 = (long_term_debt['2014']/total_assets['2014'])/(long_term_debt['2013']/total_assets['2013'])
LVGI_2016 = (long_term_debt['2016']/total_assets['2016'])/(long_term_debt['2015']/total_assets['2015'])
print("LVGI 2014:", LVGI_2014)
print("LVGI 2016:", LVGI_2016)
print("---------------------------------")
#EIGHTH RATIO: TATA (Total Accruals to Total Assets)
TATA_2014 = (net_income_loss['2014'] - operating_cash_flow['2014'])/total_assets['2014']
TATA_2016 = (net_income_loss['2016'] - operating_cash_flow['2016'])/total_assets['2016']
print("TATA 2014:", TATA_2014)
print("TATA 2016:", TATA_2016)
print("---------------------------------")
# ============================================
# SECTION 3: CALCULATE FINAL M-SCORE
# ============================================