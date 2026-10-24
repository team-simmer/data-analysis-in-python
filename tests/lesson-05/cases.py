"""Lesson 5.'s workbook tests: the solution, the workbook as published, and the common mistakes.

Published as tests/lesson-05/cases.py in team-simmer/data-analysis-in-python and run by
tests/run_tests.py, which provides replace(cells, starts, old, new). Each case is
(name, cells, order, expected lines in the check's output).
"""

CLEAN = "✅ Every cell in this session ran once"
DONE = "Everything matches, in a clean run"


def twice(cells):
    """Run every cell, then the check again: the check should warn that it has run before."""
    return list(range(1, len(cells) + 1)) + [len(cells)]


def cases(load):
    # 5.1 Combine 2025's ad spend
    book, solved = load("5.1-spend-table.ipynb"), load("5.1-spend-table.ipynb", solved=True)
    yield "5.1 solution", solved, None, [CLEAN, "✅ google_std, meta_std and youtube_std have the standard columns", "✅ The spend table has 2025's 10,754 rows", "✅ 2025's spend: Google Ads $198,630.66", "✅ The three platforms spent $318,705.08 in 2025", DONE]
    yield "5.1 as published", book, None, ["❌ google_std isn't a DataFrame yet", "❌ spend isn't a DataFrame yet", "❌ spend_by_platform isn't a Series yet", "❌ total_spend should be"]
    yield "5.1 micros not divided", replace(solved, "def standard_columns", 'google_std["cost_micros"] / 1_000_000', 'google_std["cost_micros"]'), None, ["❌ The google_std table's spend is still in micros", "❌ The spend table's spend adds up to"]
    yield "5.1 extra columns", replace(solved, "def standard_columns", "google_std = standard_columns(google_std)\n", ""), None, ["❌ The google_std table has columns that aren't standard: ['campaign_id', 'cost_micros']"]
    yield "5.1 Meta clicks not renamed", replace(solved, "def standard_columns", '"Link clicks": "clicks", ', ""), None, ["❌ The meta_std table has no clicks column", "❌ The spend table has missing values in clicks"]
    yield "5.1 ad_set on Google Ads", replace(solved, "def standard_columns", 'google_std["platform"] = "Google Ads"\n', 'google_std["platform"] = "Google Ads"\ngoogle_std["ad_set"] = None\n'), None, ["❌ The google_std table has an ad_set column, but Google Ads has no ad sets"]
    yield "5.1 both years", replace(solved, "spend = pd.concat", 'spend = spend[spend["date"].dt.strftime("%Y") == "2025"].reset_index(drop=True)\n', ""), None, ["❌ The spend table has 21,536 rows: both years"]
    yield "5.1 index not reset", replace(solved, "spend = pd.concat", '== "2025"].reset_index(drop=True)', '== "2025"]'), None, ["❌ The spend table should be numbered from 0"]
    yield "5.1 by platform as a DataFrame", replace(solved, "spend_by_platform =", 'spend.groupby("platform")["spend"].sum()', 'spend.groupby("platform")[["spend"]].sum()'), None, ["❌ spend_by_platform is a DataFrame"]
    yield "5.1 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # 5.2 Calculate Q4 2024's Google Ads ROAS
    book, solved = load("5.2-google-ads-roas.ipynb"), load("5.2-google-ads-roas.ipynb", solved=True)
    yield "5.2 solution", solved, None, [CLEAN, "✅ The revenue table has the quarter's 2,551 campaign-days", "✅ The joined table has the spend table's 1,008 rows", "✅ Google Ads' ROAS for Q4 2024 is 2.51", "✅ The best ROAS, 9.59, is 2024_ca_display_blackfriday", DONE]
    yield "5.2 as published", book, None, ["❌ revenue isn't a DataFrame yet", "❌ joined isn't a DataFrame yet", "❌ roas should be", "❌ by_campaign isn't a DataFrame yet"]
    yield "5.2 key not renamed", replace(solved, "revenue =", 'revenue = revenue.rename(columns={"session_campaign": "campaign"})\n', ""), None, ["❌ The revenue table still has a session_campaign column", "⚠️ A cell stopped with"]
    yield "5.2 joined on the campaign alone", replace(solved, "joined =", 'on=["date", "campaign"]', 'on="campaign"'), None, ["❌ The joined table has 86,264 rows and columns ending in _x and _y: it was joined on campaign alone"]
    yield "5.2 right join", replace(solved, "joined =", 'how="left"', 'how="right"'), None, ["❌ The joined table has 2,551 rows"]
    yield "5.2 mean of daily ROAS", replace(solved, "joined =", 'roas = joined["revenue"].sum() / joined["spend"].sum()', 'roas = (joined["revenue"] / joined["spend"]).mean()'), None, ["❌ roas is 3.04, the mean of the 1,008 daily ROASes"]
    yield "5.2 spend over revenue", replace(solved, "joined =", 'roas = joined["revenue"].sum() / joined["spend"].sum()', 'roas = joined["spend"].sum() / joined["revenue"].sum()'), None, ["❌ roas is 0.40: spend over revenue"]
    yield "5.2 every refund day", replace(solved, "joined =", 'roas = joined["revenue"].sum() / joined["spend"].sum()', 'roas = sessions.loc[sessions["session_campaign"].isin(spend["campaign"]), "revenue"].sum() / spend["spend"].sum()'), None, ["❌ roas is 2.47"]
    rates = ('by_campaign["roas"] = by_campaign["revenue"] / by_campaign["spend"]',
             'by_campaign["roas"] = joined.assign(roas=joined["revenue"] / joined["spend"]).groupby("campaign")["roas"].mean()')
    yield "5.2 campaign ROAS from daily ROAS", replace(solved, "by_campaign =", *rates), None, ["❌ The by_campaign table's roas should be each campaign's total revenue over its total spend"]
    yield "5.2 worst is the first", replace(solved, "by_campaign =", "by_campaign.index[-1]", "by_campaign.index[0]"), None, ["❌ worst_campaign should be the name of the campaign with the lowest ROAS"]

    # 5.3 Fix Q3 2025's campaign keys
    book, solved = load("5.3-campaign-keys.ipynb"), load("5.3-campaign-keys.ipynb", solved=True)
    yield "5.3 solution", solved, None, [CLEAN, "✅ Four names don't match", "✅ 474 rows of spend found no revenue: $13,965.82", "✅ Every campaign matches after the fix, and YouTube's ROAS is 1.48", DONE]
    yield "5.3 as published", book, None, ["❌ unmatched_names isn't a set yet", "❌ check should be the spend table joined to the revenue table", "❌ campaign_key isn't a function yet"]
    yield "5.3 difference reversed", replace(solved, "unmatched_names =", 'set(spend["campaign"]) - set(revenue["campaign"])', 'set(revenue["campaign"]) - set(spend["campaign"])'), None, ["❌ unmatched_names has 12 names, such as (direct) and (organic)"]
    yield "5.3 names as a list", replace(solved, "unmatched_names =", 'unmatched_names = set(spend["campaign"]) - set(revenue["campaign"])', 'unmatched_names = sorted(set(spend["campaign"]) - set(revenue["campaign"]))'), None, ["❌ unmatched_names has the right four names, but it should be a set"]
    yield "5.3 YouTube's spend only", replace(solved, "check =", 'check.loc[check["_merge"] == "left_only", "spend"]', 'check.loc[(check["_merge"] == "left_only") & (check["platform"] == "YouTube"), "spend"]'), None, ["❌ spend_lost is 12,102.60: YouTube's only"]
    yield "5.3 strip only", replace(solved, "def campaign_key", "names.str.strip().str.lower()", "names.str.strip()"), None, ["❌ campaign_key() should strip spaces and lowercase"]
    yield "5.3 revenue not fixed", replace(solved, "def campaign_key", 'revenue["campaign"] = campaign_key(revenue["campaign"])\n', ""), None, ["❌ The spend table's names are fixed, but nothing in your notebook runs campaign_key() on the revenue table's"]
    yield "5.3 ROAS from the old join", replace(solved, "def campaign_key", 'joined = spend.merge(revenue, on=["date", "campaign"], how="left")', "joined = check"), None, ["❌ youtube_roas is 0"]

    # 5.4 Report Q4 2025's Meta ROAS
    book, solved = load("5.4-meta-roas.ipynb"), load("5.4-meta-roas.ipynb", solved=True)
    yield "5.4 solution", solved, None, [CLEAN, "✅ The social team's 4.81 comes from 1,648 ad-set rows joined to 640 campaign-days: 1,008 rows repeat a key", "✅ Meta's ROAS for Q4 2025 is 1.90", "✅ 2025_ca_instagram_blackfriday leads with 4.42", DONE]
    yield "5.4 as published", book, None, ["❌ naive should be the spend table joined to the revenue table", "❌ meta_daily isn't a DataFrame yet", "❌ by_campaign isn't a DataFrame yet"]
    yield "5.4 whole rows compared", replace(solved, "naive =", 'spend.duplicated(["date", "campaign"])', "spend.duplicated()"), None, ["❌ repeated_keys is 0"]
    yield "5.4 every repeated row", replace(solved, "naive =", 'spend.duplicated(["date", "campaign"])', 'spend.duplicated(["date", "campaign"], keep=False)'), None, ["❌ repeated_keys is 1,648"]
    yield "5.4 grouped by ad set", replace(solved, "meta_daily =", 'groupby(["date", "campaign"]', 'groupby(["date", "campaign", "ad_set"]'), None, ["⚠️ A cell stopped with", "❌ The meta_daily table has 1,648 rows: it's still one row per ad set"]
    yield "5.4 no validate", replace(solved, "meta_daily =", ', validate="one_to_one"', ""), None, ["❌ The joined table is right, but no merge in your notebook says validate=\"one_to_one\""]
    yield "5.4 campaigns from the naive join", replace(solved, "by_campaign =", 'joined.groupby("campaign")', 'naive.groupby("campaign")'), None, ["❌ The by_campaign table's revenue adds up to $126,901.38"]

    # Final exercise: Calculate ROAS by platform and campaign
    book, solved = load("5-roas-by-platform.ipynb"), load("5-roas-by-platform.ipynb", solved=True)
    yield "final solution", solved, None, [CLEAN, "✅ The spend table has both years of all three platforms, $571,200.03", "✅ The campaign_days table has 13,862 campaign-days", "✅ ROAS for 2024 and 2025: Google Ads 2.28, Meta 2.02 and YouTube 1.62", "✅ 84 campaigns", DONE]
    yield "final as published", book, None, ["❌ spend isn't a DataFrame yet", "❌ campaign_days isn't a DataFrame yet", "❌ roas_by_platform should be", "❌ roas_by_campaign should be"]
    micros = replace(solved, "def standard_columns", 'google_std["cost_micros"] / 1_000_000', 'google_std["cost_micros"]')
    micros = replace(micros, "def standard_columns", 'assert round(spend.loc[spend["platform"] == "Google Ads", "spend"].sum(), 2) == round(google["cost_micros"].sum() / 1_000_000, 2)\n', "")
    yield "final micros", micros, None, ["❌ Google Ads' spend in the spend table is in the billions", "❌ Google Ads' ROAS is almost 0"]
    keys = replace(solved, "revenue =", 'spend["campaign"] = campaign_key(spend["campaign"])\nrevenue["campaign"] = campaign_key(revenue["campaign"])\n', "")
    keys = replace(keys, "revenue =", 'assert set(spend["campaign"]) <= set(revenue["campaign"]), set(spend["campaign"]) - set(revenue["campaign"])', "")
    keys = replace(keys, "daily =", 'assert campaign_days["revenue"].notna().all()\n', "")
    yield "final raw keys", keys, None, ["❌ 19 of the spend table's campaign names aren't in the revenue table", "❌ 2,728 rows of the campaign_days table have no revenue", "❌ YouTube's ROAS is 0"]
    naive = replace(solved, "daily =", 'daily = spend.groupby(["date", "platform", "campaign"], as_index=False)[["impressions", "clicks", "spend"]].sum()', "daily = spend")
    naive = replace(naive, "daily =", ', validate="one_to_one"', "")
    yield "final naive Meta join", naive, None, ["❌ The campaign_days table has 21,536 rows: one per Meta ad set", "❌ Meta's ROAS is 5.22: the naive merge"]
    outer = replace(solved, "daily =", 'how="left"', 'how="outer"')
    outer = replace(outer, "daily =", "assert len(campaign_days) == len(daily)\nassert campaign_days[\"revenue\"].notna().all()\nassert round(campaign_days[\"spend\"].sum(), 2) == round(spend[\"spend\"].sum(), 2)\n", "")
    yield "final outer join", outer, None, ["❌ The campaign_days table has 18,956 rows, but there are 13,862 campaign-days with spend"]
    yield "final no validate", replace(solved, "daily =", ', validate="one_to_one"', ""), None, ["❌ The campaign_days table is right, but no merge in your notebook says validate=\"one_to_one\""]
    mean = ('roas_by_platform["roas"] = roas_by_platform["revenue"] / roas_by_platform["spend"]',
            'roas_by_platform["roas"] = campaign_days.assign(roas=campaign_days["revenue"] / campaign_days["spend"]).groupby("platform")["roas"].mean()')
    yield "final mean of daily ROAS", replace(solved, "roas_by_platform =", *mean), None, ["❌ Google Ads' ROAS is 2.50: a mean of the campaigns' or the days' ROASes"]
    yield "final campaigns unsorted", replace(solved, "roas_by_platform =", 'roas_by_campaign = roas_by_campaign.sort_values("roas", ascending=False)\n', ""), None, ["❌ The roas_by_campaign table should be sorted by roas, highest first"]
