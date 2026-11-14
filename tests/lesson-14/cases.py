"""Lesson 14.'s workbook tests: the solution, the workbook as published, and the common mistakes.

Published as tests/lesson-14/cases.py in team-simmer/data-analysis-in-python and run by
tests/run_tests.py, which provides replace(cells, starts, old, new). Each case is
(name, cells, order, expected lines in the check's output).

Topic 14.1.'s third cell is the code Gemini writes. The tests use the solution's version of it,
and the mistakes an assistant makes without the definitions: a mean of the rows' rates and
dropping the refund rows.
"""

CLEAN = "✅ Every cell in this session ran once"
DONE = "Everything matches, in a clean run"

TOTALS_RATE = 'channels["conversion_rate"] = channels["transactions"] / channels["sessions"]'
ROW_MEAN_RATE = ('channels["conversion_rate"] = (sessions["transactions"] / sessions["sessions"])'
                 '.groupby(sessions["channel_group"]).mean().loc[channels["channel_group"]].values')
DAILY_MEAN_CHANNELS = '''daily = sessions.groupby(["channel_group", "date"], as_index=False)[["sessions", "transactions", "revenue"]].sum()
daily["conversion_rate"] = daily["transactions"] / daily["sessions"]
channels = daily.groupby("channel_group", as_index=False).agg(
    sessions=("sessions", "sum"), transactions=("transactions", "sum"),
    revenue=("revenue", "sum"), conversion_rate=("conversion_rate", "mean"))'''


def twice(cells):
    """Run every cell, then the check again: the check should warn that it has run before."""
    return list(range(1, len(cells) + 1)) + [len(cells)]


