"""Lesson 12.'s workbook tests: the solution, the workbook as published, and the common mistakes.

Published as tests/lesson-12/cases.py in team-simmer/data-analysis-in-python and run by
tests/run_tests.py, which provides replace(cells, starts, old, new). Each case is
(name, cells, order, expected lines in the check's output).

The workbooks call the live Simmer API. The tests read the course key from the SIMMER_API_KEY
environment variable instead of Colab Secrets (and the API's address from SIMMER_API_URL, if it's
set, to test against a local copy). Google's login and gspread become an in-memory fake that, like
the real client, serializes what it's given to JSON. Topics 12.1., 12.2. and 12.4. also get a
wrapper that retries 429 and 503 answers, because a random 503 isn't what those topics test.
"""

CLEAN = "✅ Every cell in this session ran once"
DONE = "Everything matches, in a clean run"

KEY_LINE = 'API_KEY = userdata.get("SIMMER_API_KEY")'
ADDRESS = "https://api.teamsimmer.com"

PATIENT_REQUESTS = '''import time as _time

import requests as _requests

_send = _requests.Session.send


def _patient_send(self, request, **kwargs):
    """Retry 429 and 503 answers, so a busy API doesn't fail a test that isn't about retries."""
    for _ in range(10):
        response = _send(self, request, **kwargs)
        if response.status_code not in (429, 503) or "simulate_error" in request.url:
            return response
        _time.sleep(int(response.headers.get("Retry-After", 1)))
    return response


_requests.Session.send = _patient_send'''

FAKE_GOOGLE = '''# The tests' stand-in for Google's login and gspread: one in-memory Drive.
import json


class SpreadsheetNotFound(Exception):
    pass


class _Worksheet:
    def __init__(self):
        self.values = []

    def clear(self):
        self.values = []

    def update(self, values=None, range_name=None, **kwargs):
        json.dumps(values)  # The real client sends the values as JSON, so a date fails here too.
        self.values = [list(row) for row in values]

    def get_all_records(self):
        if not self.values:
            return []
        header, *rows = self.values
        return [dict(zip(header, row)) for row in rows]


class _Spreadsheet:
    def __init__(self, title):
        self.title, self.sheet1, self.url = title, _Worksheet(), "https://docs.google.com/spreadsheets/d/test"


class _Client:
    def __init__(self):
        self.files = {}

    def open(self, title):
        if title not in self.files:
            raise SpreadsheetNotFound(title)
        return self.files[title]

    def create(self, title):
        self.files[title] = _Spreadsheet(title)
        return self.files[title]


class gspread:
    SpreadsheetNotFound = SpreadsheetNotFound


gc = _Client()'''


def offline_google(cells, patient=False):
    """Return the cells with Colab's secrets, pip and login replaced for a test kernel."""
    out = []
    for source in cells:
        if KEY_LINE in source:
            source = source.replace("from google.colab import userdata\n", "")
            source = source.replace(KEY_LINE, 'API_KEY = os.environ["SIMMER_API_KEY"]')
            source = "import os\n" + source
        if ADDRESS in source:
            source = source.replace(f'"{ADDRESS}/v1/"', f'os.environ.get("SIMMER_API_URL", "{ADDRESS}") + "/v1/"')
            source = source.replace(f'"{ADDRESS}"', f'os.environ.get("SIMMER_API_URL", "{ADDRESS}")')
        if source.startswith("%pip install"):
            source = "pass  # installed by the test environment"
        if source.startswith("# Log in to Google"):
            source = FAKE_GOOGLE
        out.append(source)
    return [PATIENT_REQUESTS] + out if patient else out


def twice(cells):
    """Run every cell, then the check again: the check should warn that it has run before."""
    return list(range(1, len(cells) + 1)) + [len(cells)]


