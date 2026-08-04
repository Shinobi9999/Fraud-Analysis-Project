Fraud analysis project:
UnderArmour company’s UID (or CIK) on SEC website= 00013336917
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

This code pulls the original, non repeated total assets, revenue, and receivables from the years 2013 to 2016. Since UnderArmour was growing rapidly in the course of these years, the attempt to fake their numbers to look good was tempting here.

A flaw that I have noticed here is that the SEC EDGAR API does not have common tags for every company. So, if someone is pulling data needed for audit or legal purposes, it is a hassle since they have to go through every specific tag that comprises the values they need. For example, Under Armour reported revenue under SalesRevenueNet in 2014-2015 but switched to Revenues in 2013 and 2016. To handle this, I built a merge system that tries multiple known tags and combines results, prioritizing the more authoritative tag where both exist.

The following values have been pulled to calculate the 8 specific ratios of the Beneish M-score formula.
Year	Total Assets
2013	$1.58 Billion
2014	$2.10 Billion
2015	$2.87 Billion
2016	$3.64 Billion


Year	Total Revenue
2013	$2.08 Billion
2014	$3.00 Billion
2015	$3.96 Billion
2016	$4.83 Billion

Year	Total Receivables
2013	$210 Million
2014	$280 Million
2015	$434 Million
2016	$623 Million

Receivables are growing faster than revenue. Revenue roughly doubled from 2013 to 2016 (2x), but receivables nearly tripled (3x). DSRI(the first ratio in the eight ratio formula) is designed to catch this. Customers are taking longer to pay (receivables) compared to how fast the sales are growing (revenue).

Year	Cost of Goods Sold
2013	$1.19 Billion
2014	$1.57 Billion
2015	$2.05 Billion
2016	$2.58 Billion

Year	Revenue	        Cost of Goods Sold	    Cost of goods sold as % of Revenue
2013	$2.08 Billion	$1.19 Billion	           57%
2014	$3.00 Billion	$1.57 Billion	           52%
2015	$3.96 Billion	$2.05 Billion	           52%
2016	$4.83 Billion	$2.58 Billion	           53%

Year	Current Assets
2013	$1.12 Billion
2014	$1.54 Billion
2015	$1.49 Billion
2016	$1.96 Billion


Year	Net Property, Plant and Equipment (NPP&E)
2013	$223 Million
2014	$305 Million
2015	$538 Million
2016	$804 Million

For depreciation, the standard EDGAR tag Depreciation only returned data for 2016. I used DepreciationAndAmortization instead, which covers all 4 years. This tag combines depreciation (loss of value of physical assets) and amortization (loss of value of intangible assets like patents) into one number. For Beneish M-Score purposes this is acceptable since the formula is looking for changes in the rate of expensing assets over time, and the combined tag captures that pattern consistently across all years.

Year	Depreciation
2013	$50 Million
2014	$72 Million
2015	$100 Million
2016	$144 Million

For total debt, no short term debt tag existed in Under Armour's EDGAR filings for this period. I used LongTermDebt as a proxy for total debt. This is a reasonable approximation since Under Armour's debt structure during 2013-2016 was primarily long term. Their debt jumped from $53M in 2013 to $828M in 2016, mostly from long term credit facilities and notes, not short term borrowings.

Year	Long Term Debt
2013	$52 Million
2014	$284 Million
2015	$669 Million
2016	$828 Million

Year	Selling, General and Administrative Expenses (SG&A)
2013	$871 Million
2014	$1.15 Billion
2015	$1.49 Billion
2016	$1.83 Billion

Year	Operating Cash Flow
2013	$120 Million
2014	$219 Million
2015	$14 Million
2016	$366 Million

