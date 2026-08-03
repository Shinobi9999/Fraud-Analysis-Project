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
