"""Lesson 1.'s workbook tests: topic 1.2.'s setup check, and topic 1.4.'s solution, workbook as published and common mistakes.

Published as tests/lesson-01/cases.py in team-simmer/data-analysis-in-python and run by
tests/run_tests.py, which provides replace(cells, starts, old, new). Each case is
(name, cells, order, expected lines in the check's output). Topic 1.3. is an editor exercise,
with its tests in its topic file.
"""

CLEAN = "✅ Every cell in this session ran once"
DONE = "Everything matches, in a clean run"


def twice(cells):
    """Run every cell, then the check again: the check should warn that it has run before."""
    return list(range(1, len(cells) + 1)) + [len(cells)]


def cases(load):
    # 1.2 Check your setup: outside Colab, the first line is a warning
    book = load("1.2-setup-check.ipynb")
    yield "1.2 setup check", book, None, ["⚠️ This notebook isn't running in Google Colab", "✅ Python 3.", "✅ The course's data store answers: January 2024's sessions export has 1,711 rows.", "Your setup is ready for lesson 2."]
    yield "1.2 data store unreachable", replace(book, "# @title Check your setup", "simmer-store/v1/", "simmer-store/no-such-folder/"), None, ["❌ Colab couldn't read the course's data store: HTTPError"]

    # 1.4 Total February's referral sessions
    book, solved = load("1.4-referral-report.ipynb"), load("1.4-referral-report.ipynb", solved=True)
    yield "1.4 solution", solved, None, [CLEAN, "✅ February's export: 1,724 rows.", "✅ 361 referral rows.", "✅ 6,909 referral sessions in February's export", DONE]
    yield "1.4 as published", book, None, ["❌ sessions should be a DataFrame", "❌ referral should be a DataFrame", "❌ referral_sessions should be a number"]
    yield "1.4 January", replace(solved, "sessions =", "2024_02", "2024_01"), None, ["❌ The sessions table has 1,711 rows: that's January's file", "❌ referral has 365 rows", "❌ referral_sessions is 7,295"]
    yield "1.4 capitalized", replace(solved, "referral =", '"referral"', '"Referral"'), None, ["❌ referral has no rows"]
    yield "1.4 rows", replace(solved, "referral_sessions =", 'referral["sessions"].sum()', "len(referral)"), None, ["❌ referral_sessions is 361: that's how many rows there are"]
    yield "1.4 whole file", replace(solved, "referral_sessions =", 'referral["sessions"].sum()', 'sessions["sessions"].sum()'), None, ["❌ referral_sessions is 84,654"]
    yield "1.4 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]