def cases(load):
    def both(name, patient=False):
        return (offline_google(load(name), patient), offline_google(load(name, solved=True), patient))

    # 12.1 Get the campaign list
    book, solved = both("12.1-campaign-list.ipynb", patient=True)
    yield "12.1 solution", solved, None, [CLEAN, "✅ Without the key, the API answers 401", "✅ 104 campaigns", "✅ 36 Paid Social campaigns", DONE]
    yield "12.1 as published", book, None, ["❌ There's no no_key_status yet", "❌ campaigns should be a DataFrame", "❌ campaigns_per_channel should be a Series"]
    yield "12.1 key in the first request", replace(solved, "no_key_status =", 'requests.get(BASE_URL + "campaigns")', 'requests.get(BASE_URL + "campaigns", headers={"X-API-Key": API_KEY})'), None, ["❌ no_key_status is 200"]
    yield "12.1 whole answer", replace(solved, "response =", 'pd.DataFrame(response.json()["campaigns"])', 'pd.DataFrame([response.json()])'), None, ["❌ The campaigns table should have one row per campaign"]

    # 12.2 Page through Q3
    book, solved = both("12.2-page-through-q3.ipynb", patient=True)
    yield "12.2 solution", solved, None, [CLEAN, "✅ 9 pages, 828 rows", "✅ 828 rows, as the API reported", DONE]
    yield "12.2 as published", book, None, ["❌ rows should be a list", "❌ q3 should be a DataFrame"]
    yield "12.2 first page only", replace(solved, "params =", 'if "next_page_token" not in body:\n        break', "break"), None, ["❌ You have only the first page"]
    yield "12.2 append", replace(solved, "params =", 'rows.extend(body["rows"])', 'rows.append(body["rows"])'), None, ["❌ rows is a list of pages"]
    yield "12.2 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # 12.3 Pull all of 2025
    book, solved = both("12.3-pull-all-of-2025.ipynb")
    yield "12.3 solution", solved, None, [CLEAN, "✅ get_json() tries again after a 503", "✅ 3,285 rows from 33 pages", DONE]
    yield "12.3 as published", book, None, ["❌ get_json should be a function", "❌ year_2025 should be a DataFrame"]
    yield "12.3 no retry", replace(solved, "RETRY_STATUSES =", "        if response.status_code not in RETRY_STATUSES:", "        if True:"), [1, 2, len(solved)], ["❌ get_json() stopped at the first 503"]

    # 12.4 Report Q4 by channel group
    book, solved = both("12.4-ga4-channel-report.ipynb", patient=True)
    yield "12.4 solution", solved, None, [CLEAN, "✅ A report of 9 channel groups", "✅ 486,702 sessions, 14,997 transactions", DONE]
    yield "12.4 as published", book, None, ["❌ response should be the answer", "❌ channels should be a DataFrame"]
    yield "12.4 values as text", replace(solved, "names =", 'channels[["sessions", "transactions"]] = channels[["sessions", "transactions"]].astype(int)\nchannels["purchaseRevenue"] = channels["purchaseRevenue"].astype(float)\n', ""), None, ["❌ The metrics are still text"]
    yield "12.4 wrong quarter", replace(solved, "request =", "date_ranges=[DateRange(start_date=START_DATE, end_date=END_DATE)]", 'date_ranges=[DateRange(start_date="2025-07-01", end_date="2025-09-30")]'), None, ["❌ Q4 2025 has 486,702 sessions"]

    # 12.5 Share five weeks in a sheet
    book, solved = both("12.5-weekly-sheet.ipynb")
    yield "12.5 solution", solved, None, [CLEAN, "✅ The spreadsheet 'Simmer weekly report'", "✅ The sheet reads back as the weekly table", DONE]
    yield "12.5 as published", book, None, ["❌ spreadsheet should be a gspread spreadsheet", "❌ read_back should be a DataFrame"]
    yield "12.5 dates as dates", replace(solved, "weekly[", 'weekly["week_start"] = weekly["week_start"].dt.strftime("%Y-%m-%d")\n', ""), None, ["⚠️ A cell stopped with TypeError: Object of type Timestamp is not JSON serializable", "❌ The sheet's header row"]
    yield "12.5 no header", replace(solved, "weekly[", "[weekly.columns.tolist()] + weekly.values.tolist()", "weekly.values.tolist()"), None, ["❌ The sheet's header row should be"]

    # 12 Pull a year of campaign data
    book, solved = both("12-campaign-year.ipynb")
    yield "12 final solution", solved, None, [CLEAN, "✅ 8,139 rows of 2025 by campaign", "✅ 12 months of ROAS", "✅ The sheet reads back as the monthly table", DONE]
    yield "12 final as published", book, None, ["❌ get_json should be a function", "❌ report should be a DataFrame", "❌ monthly should be a DataFrame", "❌ read_back should be a DataFrame"]
    yield "12 final every row's revenue", replace(solved, "paid =", 'paid = report[report["spend"] > 0].copy()', "paid = report.copy()"), None, ["❌ November's ROAS is 13.67"]
    yield "12 final ROAS reversed", replace(solved, "paid =", 'monthly["revenue"] / monthly["spend"]', 'monthly["spend"] / monthly["revenue"]'), None, ["❌ November's ROAS is 0.35"]
    yield "12 final check run twice", solved, twice(solved), ["⚠️ This cell has run before"]
