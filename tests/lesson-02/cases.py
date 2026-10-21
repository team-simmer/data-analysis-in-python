"""Lesson 2.'s workbook tests: the solution, the workbook as published, and the common mistakes.

Published as tests/lesson-02/cases.py in team-simmer/data-analysis-in-python and run by
tests/run_tests.py, which provides replace(cells, starts, old, new). Each case is
(name, cells, order, expected lines in the check's output).
"""

CLEAN = "✅ Every cell in this session ran once"
DONE = "Everything matches, in a clean run"


def twice(cells):
    """Run every cell, then the check again: the check should warn that it has run before."""
    return list(range(1, len(cells) + 1)) + [len(cells)]


def cases(load):
    # 2.1 Load April 2024's sessions with the right types
    book, solved = load("2.1-load-april.ipynb"), load("2.1-load-april.ipynb", solved=True)
    yield "2.1 solution", solved, None, [CLEAN, "✅ april has all 1,791 rows", "✅ first_date and last_date", "✅ april_revenue is $129,442.38", "✅ numeric_columns has the three", DONE]
    yield "2.1 as published", book, None, ["❌ april isn't a DataFrame yet"]
    yield "2.1 no parse_dates", replace(solved, "april = pd.read_csv", ', parse_dates=["date"]', ""), None, ["❌ april's date column is text", "❌ first_date or last_date is text"]
    yield "2.1 dtype compared with object", replace(solved, "first_date =", "if pd.api.types.is_numeric_dtype(april[column])", "if april[column].dtype != object"), None, ["❌ numeric_columns has columns that aren't numbers"]
    yield "2.1 last date cut to April", replace(solved, "first_date =", 'last_date = april["date"].max()', 'last_date = april["date"][april["date"] <= "2024-04-30"].max()'), None, ["❌ last_date should be the latest date in the file"]
    yield "2.1 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # 2.2 Profile May 2024's sessions
    book, solved = load("2.2-profile-may.ipynb"), load("2.2-profile-may.ipynb", solved=True)
    yield "2.2 solution", solved, None, [CLEAN, "✅ 1. The file has 1,791 rows", "✅ 2. The file runs to June 2", "✅ 3. 54 rows have no campaign", "✅ 4. The largest single-row revenue", "✅ 5. paid_social has the most rows", DONE]
    yield "2.2 as published", book, None, ["❌ 1. n_rows should be"]
    yield "2.2 shape swapped", replace(solved, "n_rows, n_columns", "n_rows, n_columns = may.shape", "n_columns, n_rows = may.shape"), None, ["❌ 1. n_rows and n_columns are swapped"]
    yield "2.2 non-null count", replace(solved, "may.info()", ".isna().sum()", ".notna().sum()"), None, ["❌ 3. 1,737 is the non-null count"]
    yield "2.2 revenue total", replace(solved, "max_revenue =", '["revenue"].max()', '["revenue"].sum()'), None, ["❌ 4. max_revenue is the largest value in one row"]
    yield "2.2 count instead of name", replace(solved, "top_medium =", ".index[0]", ".iloc[0]"), None, ["❌ 5. top_medium is a number"]

    # 2.3 Find July's email orders
    book, solved = load("2.3-email-orders.ipynb"), load("2.3-email-orders.ipynb", solved=True)
    yield "2.3 solution", solved, None, [CLEAN, "✅ is_email is True", "✅ mini_email_orders has rows 0, 4 and 5", "✅ july_email_orders has July's 63", "✅ july_email_orders_q has the same rows", "✅ email_orders_revenue is $28,899.78", "✅ email_orders_report has the three columns", DONE]
    yield "2.3 as published", book, None, ["❌ is_email should be a boolean mask", "❌ mini_email_orders isn't a DataFrame yet"]
    yield "2.3 and instead of &", replace(solved, "is_email =", "is_email & (", "is_email and ("), None, ["⚠️ A cell stopped with ValueError", "❌ mini_email_orders isn't a DataFrame yet. If you got"]
    yield "2.3 | instead of &", replace(solved, "is_email =", "is_email & (", "is_email | ("), None, ["❌ mini_email_orders has rows that aren't email rows"]
    reused = replace(solved, "july_email_orders = july[", '(july["session_medium"] == "email")', "is_email")
    reused = replace(reused, "july_email_orders = july[", "july_email_orders = july[", 'is_email = july["session_medium"] == "email"\njuly_email_orders = july[')
    yield "2.3 is_email reused for July", reused, None, ["❌ is_email has 1984 values, but mini has 6 rows", "✅ july_email_orders has July's 63"]
    yield "2.3 no date condition", replace(solved, "july_email_orders = july[", '(july["date"] <= "2024-07-31")\n    & ', ""), None, ["❌ july_email_orders has 67 rows", "❌ email_orders_revenue includes August 1 and 2"]
    yield "2.3 no transactions condition", replace(solved, "july_email_orders = july[", '\n    & (july["transactions"] > 0)', ""), None, ["❌ july_email_orders has every July email row"]

    # 2.4 Rank August's best rows
    book, solved = load("2.4-rank-august.ipynb"), load("2.4-rank-august.ipynb", solved=True)
    yield "2.4 solution", solved, None, [CLEAN, "✅ august has its 1,712 rows", "✅ top_revenue has August's five", "✅ paid_social's sessions_rank", "✅ Six rows share fifth place", "✅ top_paid_social has 10 rows", DONE]
    yield "2.4 as published", book, None, ["❌ august isn't a DataFrame yet"]
    yield "2.4 sorted the whole file", replace(solved, "top_revenue =", "august.sort_values", "export.sort_values"), None, ["❌ top_revenue has a row from September 1"]
    yield "2.4 smallest first", replace(solved, "top_revenue =", ", ascending=False).head(5)", ").head(5)"), None, ["❌ top_revenue has the smallest revenue rows"]
    yield "2.4 default tie rule", replace(solved, "paid_social =", ', method="min"', ""), None, ["❌ Six rows tie with 81 sessions, and they're ranked 7.5", "❌ tied_fifth is 0"]
    yield "2.4 head(5) for the top", replace(solved, "tied_fifth =", 'paid_social[paid_social["sessions_rank"] <= 5]', 'paid_social.sort_values("sessions", ascending=False).head(5)'), None, ["❌ top_paid_social has 5 rows"]

    # 2.5 Stack 2024's twelve exports
    book, solved = load("2.5-stack-2024.ipynb"), load("2.5-stack-2024.ipynb", solved=True)
    yield "2.5 solution", solved, None, [CLEAN, "✅ frames has the twelve months", "✅ year has all 22,596 rows", "✅ 1,411 rows (79,037 sessions)", "✅ revenue_is_numeric is False", "✅ October, November and December 2024", DONE]
    yield "2.5 as published", book, None, ["❌ frames should be a list of DataFrames"]
    yield "2.5 no ignore_index", replace(solved, "year =", ", ignore_index=True", ""), None, ["❌ year has 22,596 rows, but its index repeats"]
    yield "2.5 no export_month", replace(solved, "frames = []", '    export["export_month"] = month\n', ""), None, ["❌ Not every DataFrame in frames has an export_month column"]
    yield "2.5 == instead of !=", replace(solved, "outside =", "!=", "=="), None, ["❌ outside has the rows inside their export's month"]
    yield "2.5 text months from year", replace(solved, "revenue_is_numeric =", 'is_numeric_dtype(frame["revenue"])', 'is_numeric_dtype(year["revenue"])'), None, ["❌ text_revenue_months has 12 months"]

    # Final exercise: Answer a manager's questions about June 2024
    book, solved = load("2-june-questions.ipynb"), load("2-june-questions.ipynb", solved=True)
    yield "final solution", solved, None, [CLEAN, "✅ june has the 1,790 rows", "✅ top_paid_search has June's five", "✅ 62 of June's rows", "✅ Email brought 9.13%", "✅ The smallest revenue is -$541.91", DONE]
    yield "final as published", book, None, ["❌ june isn't a DataFrame yet"]
    yield "final whole file", replace(solved, "june =", 'export[export["date"] <= "2024-06-30"]', "export"), None, ["❌ june has all 1,933 rows", "❌ no_campaign is 68", "❌ email_share is 0.0957"]
    yield "final June 30 left out", replace(solved, "june =", '<= "2024-06-30"', '< "2024-06-30"'), None, ["❌ june has 1,722 rows"]
    yield "final share of rows", replace(solved, "no_campaign =", 'email_share = round(email_sessions / june["sessions"].sum(), 4)', 'email_share = round((june["session_medium"] == "email").mean(), 4)'), None, ["❌ email_share is 0.0726"]
