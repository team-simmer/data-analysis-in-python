"""Lesson 13.'s workbook tests: the solution, the workbook as published, and the common mistakes.

Published as tests/lesson-13/cases.py in team-simmer/data-analysis-in-python and run by
tests/run_tests.py, which provides replace(cells, starts, old, new). Each case is
(name, cells, order, expected lines in the check's output).

The BigQuery workbooks run their queries for real, in the project named by the BQ_PROJECT
environment variable, with Application Default Credentials (on GitHub, the workbook-tests service
account, through Workload Identity Federation). The tests replace Colab's login cell with the
client alone, and the empty PROJECT_ID with BQ_PROJECT. DuckDB reads the course's files from
their URLs, as in Colab.
"""

CLEAN = "✅ Every cell in this session ran once"
DONE = "Everything matches, in a clean run"


def offline_google(cells):
    """Return the cells with Colab's login replaced and PROJECT_ID set for a test kernel."""
    out = []
    for source in cells:
        if 'PROJECT_ID = ""' in source:
            source = source.replace("from google.colab import auth\n", "")
            source = "import os\n" + source.replace('PROJECT_ID = ""', 'PROJECT_ID = os.environ["BQ_PROJECT"]')
        if source.startswith("# Log in to Google"):
            source = "client = bigquery.Client(project=PROJECT_ID)"
        out.append(source)
    return out


def twice(cells):
    """Run every cell, then the check again: the check should warn that it has run before."""
    return list(range(1, len(cells) + 1)) + [len(cells)]


def cases(load):
    def both(name):
        return offline_google(load(name)), offline_google(load(name, solved=True))

    # 13.1 Report 2025 by channel group
    book, solved = both("13.1-channel-groups-2025.ipynb")
    yield "13.1 solution", solved, None, [CLEAN, "✅ 9 channel groups, with 38,502 purchases and $3,407,991.38", DONE]
    yield "13.1 as published", book, None, ["❌ channels_2025 should be a DataFrame"]
    yield "13.1 every event", replace(solved, "sql =", " AND event_name = 'purchase'", ""), None, ["events, not purchases"]
    yield "13.1 every day", replace(solved, "sql =", "_TABLE_SUFFIX BETWEEN '{START_DATE}' AND '{END_DATE}' AND ", ""), None, ["❌ The table has 65,106 purchases, but 2025 has 38,502"]
    yield "13.1 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # 13.2 Report Black Friday week on a budget
    book, solved = both("13.2-black-friday-budget.ipynb")
    yield "13.2 solution", solved, None, [CLEAN, "✅ SELECT * for the week would process 554,391,054 bytes", "✅ The query would process 14,481,987 bytes", "✅ 9 channel groups, with 2,641 purchases", DONE]
    yield "13.2 as published", book, None, ["❌ dry_run_bytes should be a function", "❌ bytes_query should be a number", "❌ bf_channels should be a DataFrame"]
    # Colab's Run all stops at the cell BigQuery refuses, so the test runs the check right after it.
    yield "13.2 event_date", replace(solved, "sql =", "_TABLE_SUFFIX BETWEEN", "event_date BETWEEN"), [1, 2, 3, 4, 5, 6], ["⚠️ BigQuery stopped a query over the budget", "❌ bytes_query is 799,090,669, over the budget", "instead of event_date"]
    yield "13.2 no limit", replace(solved, "config =", "config = bigquery.QueryJobConfig(maximum_bytes_billed=BUDGET)\nbf_channels = client.query(sql, job_config=config)", "bf_channels = client.query(sql)"), None, ["❌ Run the query with a limit"]

    # 13.3 Report 2025 with DuckDB
    book, solved = both("13.3-devices-2025-duckdb.ipynb")
    yield "13.3 solution", solved, None, [CLEAN, "✅ 8 event names and 8,424,290 events", "✅ 3 devices, with 38,502 purchases and $3,407,991.38", DONE]
    yield "13.3 as published", book, None, ["❌ events_2025 should be a DataFrame", "❌ devices_2025 should be a DataFrame"]
    yield "13.3 both years", replace(solved, "sql =", "WHERE event_date BETWEEN '{START_DATE}' AND '{END_DATE}'\n", ""), None, ["❌ events_2025 counts both years' 15,101,655 events"]
    yield "13.3 total", replace(solved, 'sql = f"""\nSELECT e.', "SUM(o.subtotal)", "SUM(o.total)"), None, ["❌ The revenue is $3,791,515.13: the orders' total"]

    # 13 Answer one question from two sources: parameters 1, login 2, solution 3-6, check 7
    book, solved = both("13-two-sources.ipynb")
    yield "13 final solution", solved, None, [CLEAN, "✅ The BigQuery query processes 135,551,439 bytes", "✅ bq_daily has 276 rows", "✅ duck_daily has 276 rows", "✅ BigQuery and DuckDB agree on all 276 days and devices", DONE]
    yield "13 final as published", book, None, ["❌ bytes_bq should be a number", "❌ bq_daily should be a DataFrame", "❌ duck_daily should be a DataFrame", "❌ compared should be a DataFrame"]
    yield "13 final event_date", replace(solved, "def dry_run_bytes", "WHERE _TABLE_SUFFIX BETWEEN '{BQ_START}' AND '{BQ_END}' AND", "WHERE event_date BETWEEN '{BQ_START}' AND '{BQ_END}' AND"), [1, 2, 3, 7], ["⚠️ BigQuery stopped the query over the budget", "❌ bytes_bq is 711,965,839, over the budget", "instead of event_date"]
    yield "13 final total", replace(solved, "duck_sql =", "SUM(o.subtotal)", "SUM(o.total)"), None, ["❌ duck_daily's revenue is $1,450,951.25: the orders' total"]
    yield "13 final dates as text", replace(solved, "bq_daily[", 'bq_daily["event_date"] = pd.to_datetime(bq_daily["event_date"], format="%Y%m%d")\n', ""), [1, 2, 3, 4, 5, 7], ["⚠️ The merge stopped", "❌ compared should be a DataFrame"]
    yield "13 final check run twice", solved, twice(solved), ["⚠️ This cell has run before"]