def cases(load):
    # 14.1 Get Q2 2025's channel report from Gemini: parameters 1, sessions 2, channel groups 3, ✏️ 4-6, check 7
    book, solved = load("14.1-channels-with-gemini.ipynb"), load("14.1-channels-with-gemini.ipynb", solved=True)
    yield "14.1 solution", solved, None, [CLEAN, "✅ describe_table() describes any table", "✅ Your prompt describes the table", "✅ 9 channel groups, with 287,371 sessions", DONE]
    yield "14.1 as published", book, None, ["❌ describe_table should be a function", "❌ context should be describe_table(sessions)", "❌ channels should be a DataFrame"]
    yield "14.1 no text values", replace(solved, "def describe_table", 'lines.append(f"- {column} ({values.dtype}): {values.nunique()} different values, such as {examples}")', 'lines.append(f"- {column} ({values.dtype})")'), None, ["❌ Text columns should show how many different values"]
    yield "14.1 no context in prompt", replace(solved, "prompt =", "{context}", ""), None, ["❌ prompt should be text with context in it"]
    yield "14.1 mean of rows", replace(solved, "# The kind of code", TOTALS_RATE, ROW_MEAN_RATE), None, ["❌ The conversion rates aren't each channel group's transactions divided by its sessions"]
    yield "14.1 refunds dropped", replace(solved, "# The kind of code", "channels = sessions.groupby", 'channels = sessions[sessions["revenue"] >= 0].groupby'), None, ["❌ The revenue is $640,317.47"]
    yield "14.1 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # 14.2 Check an AI-written channel report: parameters 1, sessions 2, channel groups 3, AI 4, ✏️ 5-7, check 8
    book, solved = load("14.2-check-ai-report.ipynb"), load("14.2-check-ai-report.ipynb", solved=True)
    yield "14.2 solution", solved, None, [CLEAN, "✅ The AI's report has $62,637.66 too much revenue", "✅ The AI's rates aren't transactions divided by sessions", "✅ The report has 9 channel groups", DONE]
    yield "14.2 as published", book, None, ["❌ revenue_gap should be a number", "❌ rate_gap should be a Series", "❌ report should be a DataFrame"]
    yield "14.2 gap reversed", replace(solved, "revenue_gap =", 'ai_report["revenue"].sum() - sessions["revenue"].sum()', 'sessions["revenue"].sum() - ai_report["revenue"].sum()'), None, ["❌ revenue_gap has the right size, but it's negative"]
    yield "14.2 rate_gap without index", replace(solved, "by_channel =", 'ai_report.set_index("channel_group")', "ai_report"), None, ["❌ rate_gap's index should be the channel groups"]
    yield "14.2 report keeps the filter", replace(solved, "report =", "report = sessions.groupby", 'report = sessions[sessions["revenue"] >= 0].groupby'), None, ["❌ The report's revenue is $517,517.55"]
    yield "14.2 report mean rates", replace(solved, "report =", 'report["conversion_rate"] = report["transactions"] / report["sessions"]',
                                            'report["conversion_rate"] = ai_report.set_index("channel_group").loc[report["channel_group"], "conversion_rate"].values'), None, ["❌ The report's conversion rates are still a mean of daily rates"]

    # 14.3 Validate Q2 2024's channel report: parameters 1, sessions 2, channel groups 3, reports 4-5, ✏️ 6-8, check 9
    book, solved = load("14.3-validate-channel-report.ipynb"), load("14.3-validate-channel-report.ipynb", solved=True)
    yield "14.3 solution", solved, None, [CLEAN, "✅ validate_report() passes on the team's report with 4 checks", "✅ Every check passes for the team's report", "✅ The AI's report fails 2 checks: revenue adds up, rates from totals", DONE]
    yield "14.3 as published", book, None, ["❌ validate_report should be a function", "❌ checks should be validate_report", "❌ ai_checks should be validate_report"]
    yield "14.3 no day check", replace(solved, "def validate_report", '        "every day is there": sessions["date"].nunique() == len(pd.date_range(start, end)),\n', ""), None, ["❌ validate_report() passes when June 10 to 16 are missing"]
    yield "14.3 no revenue check", replace(solved, "def validate_report", '        "revenue adds up": bool(round(report["revenue"].sum(), 2) == round(sessions["revenue"].sum(), 2)),\n', ""), None, ["❌ validate_report() passes a report without the refund rows"]
    yield "14.3 no rate check", replace(solved, "def validate_report", '        "rates from totals": bool(((report["conversion_rate"] - report["transactions"] / report["sessions"]).abs() < 0.000001).all()),\n', ""), None, ["❌ validate_report() passes conversion rates that are 2% off"]
    yield "14.3 no assert", replace(solved, "checks =", "assert all(checks.values()), checks\n", ""), None, ["❌ Make a failure stop the notebook"]
    yield "14.3 assert on the AI's checks", replace(solved, "ai_checks =", "ai_checks = validate_report(sessions, ai_report, START, END)\n", "ai_checks = validate_report(sessions, ai_report, START, END)\nassert all(ai_checks.values()), ai_checks\n"), None, ["⚠️ An assert stopped the notebook"]
    yield "14.3 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # 14 Review an AI-written ROAS analysis: parameters 1, AI 2, channel groups 3, AI 4-6, solution 7-10, check 11
    book, solved = load("14-review-ai-roas.ipynb"), load("14-review-ai-roas.ipynb", solved=True)
    yield "14 final solution", solved, None, [CLEAN, "✅ The sessions table has every day of Q1 2025", "✅ 9 channel groups, with conversion rates from totals", "✅ ROAS by platform: Google Ads 2.47, Meta 2.33 and YouTube 1.89", "✅ validate_report() passes on your tables", DONE]
    yield "14 final as published", book, None, [CLEAN, "❌ The sessions table has 81 of Q1's 90 days", "❌ The channels table should have 9 channel groups and 324,563 sessions", "❌ Meta's ROAS is 5.83", "❌ Add topic 14.3.'s validate_report"]
    yield "14 final dates still mixed", replace(solved, "# The AI's first cell, fixed", "format=date_format", 'format="mixed"'), None, ["⚠️ Your assert stopped the notebook", "❌ The sessions table has 81 of Q1's 90 days"]
    yield "14 final mean rates", replace(solved, "# The channels cell, fixed", 'channels = sessions.groupby("channel_group", as_index=False)[["sessions", "transactions", "revenue"]].sum()\n' + TOTALS_RATE, DAILY_MEAN_CHANNELS), None, ["⚠️ Your assert stopped the notebook", "❌ The conversion rates aren't transactions divided by sessions: Email's is 6.36%"]
    yield "14 final naive merge", replace(solved, "# The platforms cell, fixed", 'campaign_days = daily_spend.merge(revenue, on=["date", "campaign"], how="left", validate="one_to_one")', 'campaign_days = spend.merge(revenue, on=["date", "campaign"], how="left")'), None, ["❌ Meta's ROAS is 6.19"]
    yield "14 final no validate", replace(solved, "# The platforms cell, fixed", ', validate="one_to_one"', ""), None, ["❌ The ROAS is right. Make the merge stop"]
    yield "14 final weak validation", replace(solved, "def validate_report", '        "rates from totals": bool(((report["conversion_rate"] - report["transactions"] / report["sessions"]).abs() < 0.000001).all()),\n', ""), None, ["❌ validate_report() passes conversion rates that aren't transactions divided by sessions"]
    yield "14 final check run twice", solved, twice(solved), ["⚠️ This cell has run before"]