The ratios: 
•	DSRI (Days' Sales in Receivables Index) = (This year's Receivables ÷ This year's Revenue) ÷ (Last year's Receivables ÷ Last year's Revenue)
•	GMI (Gross Margin Index) = (Revenue − COGS) ÷ Revenue = Gross Margin of year X, then Gross Margin of last year/Gross margin of this year
•	AQI (Asset Quality Index) = 1 − [(Current Assets + Net PP&E) ÷ Total Assets] = Asset Quality of year X, then asset quality of this year/asset quality of last year
•	SGI (Sales Growth Index) = This year's Revenue ÷ Last year's Revenue
•	DEPI (Depreciation Index) = Depreciation ÷ (Depreciation + Net PP&E)
•	SGAI (Selling, General and Administrative Expenses Index) = SG&A ÷ Revenue
•	LVGI (Leverage Index) = Total Debt ÷ Total Assets
•	TATA (Total Accruals to Total Assets) = (Operating Cash Flow) ÷ Total Assets

Need to calculate 2 DSRI values, one for 2014 (using 2013 as last year) and one for 2016 (using 2015 as last year).
How to read a Beneish ratio result using DSRI as an example:
Every ratio in the Beneish M-Score compares "this year" against "last year" by dividing two fractions. The result always reads the same way:
•	Below 1.0 = this year looks better or unchanged compared to last year. No flag.
•	Equal to 1.0 = nothing changed between years. Perfectly normal.
•	Above 1.0 = something grew faster than it should have. The higher above 1.0, the more suspicious.
The 1.0 benchmark isn’t random. It falls out naturally from the math. If receivables and revenue both grew at exactly the same rate, the two fractions would be identical, and identical ÷ identical = 1.0. So, 1.0 literally means "no change."

DSRI 2014:
Step 1: calculate receivables as a fraction of revenue for each year:
•	2013: $209,952,000 ÷ $2,082,500,000 = 0.1008 (about 10 cents of every dollar in sales was unpaid)
•	2014: $279,835,000 ÷ $2,997,916,000 = 0.0933 (about 9.3 cents of every dollar in sales was unpaid)

Step 2: divide this year by last year:
•	DSRI = 0.0933 ÷ 0.1008 = 0.926
Since 0.0933 is smaller than 0.1008, the result is below 1.0, meaning customers were actually paying slightly faster in 2014 than in 2013. No flag. This makes sense since 2014 was a clean year for Under Armour.


DSRI 2016:
Step 1: calculate receivables as a fraction of revenue for each year:
•	2015: $433,638,000 ÷ $3,963,313,000 = 0.1094 (about 10.9 cents of every dollar in sales was unpaid)
•	2016: $622,685,000 ÷ $4,833,338,000 = 0.1288 (about 12.9 cents of every dollar in sales was unpaid)

Step 2: divide this year by last year:
•	DSRI = 0.1288 ÷ 0.1094 = 1.177
Since 0.1288 is larger than 0.1094, the result is above 1.0, meaning customers were taking longer to pay in 2016 relative to how fast sales were growing. This is a flag. In Under Armour's case, this is consistent with their revenue pull-forward scheme. They were recording sales on paper before the cash actually came in, causing unpaid receivables to pile up faster than real revenue growth.

DSRI Results:
•	2014: 0.926. This is below 1.0, no suspicion. Receivables and revenue growing at a healthy rate.
•	2016: 1.177. This is above 1.0, flag raised. Receivables growing 18% faster than revenue, suggesting sales may be recorded before cash is actually collected. Consistent with Under Armour's confirmed revenue pull-forward scheme. 
•	A DSRI above 1.0 in 2016 is consistent with Under Armour's actual misconduct. They were recording sales earlier than they should have, causing unpaid receivables to pile up faster than real revenue growth.

GMI Results:
•	2014: 0.896; below 1.0, no flag. Gross margin improved slightly from 2013 to 2014, meaning no financial pressure building.
•	2016: 1.033; marginally above 1.0, weak flag. Gross margin deteriorated very slightly in 2016 vs 2015. Not a strong signal on its own. GMI measures financial pressure (motive) rather than direct manipulation. Under Armour's margins stayed relatively stable throughout this period, suggesting their fraud was about timing of revenue recognition rather than hiding margin deterioration.

AQI Results:
•	2014: 0.804 — below 1.0, no flag. Asset quality improved from 2013 to 2014.
•	2016: 0.830 — below 1.0, no flag. Asset quality remained healthy in 2016. Under Armour's fraud did not involve shifting costs into intangible or hard-to-verify assets — their manipulation was specifically about revenue timing, not asset misclassification.

SGI Results:
•	2014: 1.440. Sales grew 44% from 2013 to 2014. Strong growth, high motive to maintain streak.
•	2016: 1.220, sales grew 22% from 2015 to 2016. Still strong but slowing down; exactly the kind of deceleration that would pressure management to manipulate numbers to meet expectations.

DEPI Results:
•	2014: 0.965. Below 1.0, no flag. Depreciation rate slightly increased, normal.
•	2016: 1.035. Marginally above 1.0, very weak flag. Company depreciated assets very slightly slower in 2016 vs 2015. Not a meaningful signal on its own.

SGAI Results:
•	2014: 0.923. Below 1.0, no flag. SG&A expenses grew slightly slower than revenue in 2014. Healthy cost management.
•	2016: 1.003. Essentially 1.0, no meaningful flag. SG&A and revenue grew at almost identical rates in 2016.

LVGI Results:
•	2014: 4.044. This is extremely high. Under Armour's debt jumped from $53M in 2013 to $284M in 2014; a massive relative increase. This reflects a deliberate expansion strategy (borrowing to fund growth) rather than financial distress, so context matters here. Worth noting as a structural change in the company rather than a pure fraud signal.
•	2016: 0.974. Below 1.0, no flag. Debt grew slower than assets in 2016, leverage actually improved slightly.

TATA Results:
•	2014: -0.063. Negative TATA means operating cash flow exceeded net income, which is actually healthy. Real cash coming in matches or exceeds reported profit.
•	2016: -0.072. Also negative, same story. No flag. Interestingly Under Armour's cash generation stayed relatively honest even while they manipulated revenue timing, their TATA doesn't betray them here.


The below code calculates all the ratios needed for the beneish formula.
# ============================================
# SECTION 2: CALCULATING ALL RATIOS
# ============================================



