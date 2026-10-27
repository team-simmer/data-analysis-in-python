"""Lesson 8.'s workbook tests: the solution, the workbook as published, and the common mistakes.

Published as tests/lesson-08/cases.py in team-simmer/data-analysis-in-python and run by
tests/run_tests.py, which provides replace(cells, starts, old, new). Each case is
(name, cells, order, expected lines in the check's output).
"""

CLEAN = "✅ Every cell in this session ran once"
DONE = "Everything matches, in a clean run"


def twice(cells):
    """Run every cell, then the check again: the check should warn that it has run before."""
    return list(range(1, len(cells) + 1)) + [len(cells)]


def cases(load):
    # 8.1 Chart Q2 2024's sessions and revenue
    book, solved = load("8.1-line-and-bar-charts.ipynb"), load("8.1-line-and-bar-charts.ipynb", solved=True)
    yield "8.1 solution", solved, None, [CLEAN, "✅ The line chart has the 91 days' sessions, from 2,002 on May 3 to 3,605 on June 25", "✅ The bar chart has nine channels, sorted, with $95,553.73 on top and $7,153.24 at the bottom", DONE]
    yield "8.1 as published", book, None, ["❌ daily_sessions should be a Series", "❌ channel_revenue should be a Series"]
    yield "8.1 pandas plot", replace(solved, "daily_sessions =", 'fig, trend_ax = plt.subplots(figsize=(10, 4))\ntrend_ax.plot(daily_sessions.index, daily_sessions)', 'trend_ax = daily_sessions.plot(figsize=(10, 4))'), None, ["✅ The line chart has the 91 days' sessions", DONE]
    yield "8.1 every row plotted", replace(solved, "daily_sessions =", "trend_ax.plot(daily_sessions.index, daily_sessions)", 'trend_ax.plot(sessions["date"], sessions["sessions"])'), None, ["❌ trend_ax's line has 5,149 points"]
    yield "8.1 no title", replace(solved, "daily_sessions =", 'trend_ax.set_title("Daily sessions, Q2 2024")\n', ""), None, ["❌ trend_ax has no title"]
    yield "8.1 no y label", replace(solved, "daily_sessions =", 'trend_ax.set_ylabel("Sessions")\n', ""), None, ["❌ trend_ax has no y-axis label"]
    yield "8.1 vertical bars", replace(solved, "channel_revenue =", "sort_values().plot.barh(", "sort_values().plot.bar("), None, ["❌ channel_ax's bars are vertical"]
    yield "8.1 unsorted bars", replace(solved, "channel_revenue =", "channel_revenue.sort_values().plot.barh(", "channel_revenue.plot.barh("), None, ["❌ channel_ax's bars aren't sorted by value"]
    yield "8.1 biggest at the bottom", replace(solved, "channel_revenue =", "sort_values()", "sort_values(ascending=False)"), None, ["❌ channel_ax's biggest bar is at the bottom"]
    yield "8.1 sessions bars", replace(solved, "channel_revenue =", 'channel_revenue.sort_values()', 'sessions.groupby("channel_group")["sessions"].sum().sort_values()'), None, ["❌ channel_ax's bars add up to 214,756"]
    seaborn = replace(solved, "channel_revenue =", "channel_revenue.sort_values().plot.barh(ax=channel_ax)", 'import seaborn as sns\nordered = channel_revenue.sort_values(ascending=False)\nsns.barplot(x=ordered.values, y=ordered.index, ax=channel_ax)')
    yield "8.1 seaborn bars", seaborn, None, ["✅ The bar chart has nine channels, sorted", DONE]
    yield "8.1 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # 8.2 Find 2025's unusual traffic days
    book, solved = load("8.2-unusual-days.ipynb"), load("8.2-unusual-days.ipynb", solved=True)
    yield "8.2 solution", solved, None, [CLEAN, "✅ A typical day in 2025 had 3,614 sessions", "✅ 13 days above the fence of 5,924 sessions, from November 21 to December 9, led by November 28 with 14,786", "✅ The histogram counts the 365 days in 30 bins, with the fence at 5,924 sessions", DONE]
    yield "8.2 as published", book, None, ["❌ typical_day should be a number", "❌ q1, q3, lower_fence and upper_fence should be numbers", "❌ hist_ax should be the Axes"]
    yield "8.2 mean, not median", replace(solved, "typical_day =", '.median()', '.mean()'), None, ["❌ typical_day is 3,922.51"]
    yield "8.2 quartiles of rows", replace(solved, "q1, q3 =", 'q1, q3 = daily["sessions"]', 'q1, q3 = sessions["sessions"]'), None, ["❌ The fences come from the sessions table's rows"]
    yield "8.2 swapped quartiles", replace(solved, "q1, q3 =", "quantile([0.25, 0.75])", "quantile([0.75, 0.25])"), None, ["❌ q1 and q3 are swapped"]
    yield "8.2 three standard deviations", replace(solved, "q1, q3 =", "upper_fence = q3 + 1.5 * iqr", 'upper_fence = daily["sessions"].mean() + 3 * daily["sessions"].std()'), None, ["❌ upper_fence is 7,678.14: that's the mean plus three standard deviations"]
    yield "8.2 three IQRs", replace(solved, "q1, q3 =", "upper_fence = q3 + 1.5 * iqr", "upper_fence = q3 + 3 * iqr"), None, ["❌ upper_fence is 7,544"]
    yield "8.2 revenue outliers", replace(solved, "q1, q3 =", 'outlier_days = daily[daily["sessions"] > upper_fence]', 'rq1, rq3 = daily["revenue"].quantile([0.25, 0.75])\noutlier_days = daily[daily["revenue"] > rq3 + 1.5 * (rq3 - rq1)]'), None, ["❌ The outlier_days table has 38 days"]
    yield "8.2 histogram of rows", replace(solved, "fig, hist_ax =", 'hist_ax.hist(daily["sessions"], bins=30)', 'hist_ax.hist(sessions["sessions"], bins=30)'), None, ["❌ hist_ax's histogram counts 21,880 values"]
    yield "8.2 no fence line", replace(solved, "fig, hist_ax =", 'hist_ax.axvline(upper_fence, color="red", linestyle="--", label=f"Outlier fence: {upper_fence:,.0f}")\n', ""), None, ["❌ hist_ax has no vertical line at upper_fence"]
    yield "8.2 seaborn histogram", replace(solved, "fig, hist_ax =", 'hist_ax.hist(daily["sessions"], bins=30)', 'sns.histplot(x=daily["sessions"], bins=30, ax=hist_ax)'), None, ["✅ The histogram counts the 365 days in 30 bins", DONE]
    yield "8.2 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # 8.3 Test 2025's spend and revenue
    book, solved = load("8.3-spend-and-revenue.ipynb"), load("8.3-spend-and-revenue.ipynb", solved=True)
    yield "8.3 solution", solved, None, [CLEAN, "✅ The scatter plot has 365 days", "✅ Spend and revenue correlate at 0.7777 over the year", "transactions and revenue the strongest pair at 0.9562", "✅ In August and September, spend and revenue correlate at -0.0119", DONE]
    yield "8.3 as published", book, None, ["❌ scatter_ax should be the Axes", "❌ correlations should be a DataFrame", "❌ quiet_r should be a number"]
    yield "8.3 axes swapped", replace(solved, "fig, scatter_ax =", 'scatter_ax.scatter(daily["spend"], daily["revenue"]', 'scatter_ax.scatter(daily["revenue"], daily["spend"]'), None, ["❌ scatter_ax has revenue on the x axis"]
    yield "8.3 pandas scatter", replace(solved, "fig, scatter_ax =", 'scatter_ax.scatter(daily["spend"], daily["revenue"], alpha=0.5)', 'daily.plot.scatter(x="spend", y="revenue", alpha=0.5, ax=scatter_ax)'), None, ["✅ The scatter plot has 365 days", DONE]
    yield "8.3 no axis labels", replace(solved, "fig, scatter_ax =", 'scatter_ax.set_ylabel("Revenue ($)")\n', ""), None, ["❌ scatter_ax needs a label on both axes"]
    yield "8.3 sessions table", replace(solved, "correlations =", "correlations = daily.corr()", "correlations = sessions.corr(numeric_only=True)"), None, ["❌ The correlations table has no spend column"]
    yield "8.3 no annotations", replace(solved, "correlations =", "annot=True, ", ""), None, ["❌ heatmap_ax's cells have no numbers in them"]
    yield "8.3 spend and sessions", replace(solved, "correlations =", 'daily["spend"].corr(daily["revenue"])', 'daily["spend"].corr(daily["sessions"])'), None, ["❌ spend_revenue_r is 0.9063"]
    yield "8.3 quiet is the year", replace(solved, "quiet =", 'daily.loc["2025-08-01":"2025-09-30"]', "daily"), None, ["❌ quiet_r is 0.7777"]
    yield "8.3 August only", replace(solved, "quiet =", '"2025-09-30"', '"2025-08-31"'), None, ["❌ quiet_r is one month's correlation"]
    yield "8.3 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # 8.4 Build Q1 2025's channel figure
    book, solved = load("8.4-stakeholder-figure.ipynb"), load("8.4-stakeholder-figure.ipynb", solved=True)
    yield "8.4 solution", solved, None, [CLEAN, "✅ Nine conversion rates, from Paid Video's 0.64% to Email's 6.22%, and 12 full weeks of sessions, 304,708 in all", "✅ report_fig has the rates, sorted from 0 with percentage ticks, and the 12 weeks", "✅ q1_2025_channels.png is saved", DONE]
    yield "8.4 as published", book, None, ["❌ conversion_by_channel should be a Series", "❌ report_fig should be the Figure", "❌ q1_2025_channels.png hasn't been saved in this session"]
    yield "8.4 average of row rates", replace(solved, "by_channel =", 'by_channel = sessions.groupby("channel_group")[["sessions", "transactions"]].sum()\nconversion_by_channel = by_channel["transactions"] / by_channel["sessions"]', 'conversion_by_channel = (sessions["transactions"] / sessions["sessions"]).groupby(sessions["channel_group"]).mean()'), None, ["❌ conversion_by_channel's Email rate is 5.77%"]
    yield "8.4 rates in percent", replace(solved, "by_channel =", 'by_channel["transactions"] / by_channel["sessions"]', 'by_channel["transactions"] / by_channel["sessions"] * 100'), None, ["❌ conversion_by_channel is in percent"]
    yield "8.4 partial weeks", replace(solved, "by_channel =", '.resample("W").sum()[days == 7]', '.resample("W").sum()'), None, ["❌ weekly_sessions has 14 weeks"]
    yield "8.4 axis not from zero", replace(solved, "report_fig, (rate_ax", 'rate_ax.set_ylabel("")', 'rate_ax.set_ylabel("")\nrate_ax.set_xlim(left=0.005)'), None, ["❌ rate_ax's value axis starts at 0.0050"]
    yield "8.4 no percent ticks", replace(solved, "report_fig, (rate_ax", 'rate_ax.xaxis.set_major_formatter("{x:.0%}")\n', ""), None, ["❌ rate_ax's ticks aren't percentages"]
    yield "8.4 no headline", replace(solved, "report_fig, (rate_ax", 'report_fig.suptitle("Q1 2025: Email converted at 6.2%, ten times Paid Video\'s rate", fontsize=14, x=0.01, ha="left")\n', ""), None, ["❌ report_fig has no headline"]
    yield "8.4 two figures", replace(solved, "report_fig, (rate_ax", 'report_fig, (rate_ax, weekly_ax) = plt.subplots(1, 2, figsize=(13, 4.5))', 'report_fig, rate_ax = plt.subplots(figsize=(6.5, 4.5))\nweekly_fig, weekly_ax = plt.subplots(figsize=(6.5, 4.5))'), None, ["❌ report_fig should have two Axes"]
    yield "8.4 blank file", replace(solved, "report_fig.savefig(", "report_fig.savefig(REPORT_FILE", "plt.savefig(REPORT_FILE"), None, ["❌ q1_2025_channels.png is blank"]
    yield "8.4 not saved", replace(solved, "report_fig.savefig(", 'report_fig.savefig(REPORT_FILE, dpi=150, bbox_inches="tight")', "pass"), None, ["❌ q1_2025_channels.png hasn't been saved in this session"]
    yield "8.4 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # 8.5 Fix the first-half deck's charts
    book, solved = load("8.5-honest-charts.ipynb"), load("8.5-honest-charts.ipynb", solved=True)
    yield "8.5 solution", solved, None, [CLEAN, "✅ Both years on one scale from 0: the first half of 2025 brought 46.8% more revenue", "✅ Average order value from $72.10 to $82.33, on bars from 0: Direct's orders are 14% bigger than Paid Social's, not the 10 times", DONE]
    yield "8.5 as published", book, None, ["❌ monthly_revenue should be a DataFrame", "❌ aov_by_channel should be a Series"]
    yield "8.5 pivot averages", replace(solved, "monthly_revenue =", ', aggfunc="sum")', ")"), None, ["❌ The monthly_revenue table should have six months and two years"]
    yield "8.5 years as rows", replace(solved, "monthly_revenue =", 'index=sessions["date"].dt.month, columns=sessions["date"].dt.year', 'index=sessions["date"].dt.year, columns=sessions["date"].dt.month'), None, ["❌ The monthly_revenue table has the years as rows"]
    yield "8.5 growth backwards", replace(solved, "monthly_revenue =", "totals[2025] / totals[2024]", "totals[2024] / totals[2025]"), None, ["❌ growth is -0.3189"]
    yield "8.5 one year plotted", replace(solved, "monthly_revenue =", "monthly_revenue.plot(ax=years_ax", "monthly_revenue[2025].plot(ax=years_ax"), None, ["❌ years_ax has one line"]
    yield "8.5 years axis not from zero", replace(solved, "monthly_revenue =", "years_ax.set_ylim(bottom=0)\n", ""), None, ["❌ years_ax's y axis starts at"]
    yield "8.5 both years' AOV", replace(solved, "first_half =", 'sessions[sessions["date"].dt.year == 2025]', "sessions"), None, ["❌ aov_by_channel's Direct is $81.44"]
    yield "8.5 AOV truncated", replace(solved, "first_half =", "aov_ax.set_xlim(left=0)", "aov_ax.set_xlim(left=71)"), None, ["❌ aov_ax's value axis starts at $71.00, so Direct's bar is 10.3 times Paid Social's, for a difference of 14%"]
    yield "8.5 AOV unsorted", replace(solved, "first_half =", "aov_by_channel.sort_values().plot.barh(", "aov_by_channel.plot.barh("), None, ["❌ aov_ax's bars should be sorted"]
    yield "8.5 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # 8.6 Chart H2 2024's channels by week
    book, solved = load("8.6-interactive-chart.ipynb"), load("8.6-interactive-chart.ipynb", solved=True)
    yield "8.6 solution", solved, None, [CLEAN, "✅ 234 rows: 26 full weeks of 9 channel groups, from the week ending July 7 to the one ending December 29", "✅ channel_fig has nine channels of 26 weeks", "The busiest week ended December 1, 2024", "✅ weekly_channels_h2_2024.html is saved", DONE]
    yield "8.6 as published", book, None, ["❌ weekly_channels should be a DataFrame", "❌ channel_fig should be a Plotly figure", "❌ weekly_channels_h2_2024.html hasn't been saved"]
    yield "8.6 partial week", replace(solved, "weekly_channels =", 'weekly_channels = weekly_channels[weekly_channels["date"].isin(full_weeks)]\n', ""), None, ["❌ The weekly_channels table has 243 rows"]
    yield "8.6 no reset_index", replace(solved, "weekly_channels =", ".resample(\"W\").sum().reset_index()", ".resample(\"W\").sum()"), None, ["❌ The weekly_channels table should have the columns date, channel_group, sessions and revenue"]
    yield "8.6 every row plotted", replace(solved, "channel_fig =", "px.line(weekly_channels,", "px.line(sessions,"), None, ["❌ channel_fig plots 10,974 points"]
    yield "8.6 no color", replace(solved, "channel_fig =", ' color="channel_group",', ""), None, ["❌ channel_fig should have nine traces"]
    yield "8.6 no hover revenue", replace(solved, "channel_fig =", ' hover_data=["revenue"],', ""), None, ["❌ channel_fig's hover box has no revenue"]
    yield "8.6 peak row number", replace(solved, "channel_fig =", 'weekly_channels.groupby("date")["sessions"].sum().idxmax()', 'weekly_channels["sessions"].idxmax()'), None, ["That's a row number"]
    yield "8.6 not saved", replace(solved, "channel_fig.write_html(", "channel_fig.write_html(CHART_FILE)", "pass"), None, ["❌ weekly_channels_h2_2024.html hasn't been saved"]
    yield "8.6 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # Final exercise: Explore the orders and back up three findings
    book, solved = load("8-orders-findings.ipynb"), load("8-orders-findings.ipynb", solved=True)
    yield "final solution", solved, None, [CLEAN, "✅ 2,246 orders above $214.99, worth $604,781.19: 11.1% of the valid orders' revenue, with 3.44 items each against 1.54", "✅ Return rates by category run from 12.0% (Outerwear) to 13.6% (Sweaters): 1.6 percentage points apart", "✅ num_items and subtotal correlate at 0.7955", "✅ findings_fig has the 12 return rates", "✅ orders_findings.png is saved", DONE]
    yield "final as published", book, None, ["❌ orders should be the orders file", "❌ item_rows should be", "❌ correlations should be a 4 × 4 table", "❌ findings_fig should be the Figure", "❌ orders_findings.png hasn't been saved"]
    yield "final cancelled kept", replace(solved, "valid_orders =", 'valid_orders = orders[orders["status"] != "Cancelled"]', "valid_orders = orders"), None, ["❌ The valid_orders table has all 65,106 orders", "❌ The correlations table includes the cancelled orders", "❌ value_ax's histogram counts 65,106 orders"]
    yield "final fence on total", replace(solved, "valid_orders =", 'q1, q3 = valid_orders["subtotal"]', 'q1, q3 = valid_orders["total"]'), None, ["❌ upper_fence is 219.62"]
    yield "final cancelled lines", replace(solved, "item_rows =", 'item_rows = item_rows[item_rows["status"] != "Cancelled"]\n', ""), None, ["❌ The item_rows table has 92,723 rows"]
    department = replace(solved, "item_rows =", 'products[["product_id", "category"]]', 'products[["product_id", "category", "department"]]')
    yield "final by department", replace(department, "item_rows =", 'groupby(item_rows["category"])', 'groupby(item_rows["department"])'), None, ["❌ return_rates is by department"]
    yield "final rates in percent", replace(solved, "item_rows =", ".mean()", ".mean() * 100"), None, ["❌ return_rates is in percent"]
    yield "final formula pair", replace(solved, "correlations =", 'strongest_pair = ("num_items", "subtotal")\nstrongest_r = correlations.loc["num_items", "subtotal"]', 'strongest_pair = ("subtotal", "total")\nstrongest_r = correlations.loc["subtotal", "total"]'), None, ["❌ strongest_pair is subtotal and total, 0.9992"]
    yield "final negative pair", replace(solved, "correlations =", 'strongest_pair = ("num_items", "subtotal")', 'strongest_pair = ("subtotal", "shipping")'), None, ["❌ strongest_pair is subtotal and shipping, -0.7417"]
    yield "final truncated rates", replace(solved, "findings_fig, (rate_ax", "rate_ax.set_xlim(left=0)", "rate_ax.set_xlim(left=0.115)"), None, ["❌ rate_ax's value axis starts at 11.5%, so Sweaters' bar is 4.3 times Outerwear's, for rates 1.6 points apart"]
    yield "final unsorted rates", replace(solved, "findings_fig, (rate_ax", "return_rates.sort_values().plot.barh(", "return_rates.plot.barh("), None, ["❌ rate_ax's bars should be sorted"]
    yield "final no fence line", replace(solved, "findings_fig, (rate_ax", 'value_ax.axvline(upper_fence, color="red", linestyle="--", label=f"Outlier fence: ${upper_fence:,.2f}")\n', ""), None, ["❌ value_ax has no vertical line at upper_fence"]
    blank = replace(solved, "findings_fig, (rate_ax", 'findings_fig.savefig(FIGURE_FILE, dpi=150, bbox_inches="tight")\n', "")
    yield "final blank file", blank[:-1] + ["plt.savefig(FIGURE_FILE)"] + blank[-1:], None, ["❌ orders_findings.png is blank"]
    yield "final check run twice", solved, twice(solved), ["⚠️ This cell has run before"]
