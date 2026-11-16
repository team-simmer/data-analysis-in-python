"""Lesson 16.'s workbook tests: the solution, the workbook as published, and the common mistakes.

Published as tests/lesson-16/cases.py in team-simmer/data-analysis-in-python and run by
tests/run_tests.py, which provides replace(cells, starts, old, new). Each case is
(name, cells, order, expected lines in the check's output).
"""

CLEAN = "✅ Every cell in this session ran once"
DONE = "Everything matches, in a clean run"


def twice(cells):
    """Run every cell, then the check again: the check should warn that it has run before."""
    return list(range(1, len(cells) + 1)) + [len(cells)]


def cases(load):
    # 16.1 Source the budget data
    book, solved = load("16.1-source-the-data.ipynb"), load("16.1-source-the-data.ipynb", solved=True)
    yield "16.1 solution", solved, None, [CLEAN, "✅ 13,862 campaign days and $571,200.03 of spend", "✅ Every campaign day has its revenue and its channel group: $1,216,642.52", "✅ 2,924 rows: 4 channel groups × 731 days", "✅ 3 checks pass, and an assert stops the notebook", DONE]
    yield "16.1 as published", book, None, ["❌ spend should be a DataFrame", "❌ campaign_days should be a DataFrame", "❌ channel_days should be a DataFrame", "❌ checks should be a dictionary"]
    yield "16.1 micros", replace(solved, "google =", " / 1_000_000", ""), None, ["❌ The spend table's spend adds up to", "cost_micros are millionths"]
    yield "16.1 ad sets, no validate", replace(replace(solved, "google =", 'spend = spend.groupby(["date", "campaign"], as_index=False)["spend"].sum()\n', ""), "revenue =", ', validate="one_to_one"', ""), None, ["❌ The spend table has 21,536 rows", "❌ campaign_days has 21,536 rows"]
    yield "16.1 ad sets, validate", replace(solved, "google =", 'spend = spend.groupby(["date", "campaign"], as_index=False)["spend"].sum()\n', ""), None, ["⚠️ A cell stopped with", "❌ The spend table has 21,536 rows"]
    yield "16.1 spend key", replace(solved, "google =", 'spend["campaign"] = campaign_key(spend["campaign"])\n', ""), None, ["⚠️ A cell stopped with AssertionError", "❌ Some campaign names in the spend table have spaces or capital letters"]
    yield "16.1 no channel groups", replace(solved, "revenue =", ".str[2].map(CHANNEL_GROUPS)", ".str[2]"), None, ["❌ channel_group should be one of the four budget lines"]
    yield "16.1 all sessions", replace(solved, "organic =", 'sessions[sessions["session_medium"] == "organic"]', "sessions"), None, ["❌ The organic column has every session of the day"]
    yield "16.1 index", replace(solved, "organic =", 'groupby(["channel_group", "date"], as_index=False)', 'groupby(["channel_group", "date"])'), None, ["❌ channel_days should be a DataFrame"]
    yield "16.1 no bool", replace(solved, "checks =", 'bool(campaign_days["revenue"].notna().all())', 'campaign_days["revenue"].notna().all()'), None, ["❌ Each check should be True or False"]
    yield "16.1 no assert", replace(solved, "checks =", "assert all(checks.values()), checks\n", ""), None, ["❌ Make a failure stop the notebook"]
    yield "16.1 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # 16.2 Model every channel's next dollar
    book, solved = load("16.2-marginal-returns.ipynb"), load("16.2-marginal-returns.ipynb", solved=True)
    yield "16.2 solution", solved, None, [CLEAN, "✅ Paid Search on its own: each extra dollar comes with $1.98", "✅ The next dollar brings the most in Paid Search, $1.98, and the least in Paid Social, $0.55, though Paid Social's ROAS is 2.02", DONE]
    yield "16.2 as published", book, None, ["❌ search_weekly should be a DataFrame", "❌ returns should be a DataFrame"]
    yield "16.2 search no control", replace(solved, "search_days =", '"revenue ~ spend + organic"', '"revenue ~ spend"'), None, ["❌ search_model's spend coefficient is 3.193"]
    yield "16.2 search partial week", replace(solved, "search_days =", "search_weekly = search_weekly[days == 7]\n", ""), None, ["❌ search_weekly has 105 rows"]
    yield "16.2 no control", replace(solved, "rows = []", '"revenue ~ spend + organic"', '"revenue ~ spend"'), None, ["❌ Paid Search's marginal return is 3.19, more than its ROAS of 2.38"]
    yield "16.2 partial week passes", replace(solved, "rows = []", "    weekly = weekly[days == 7]\n", ""), None, ["✅ The next dollar brings the most in Paid Search, $1.91"]
    yield "16.2 unsorted", replace(solved, "rows = []", '.sort_values("marginal_return", ascending=False)', ""), None, ["❌ Sort the returns table by marginal_return"]
    yield "16.2 sorted by roas", replace(solved, "rows = []", '.sort_values("marginal_return", ascending=False)', '.sort_values("roas", ascending=False)'), None, ["❌ Sort the returns table by marginal_return"]
    yield "16.2 roas reversed", replace(solved, "rows = []", 'weekly["revenue"].sum() / weekly["spend"].sum()', 'weekly["spend"].sum() / weekly["revenue"].sum()'), None, ["❌ Paid Search's roas is 0.4199"]
    yield "16.2 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # 16.3 Deliver the budget report
    book, solved = load("16.3-budget-report.ipynb"), load("16.3-budget-report.ipynb", solved=True)
    yield "16.3 solution", solved, None, [CLEAN, "✅ budget_report() works for a period of the check's choosing: from July 2024 to June 2025, the next dollar brings the most in Paid Search, $2.24", "✅ report is topic 16.2.'s table: from Paid Search's $1.98 down to Paid Social's $0.55", "✅ Move budget from Paid Social to Paid Search", "✅ Each year on its own: Paid Search $1.81 and $2.37, Paid Social $0.53 and $0.57. Both years point the same way.", "✅ The chart shows each channel group's next dollar with its interval", DONE]
    yield "16.3 as published", book, None, ["❌ budget_report should be a function", "❌ report should be budget_report", "❌ more_budget and less_budget should be the names", "❌ report_2024 and report_2025 should be", "❌ report_ax should be the Axes"]
    yield "16.3 reads START and END", replace(solved, "def budget_report", 'channel_days["date"].between(start, end)', 'channel_days["date"].between(START, END)'), None, ["❌ budget_report(channel_days, \"2024-07-01\", \"2025-06-30\") returns the table for 2024 and 2025"]
    yield "16.3 less by ROAS", replace(solved, "more_budget,", "report.index[-1]", 'report["roas"].idxmin()'), None, ["❌ less_budget is Display, the channel group with the lowest ROAS"]
    yield "16.3 reversed", replace(solved, "more_budget,", "report.index[0], report.index[-1]", "report.index[-1], report.index[0]"), None, ["❌ more_budget and less_budget are the wrong way round"]
    yield "16.3 not confident", replace(solved, "more_budget,", 'confident = bool(report.loc[more_budget, "return_low"] > report.loc[less_budget, "return_high"])', "confident = False"), None, ["❌ confident is False"]
    yield "16.3 year with a partial week", replace(solved, "report_2024 =", '"2025-01-01", "2025-12-31"', '"2024-12-30", "2025-12-31"'), None, ["❌ report_2024 and report_2025 should cover one year each"]
    yield "16.3 errors from the unsorted table", replace(solved, "chart =", 'errors = [chart["marginal_return"] - chart["return_low"], chart["return_high"] - chart["marginal_return"]]', 'errors = [report["marginal_return"] - report["return_low"], report["return_high"] - report["marginal_return"]]'), None, ["❌ Each bar should have its interval as an error bar"]
    yield "16.3 no error bars", replace(solved, "chart =", "plot.barh(xerr=errors)", "plot.barh()"), None, ["❌ Each bar should have its interval as an error bar"]
    yield "16.3 highest at the bottom", replace(solved, "chart =", 'chart = report.sort_values("marginal_return")', "chart = report"), None, ["❌ Put the highest marginal return on top"]
    yield "16.3 inverted axis passes", replace(replace(solved, "chart =", 'chart = report.sort_values("marginal_return")', "chart = report"), "chart =", "plt.show()", "report_ax.invert_yaxis()\nplt.show()"), None, ["✅ The chart shows each channel group's next dollar", DONE]
    yield "16.3 no title", replace(solved, "chart =", "report_ax.set_title(\"Paid Search's next dollar brings the most, Paid Social's the least\")\n", ""), None, ["❌ The chart has no title"]
    yield "16.3 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]
