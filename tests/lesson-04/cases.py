"""Lesson 4.'s workbook tests: the solution, the workbook as published, and the common mistakes.

Published as tests/lesson-04/cases.py in team-simmer/data-analysis-in-python and run by
tests/run_tests.py, which provides replace(cells, starts, old, new). Each case is
(name, cells, order, expected lines in the check's output).
"""

CLEAN = "✅ Every cell in this session ran once"
DONE = "Everything matches, in a clean run"


def twice(cells):
    """Run every cell, then the check again: the check should warn that it has run before."""
    return list(range(1, len(cells) + 1)) + [len(cells)]


def cases(load):
    # 4.1 Calculate 2025's CTR and CPC
    book, solved = load("4.1-google-ads-metrics.ipynb"), load("4.1-google-ads-metrics.ipynb", solved=True)
    yield "4.1 solution", solved, None, [CLEAN, "✅ ads_2025 has 2025's 3,796 rows", "✅ Google Ads spent $198,630.66 in 2025", "✅ 2025's CTR is 1.21% and its CPC $0.58", "✅ top_cpc's most expensive day", DONE]
    yield "4.1 as published", book, None, ["❌ ads_2025 isn't a DataFrame yet", "❌ total_spend should be", "❌ top_cpc isn't a DataFrame yet"]
    yield "4.1 micros not divided", replace(solved, "ads_2025 =", 'ads_2025["cost_micros"] / 1_000_000', 'ads_2025["cost_micros"]'), None, ["❌ ads_2025's spend is still in micros", "❌ total_spend is 198,630,660,000"]
    yield "4.1 mean of row rates", replace(solved, "total_spend =", 'ads_2025["clicks"].sum() / ads_2025["impressions"].sum()', 'ads_2025["ctr"].mean()'), None, ["❌ overall_ctr is 2.95%, the average of the rows' CTRs"]
    yield "4.1 ctr as a percentage", replace(solved, "total_spend =", 'ads_2025["clicks"].sum() / ads_2025["impressions"].sum()', 'ads_2025["clicks"].sum() / ads_2025["impressions"].sum() * 100'), None, ["❌ overall_ctr is 1.21: a percentage"]
    yield "4.1 cpc mean", replace(solved, "total_spend =", 'ads_2025["spend"].sum() / ads_2025["clicks"].sum()', 'ads_2025["cpc"].mean()'), None, ["❌ overall_cpc is $0.50, the average of the rows' CPCs"]
    yield "4.1 top_cpc lowest first", replace(solved, "top_cpc =", 'nlargest(5, "cpc")', 'nsmallest(5, "cpc")'), None, ["❌ top_cpc's first CPC is 0.0806"]
    yield "4.1 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # 4.2 Group Q3 2025's sessions by channel
    book, solved = load("4.2-channel-groups.ipynb"), load("4.2-channel-groups.ipynb", solved=True)
    yield "4.2 solution", solved, None, [CLEAN, "✅ channel_group() follows Foundations topic 12.3's spec", "✅ sessions has a channel_group column with the nine groups", "✅ No row is Unassigned", "✅ Organic Social had 16,652 sessions and Paid Video 35,517", DONE]
    yield "4.2 as published", book, None, ["❌ channel_group isn't a function yet", "❌ sessions has no channel_group column yet"]
    old = replace(solved, "SOCIAL_SITES =", '    if medium == "display":\n        return "Display"\n', "")
    old = replace(old, "SOCIAL_SITES =", '    if medium == "video":\n        return "Paid Video"\n', "")
    yield "4.2 topic 5.3's function", old, None, ["❌ channel_group() has no rule for Display or Paid Video", "❌ sessions has 8 channel groups", "❌ unassigned_rows is 774"]
    yield "4.2 standardized source", replace(solved, "def row_channel_group", 'row["session_source"]', 'row["source"]'), None, ["❌ sessions has no Organic Social, and Referral has 26,247 sessions", "❌ organic_social_sessions is 0"]
    yield "4.2 not_in_crm as a list", replace(solved, "unassigned_rows =", "set(sessions[\"channel_group\"].unique()) - CUSTOMER_CHANNELS", "[group for group in sessions[\"channel_group\"].unique() if group not in CUSTOMER_CHANNELS]"), None, ["❌ not_in_crm should be a set"]
    yield "4.2 unassigned rows as a table", replace(solved, "unassigned_rows =", '(sessions["channel_group"] == "Unassigned").sum()', 'sessions[sessions["channel_group"] == "Unassigned"]'), None, ["❌ unassigned_rows is a DataFrame, not a number"]

    # 4.3 Total Q4 2024 by channel
    book, solved = load("4.3-channel-totals.ipynb"), load("4.3-channel-totals.ipynb", solved=True)
    yield "4.3 solution", solved, None, [CLEAN, "✅ by_channel has the nine groups", "✅ Direct brought in the most revenue in Q4 2024, and Email converted 6.89%", "✅ Paid search's top three", DONE]
    yield "4.3 as published", book, None, ["❌ by_channel isn't a DataFrame yet", "❌ top_channel should be", "❌ top_search_campaigns isn't a Series yet"]
    yield "4.3 mean instead of sum", replace(solved, "by_channel =", '{"sessions": "sum", "transactions": "sum", "revenue": "sum"}', '{"sessions": "mean", "transactions": "mean", "revenue": "mean"}'), None, ["❌ by_channel's Direct sessions is 298.47"]
    rates = replace(solved, "by_channel =", 'by_channel = sessions.groupby("channel_group").agg({"sessions": "sum", "transactions": "sum", "revenue": "sum"})\nby_channel["conversion_rate"] = by_channel["transactions"] / by_channel["sessions"]',
                    'rated = sessions.assign(conversion_rate=sessions["transactions"] / sessions["sessions"])\nby_channel = rated.groupby("channel_group").agg({"sessions": "sum", "transactions": "sum", "revenue": "sum", "conversion_rate": "mean"})')
    yield "4.3 mean of row rates", rates, None, ["❌ Email's conversion_rate is 0.0666"]
    yield "4.3 sorted by sessions", replace(solved, "by_channel =", 'sort_values("revenue", ascending=False)', 'sort_values("sessions", ascending=False)'), None, ["❌ by_channel should be sorted by revenue", "❌ top_channel is Organic Search"]
    yield "4.3 campaigns as a DataFrame", replace(solved, "paid_search =", 'groupby("session_campaign")["revenue"].sum().nlargest(3)', 'groupby("session_campaign").sum(numeric_only=True).nlargest(3, "revenue")'), None, ["❌ top_search_campaigns is a DataFrame"]
    yield "4.3 campaigns from every channel", replace(solved, "paid_search =", 'paid_search.groupby', 'sessions.groupby'), None, ["❌ top_search_campaigns has ['(direct)', '(organic)', '2024_us_email_newsletter']"]

    # 4.4 Report H1 2025's conversion rate
    book, solved = load("4.4-conversion-rate.ipynb"), load("4.4-conversion-rate.ipynb", solved=True)
    yield "4.4 solution", solved, None, [CLEAN, "✅ Three days: the mean of the rates is 4.67%", "✅ daily has the 181 days", "✅ The six months converted 2.54%. The mean of the daily rates says 2.50%", "✅ The mean of the rows says 1.85%, and it skipped 1,185", DONE]
    yield "4.4 as published", book, None, ["❌ mini_mean_rate and mini_pooled_rate should be numbers", "❌ daily isn't a DataFrame yet"]
    yield "4.4 pooled is the mean", replace(solved, "daily =", 'pooled_rate = sessions["transactions"].sum() / sessions["sessions"].sum()', 'pooled_rate = daily["conversion_rate"].mean()'), None, ["❌ pooled_rate is 2.50%, the mean of the daily rates"]
    yield "4.4 weighted is the plain mean", replace(solved, "daily =", 'weighted_rate = (daily["conversion_rate"] * daily["sessions"]).sum() / daily["sessions"].sum()', 'weighted_rate = daily["conversion_rate"].mean()'), None, ["❌ weighted_rate is the plain mean of the daily rates"]
    yield "4.4 daily by date and channel", replace(solved, "daily =", 'sessions.groupby("date")', 'sessions.groupby(["date", "session_medium"])'), None, ["❌ daily has 1,"]
    yield "4.4 skipped rows not counted", replace(solved, "row_rates =", "row_rates.isna().sum()", "(row_rates == 0).sum() * 0"), None, ["❌ skipped_rows is 0"]

    # 4.5 Reshape H1 2024 into a monthly table
    book, solved = load("4.5-monthly-table.ipynb"), load("4.5-monthly-table.ipynb", solved=True)
    yield "4.5 solution", solved, None, [CLEAN, "✅ mini went wide and came back long", "✅ monthly has the 54 month and channel rows", "✅ wide_sessions has six months and nine channels", "✅ report has one row of column names", DONE]
    yield "4.5 as published", book, None, ["❌ mini_wide isn't a DataFrame yet", "❌ sessions has no month column", "❌ wide_sessions isn't a DataFrame yet", "❌ report isn't a DataFrame yet"]
    yield "4.5 pivot_table averages", replace(solved, "wide_sessions =", ', aggfunc="sum")', ")"), None, ["❌ wide_sessions' January Direct is 307.9"]
    yield "4.5 pivot on the rows", replace(solved, "wide_sessions =", 'sessions.pivot_table(index="month", columns="channel_group", values="sessions", aggfunc="sum")', 'sessions.pivot(index="month", columns="channel_group", values="sessions")'), None, ["⚠️ A cell stopped with ValueError", "❌ wide_sessions isn't a DataFrame yet"]
    yield "4.5 columns not flattened", replace(solved, "report =", 'report.columns = [f"{group} {metric}" for metric, group in report.columns]\n', ""), None, ["❌ report's column names still have two levels"]
    yield "4.5 names reversed", replace(solved, "report =", 'f"{group} {metric}"', 'f"{metric} {group}"'), None, ["❌ report's columns are named like \"sessions Email\""]
    yield "4.5 melt without names", replace(solved, "wide_sessions =", 'melt(id_vars="month", var_name="channel_group", value_name="sessions")', 'melt(id_vars="month")'), None, ["❌ long_sessions should have the columns month, channel_group and sessions"]

    # 4.6 Deliver Q4 2025's channel report in Excel
    book, solved = load("4.6-excel-report.ipynb"), load("4.6-excel-report.ipynb", solved=True)
    yield "4.6 solution", solved, None, [CLEAN, "✅ by_channel and monthly_rates have the quarter's channels", "✅ The Channels sheet has the nine groups", "✅ The Conversion by month sheet has three months of rates as percentages: Email's December is 9.22%", "✅ Every column on both sheets is 16 wide", DONE]
    yield "4.6 as published", book, None, ["❌ by_channel should have the nine channel groups", "❌ q4_2025_channels.xlsx hasn't been written in this session"]
    yield "4.6 rates times 100", replace(solved, "with pd.ExcelWriter", 'by_channel.to_excel(writer, sheet_name="Channels")', 'by_channel.assign(conversion_rate=by_channel["conversion_rate"] * 100).to_excel(writer, sheet_name="Channels")'), None, ["❌ The Channels sheet's Email conversion rate is 7.95: it was multiplied by 100"]
    yield "4.6 index left out", replace(solved, "with pd.ExcelWriter", 'by_channel.to_excel(writer, sheet_name="Channels")', 'by_channel.to_excel(writer, sheet_name="Channels", index=False)'), None, ["❌ The Channels sheet has no channel names"]
    yield "4.6 revenue not formatted", replace(solved, "with pd.ExcelWriter", '    format_column(channels, "revenue", "$#,##0.00")\n', ""), None, ["❌ Some Channels columns don't have their number format: revenue is General"]
    yield "4.6 rates sheet not formatted", replace(solved, "with pd.ExcelWriter", '    for group in monthly_rates.columns:\n        format_column(rates, group, "0.00%")\n', ""), None, ["❌ Some rates on the Conversion by month sheet aren't formatted as 0.00%"]
    yield "4.6 no widths", replace(solved, "with pd.ExcelWriter", "            sheet.column_dimensions[column[0].column_letter].width = 16", "            pass"), None, ["❌ Some columns on Channels, Conversion by month are narrower than 16"]
    yield "4.6 rates averaged", replace(solved, "by_channel =", 'monthly_rates = monthly.pivot(index="month", columns="channel_group", values="conversion_rate")', 'monthly_rates = sessions.assign(rate=sessions["transactions"] / sessions["sessions"]).pivot_table(index="month", columns="channel_group", values="rate")'), None, ["❌ monthly_rates' December Email is"]

    # Final exercise: Build and deliver the monthly channel report
    book, solved = load("4-monthly-channel-report.ipynb"), load("4-monthly-channel-report.ipynb", solved=True)
    yield "final solution", solved, None, [CLEAN, "✅ sessions has the nine channel groups", "✅ monthly has 240 rows", "✅ Over both years, 2.60% of sessions converted", "✅ channel_report_2024_2025.xlsx has both years, every number matches the store's data, and it's formatted: November 2024's Email converted 7.71%, and the store 3.21%", DONE]
    yield "final as published", book, None, ["❌ sessions needs a channel_group column"]
    old = replace(solved, "SOCIAL_SITES =", '    if medium == "display":\n        return "Display"\n', "")
    old = replace(old, "SOCIAL_SITES =", '    if medium == "video":\n        return "Paid Video"\n', "")
    old = replace(old, "SOCIAL_SITES =", "assert set(", "set(")
    yield "final topic 5.3's function", old, None, ["❌ sessions has 6,200 Unassigned rows, and no Display or Paid Video", "❌ monthly has 216 rows, 9 channel groups with the Total", "❌ The 2024 sheet has Unassigned columns"]
    yield "final standardized source", replace(replace(solved, "SOCIAL_SITES =", 'row["session_source"]', 'row["source"]'), "SOCIAL_SITES =", "assert set(", "set("), None, ["❌ sessions has no Organic Social"]
    yield "final no CRM check", replace(solved, "SOCIAL_SITES =", "assert set(sessions[\"channel_group\"].unique()) <= CUSTOMER_CHANNELS, set(sessions[\"channel_group\"].unique()) - CUSTOMER_CHANNELS\n", ""), None, ["❌ Your groups are right, but nothing in your notebook checks them against CUSTOMER_CHANNELS"]
    yield "final no Total", replace(replace(solved, "by_group =", "monthly = pd.concat([by_group, totals], ignore_index=True)", "monthly = by_group.copy()"), "by_group =", 'assert monthly.loc[monthly["channel_group"] == "Total", "sessions"].sum() == sessions["sessions"].sum()\n', ""), None, ["❌ monthly has 216 rows and no Total", "❌ The 2024 sheet has no Total sessions, Total revenue, Total conversion rate column"]
    days = 'days = sessions.groupby("date")[["sessions", "transactions"]].sum()\noverall_rate = (days["transactions"] / days["sessions"]).mean()'
    yield "final overall rate from daily rates", replace(solved, "by_group =", 'overall_rate = sessions["transactions"].sum() / sessions["sessions"].sum()', days), None, ["❌ overall_rate is 2.48%, the mean of 731 daily rates"]
    daily = ('report.shape', 'days = sessions.groupby(["month", "channel_group", "date"])[["sessions", "transactions"]].sum()\n'
             'daily_mean = (days["transactions"] / days["sessions"]).groupby(level=["month", "channel_group"]).mean().unstack()\n'
             'for group in daily_mean.columns:\n    report[f"{group} conversion rate"] = daily_mean[group]\nreport.shape')
    yield "final group rates from daily rates", replace(solved, "report =", *daily), None, ["❌ The 2024 sheet's Direct conversion rate is the mean of its daily rates"]
    groups = '["Direct", "Display", "Email", "Organic Search", "Organic Social", "Paid Search", "Paid Social", "Paid Video", "Referral"]'
    yield "final total rate from channel rates", replace(solved, "report =", "report.shape", f'report["Total conversion rate"] = report[[f"{{group}} conversion rate" for group in {groups}]].mean(axis=1)\nreport.shape'), None, ["❌ The 2024 sheet's Total conversion rate is the mean of the nine channels' rates"]
    yield "final rates times 100", replace(solved, "by_group =", 'monthly["conversion_rate"] = monthly["transactions"] / monthly["sessions"]', 'monthly["conversion_rate"] = monthly["transactions"] / monthly["sessions"] * 100'), None, ["❌ The 2024 sheet's Direct conversion rate is multiplied by 100"]
    yield "final no formats", replace(solved, "def format_column", "                    format_column(sheet, header, number_format)", "                    pass"), None, ["❌ Some columns on the 2024 sheet don't have their number format, such as Direct sessions (General)"]
    yield "final index left out", replace(solved, "def format_column", ".to_excel(writer, sheet_name=year)", ".to_excel(writer, sheet_name=year, index=False)"), None, ["❌ The 2024 sheet should have 2024's twelve months as rows"]
    yield "final narrow columns", replace(solved, "def format_column", "            sheet.column_dimensions[column[0].column_letter].width = 16", "            pass"), None, ["❌ Some columns on the 2024 sheet are narrower than 16"]
