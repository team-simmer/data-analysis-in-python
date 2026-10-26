"""Lesson 6.'s workbook tests: the solution, the workbook as published, and the common mistakes.

Published as tests/lesson-06/cases.py in team-simmer/data-analysis-in-python and run by
tests/run_tests.py, which provides replace(cells, starts, old, new). Each case is
(name, cells, order, expected lines in the check's output).
"""

CLEAN = "✅ Every cell in this session ran once"
DONE = "Everything matches, in a clean run"


def twice(cells):
    """Run every cell, then the check again: the check should warn that it has run before."""
    return list(range(1, len(cells) + 1)) + [len(cells)]


def cases(load):
    # 6.1 Measure the summer sale's lift
    book, solved = load("6.1-summer-sale.ipynb"), load("6.1-summer-sale.ipynb", solved=True)
    yield "6.1 solution", solved, None, [CLEAN, "✅ The daily table has 61 days", "✅ The sale has 18 days, June 20 to July 7", "✅ During the sale, the store had 43% more sessions and 67% more revenue per day, and converted 3.55% of sessions instead of 2.25%", DONE]
    yield "6.1 as published", book, None, ["❌ daily isn't a DataFrame yet", "❌ sale should be the daily table's rows", "❌ session_lift, revenue_lift, sale_rate, before_rate, sale_weekend_days, before_weekend_days should be numbers"]
    yield "6.1 dates not the index", replace(solved, "daily =", 'groupby("date")', 'groupby("date", as_index=False)'), None, ["❌ The daily table's index is a RangeIndex"]
    yield "6.1 end left out", replace(solved, "sale =", "daily.loc[SALE_START:SALE_END]", "daily.loc[SALE_START:SALE_END - pd.Timedelta(days=1)]"), None, ["❌ The sale table has 17 rows and ends on July 6"]
    yield "6.1 sale_days one short", replace(solved, "sale =", "(SALE_END - SALE_START).days + 1", "(SALE_END - SALE_START).days"), None, ["❌ sale_days is 17"]
    yield "6.1 windows share a day", replace(solved, "sale =", "SALE_START - pd.Timedelta(days=1)]", "SALE_START]"), None, ["❌ The before table ends on June 20"]
    yield "6.1 lift without minus 1", replace(solved, "session_lift =", 'before["sessions"].mean() - 1', 'before["sessions"].mean()'), None, ["❌ session_lift is 1.43"]
    yield "6.1 mean of daily rates", replace(solved, "session_lift =", 'sale_rate = sale["transactions"].sum() / sale["sessions"].sum()', 'sale_rate = (sale["transactions"] / sale["sessions"]).mean()'), None, ["❌ sale_rate or before_rate is the mean of the days' rates"]
    yield "6.1 Sundays only", replace(solved, "session_lift =", "day_of_week >= 5", "day_of_week > 5"), None, ["❌ The weekend counts are 3 and 2"]
    yield "6.1 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # 6.2 Report Q2 2025 by week and month
    book, solved = load("6.2-weekly-and-monthly.ipynb"), load("6.2-weekly-and-monthly.ipynb", solved=True)
    yield "6.2 solution", solved, None, [CLEAN, "✅ The weekly table has the 12 full weeks", "✅ The monthly table has April, May and June", "✅ Revenue's 7-day average peaks at the end of June", DONE]
    yield "6.2 as published", book, None, ["❌ days_per_week should be a Series", "❌ monthly isn't a DataFrame yet", "❌ revenue_7d should be a Series"]
    yield "6.2 partial weeks kept", replace(solved, "days_per_week =", "weekly = weekly[days_per_week == 7].copy()\n", ""), None, ["❌ The weekly table has 14 weeks"]
    yield "6.2 weeks averaged", replace(solved, "days_per_week =", 'daily.resample("W").sum()', 'daily.resample("W").mean()'), None, ["❌ The weekly table's first week has $5,898.97 of revenue"]
    rates = ('weekly["conversion_rate"] = weekly["transactions"] / weekly["sessions"]',
             'weekly["conversion_rate"] = (daily["transactions"] / daily["sessions"]).resample("W").mean()')
    yield "6.2 mean of daily rates", replace(solved, "days_per_week =", *rates), None, ["❌ The weekly table's conversion_rate is the mean of the days' rates"]
    yield "6.2 months by their last day", replace(solved, "monthly =", '"MS"', '"ME"'), None, ["❌ The monthly table's months are labelled by their last day"]
    yield "6.2 months as text", replace(solved, "monthly =", 'daily.resample("MS").sum()', 'daily.groupby(daily.index.strftime("%Y-%m")).sum()'), None, ["❌ The monthly table's labels are ['2025-04', '2025-05', '2025-06']"]
    yield "6.2 min_periods=1", replace(solved, "revenue_7d =", "rolling(7)", "rolling(7, min_periods=1)"), None, ["❌ revenue_7d has no NaN"]
    yield "6.2 centered", replace(solved, "revenue_7d =", "rolling(7)", "rolling(7, center=True)"), None, ["❌ revenue_7d is NaN on June 30"]
    yield "6.2 rolling sum", replace(solved, "revenue_7d =", "rolling(7).mean()", "rolling(7).sum()"), None, ["❌ revenue_7d is the 7-day total"]
    yield "6.2 best week's revenue", replace(solved, "revenue_7d =", "idxmax()", "max()"), None, ["❌ best_week is the best week's revenue"]
    yield "6.2 best week as a table", replace(solved, "revenue_7d =", 'weekly["revenue"].idxmax()', 'weekly.nlargest(1, "revenue")'), None, ["❌ best_week is a DataFrame, not the week's label"]
    yield "6.2 best week's index", replace(solved, "revenue_7d =", 'weekly["revenue"].idxmax()', 'weekly.nlargest(1, "revenue").index'), None, ["❌ best_week is a DatetimeIndex, not the week's label"]
    yield "6.2 best week as text", replace(solved, "revenue_7d =", 'weekly["revenue"].idxmax()', 'f"{weekly[\'revenue\'].idxmax():%Y-%m-%d}"'), None, ["❌ best_week is text, '2025-06-29'"]
    yield "6.2 best week by nlargest", replace(solved, "revenue_7d =", 'weekly["revenue"].idxmax()', 'weekly.nlargest(1, "revenue").index[0]'), None, ["✅ Revenue's 7-day average peaks at the end of June", DONE]

    # 6.3 Compare Q3 2025 with last year
    book, solved = load("6.3-period-comparisons.ipynb"), load("6.3-period-comparisons.ipynb", solved=True)
    yield "6.3 solution", solved, None, [CLEAN, "✅ The week ending September 28, 2025 grew most on the year before, 58.6%", "✅ September 2025's revenue is up 8.5% on August, and its conversion rate 0.06 points", "✅ July to September 2025's revenue is up 37.7%", DONE]
    yield "6.3 as published", book, None, ["❌ The weekly table should have the columns revenue_wow and revenue_yoy", "❌ The monthly table should be the provided cell's 15 months", "❌ q3_yoy should be a number"]
    yield "6.3 YoY as the week before", replace(solved, 'weekly["revenue_wow"]', "pct_change(52)", "pct_change(1)"), None, ["❌ The weekly table's revenue_yoy is the same as revenue_wow"]
    yield "6.3 YoY 53 weeks back", replace(solved, 'weekly["revenue_wow"]', "pct_change(52)", "pct_change(53)"), None, ["❌ The weekly table's revenue_yoy compares with the week 53 weeks earlier"]
    yield "6.3 WoW as a difference", replace(solved, 'weekly["revenue_wow"]', 'weekly["revenue"].pct_change()', 'weekly["revenue"].diff()'), None, ["❌ The weekly table's revenue_wow is"]
    yield "6.3 MoM as a difference", replace(solved, 'monthly["revenue_mom"]', 'monthly["revenue"].pct_change()', 'monthly["revenue"].diff()'), None, ["❌ The monthly table's revenue_mom is", "in September: that's the difference in dollars"]
    yield "6.3 best week by revenue", replace(solved, 'weekly["revenue_wow"]', 'q3_weeks["revenue_yoy"].idxmax()', 'q3_weeks["revenue"].idxmax()'), None, ["❌ best_yoy_week is the week with the most revenue"]
    yield "6.3 best week as a table", replace(solved, 'weekly["revenue_wow"]', 'q3_weeks["revenue_yoy"].idxmax()', 'q3_weeks.nlargest(1, "revenue_yoy")'), None, ["❌ best_yoy_week is a DataFrame, not the week's label"]
    yield "6.3 last year's week as a table", replace(solved, 'weekly["revenue_wow"]', "weekly.loc[best_yoy_week - pd.Timedelta(weeks=52)]", "weekly.loc[[best_yoy_week - pd.Timedelta(weeks=52)]]"), None, ["❌ last_year_week is a table with one row"]
    yield "6.3 a calendar year back", replace(solved, 'weekly["revenue_wow"]', "pd.Timedelta(weeks=52)", "pd.DateOffset(years=1)"), None, ["⚠️ A cell stopped with", "❌ last_year_week should be the weekly table's row 52 weeks before best_yoy_week"]
    yield "6.3 rate change relative", replace(solved, 'monthly["revenue_mom"]', 'monthly["conversion_rate"].diff()', 'monthly["conversion_rate"].pct_change()'), None, ["❌ The monthly table's rate_change is the relative change"]
    yield "6.3 quarter as mean of weeks", replace(solved, "q3_yoy =", 'daily.loc["2025-07":"2025-09", "revenue"].sum() / daily.loc["2024-07":"2024-09", "revenue"].sum() - 1', 'q3_weeks["revenue_yoy"].mean()'), None, ["❌ q3_yoy is 0.3883"]
    yield "6.3 quarter from weeks", replace(solved, "q3_yoy =", 'daily.loc["2025-07":"2025-09", "revenue"].sum() / daily.loc["2024-07":"2024-09", "revenue"].sum() - 1', 'q3_weeks["revenue"].sum() / weekly.loc["2024-07":"2024-09", "revenue"].sum() - 1'), None, ["❌ q3_yoy is 0.3747"]

    # Final exercise: Compare Black Friday week year over year
    book, solved = load("6-black-friday-yoy.ipynb"), load("6-black-friday-yoy.ipynb", solved=True)
    yield "final solution", solved, None, [CLEAN, "✅ The weekly table has 64 full weeks", "✅ The 7-day average of revenue on Black Friday was $21,465.39", "✅ Black Friday week 2025 against the same week of 2024: sessions up 40.6%, transactions 47.7% and revenue 43.1%", DONE]
    yield "final as published", book, None, ["❌ daily should be a DataFrame", "❌ revenue_7d should be a Series", "❌ bf_week should be"]
    calendar = replace(solved, "bf_week =", "last_year = BLACK_FRIDAY - pd.Timedelta(weeks=52)", "last_year = BLACK_FRIDAY - pd.DateOffset(years=1)")
    calendar = replace(calendar, "bf_week =", "assert list(bf_week.index.day_name()) == list(last_year_week.index.day_name())\n", "")
    yield "final a calendar year back", calendar, None, ["❌ The last_year_week table starts on November 24, 2024"]
    yield "final partial weeks kept", replace(solved, "days_per_week =", "weekly = weekly[days_per_week == 7].copy()\n", ""), None, ["❌ The weekly table has 66 weeks"]
    yield "final YoY as a difference", replace(solved, "days_per_week =", 'weekly["revenue"].pct_change(52)', 'weekly["revenue"].diff(52)'), None, ["❌ The weekly table's revenue_yoy is", "that's the difference in dollars, diff(52)"]
    yield "final YoY 53 weeks back", replace(solved, "days_per_week =", "pct_change(52)", "pct_change(53)"), None, ["❌ The weekly table's revenue_yoy compares with the week 53 weeks earlier"]
    sunday = replace(solved, "bf_week =", "pd.Timedelta(days=4)", "pd.Timedelta(days=5)")
    sunday = replace(sunday, "bf_week =", "pd.Timedelta(days=2)", "pd.Timedelta(days=1)")
    yield "final Sunday-to-Saturday week", sunday, None, ["❌ The bf_week table starts on Sunday, November 23"]
    yield "final Black Friday alone", replace(solved, "bf_week =", "bf_week_yoy = bf_week.sum() / last_year_week.sum() - 1", "bf_week_yoy = daily.loc[BLACK_FRIDAY] / daily.loc[last_year] - 1"), None, ["❌ bf_week_yoy's revenue is 0.398"]
    yield "final centered average", replace(solved, "revenue_7d =", "rolling(7)", "rolling(7, center=True)"), None, ["❌ revenue_7d is centered"]
    yield "final check run twice", solved, twice(solved), ["⚠️ This cell has run before"]
