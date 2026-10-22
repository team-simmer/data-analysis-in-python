"""Lesson 3.'s workbook tests: the solution, the workbook as published, and the common mistakes.

Published as tests/lesson-03/cases.py in team-simmer/data-analysis-in-python and run by
tests/run_tests.py, which provides replace(cells, starts, old, new). Each case is
(name, cells, order, expected lines in the check's output).
"""

CLEAN = "✅ Every cell in this session ran once"
DONE = "Everything matches, in a clean run"


def twice(cells):
    """Run every cell, then the check again: the check should warn that it has run before."""
    return list(range(1, len(cells) + 1)) + [len(cells)]


def cases(load):
    # 3.1 Count September's lost campaigns
    book, solved = load("3.1-lost-campaigns.ipynb"), load("3.1-lost-campaigns.ipynb", solved=True)
    yield "3.1 solution", solved, None, [CLEAN, "✅ missing_by_column: 65 missing campaigns", "✅ Three spellings of a lost campaign", "✅ 207 rows have a lost campaign", "✅ 820 sessions have a lost campaign", "✅ september keeps all 1,780 rows", DONE]
    yield "3.1 as published", book, None, ["❌ missing_by_column should be", "❌ september isn't a DataFrame yet"]
    yield "3.1 no - in na_values", replace(solved, "september = pd.read_csv", '["(not set)", "-"]', '["(not set)"]'), None, ["❌ lost_campaigns is 187", "❌ september still has campaigns spelled -"]
    yield "3.1 dropna instead of fillna", replace(solved, 'september["session_campaign"] =', 'september["session_campaign"] = september["session_campaign"].fillna("(not set)")', "september = september.dropna()"), None, ["❌ september has 1,573 rows"]
    yield "3.1 fillna not assigned", replace(solved, 'september["session_campaign"] =', 'september["session_campaign"] = september["session_campaign"].fillna', 'september["session_campaign"].fillna'), None, ["❌ september still has 207 missing campaigns"]
    yield "3.1 value_counts drops NaN", replace(solved, "campaigns = september_raw", "nan_rows = campaigns.isna().sum()", 'nan_rows = campaigns.value_counts().get("nan", 0)'), None, ["❌ nan_rows is 0"]
    yield "3.1 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # 3.2 Fix March 2025's dates and autumn's revenue
    book, solved = load("3.2-dates-and-revenue.ipynb"), load("3.2-dates-and-revenue.ipynb", solved=True)
    yield "3.2 solution", solved, None, [CLEAN, "✅ 1,900 rows are dated in March 2025", "✅ The file's last date is March 27, 2026", "✅ frames has the four months", "✅ autumn's revenue is $1,041,976.77", DONE]
    yield "3.2 as published", book, None, ["❌ march_2025's date column is still text", "❌ frames should be a list of four DataFrames"]
    yield "3.2 format mixed", replace(solved, 'march_2025["date"] =', 'format="%d/%m/%Y"', 'format="mixed"'), None, ["❌ march_2025's dates start on January 3"]
    after = replace(solved, "frames = []", '    if not pd.api.types.is_numeric_dtype(export["revenue"]):\n        export["revenue"] = export["revenue"].str.replace("$", "").str.replace(",", "").astype(float)\n', "")
    after = replace(after, "autumn = pd.concat", "autumn = pd.concat(frames, ignore_index=True)\n", 'autumn = pd.concat(frames, ignore_index=True)\nautumn["revenue"] = autumn["revenue"].str.replace("$", "").str.replace(",", "").astype(float)\n')
    yield "3.2 converted after stacking", after, None, ["❌ Some files in frames still have revenue as text", "❌ autumn has 1,780 rows with NaN revenue"]
    yield "3.2 no comma step", replace(solved, "frames = []", '.str.replace(",", "")', ""), None, ["⚠️ A cell stopped with ValueError", "❌ frames should be a list of four DataFrames"]

    # 3.3 Standardize November's sources
    book, solved = load("3.3-source-spellings.ipynb"), load("3.3-source-spellings.ipynb", solved=True)
    yield "3.3 solution", solved, None, [CLEAN, "✅ November's export has 22 spellings", "✅ SOURCE_ALIASES has the eight aliases", "✅ source has 13 values", "✅ Facebook had 16,833 sessions", DONE]
    yield "3.3 as published", book, None, ["❌ raw_sources should be", "❌ SOURCE_ALIASES should be a dictionary", "❌ november has no source column yet"]
    yield "3.3 not lowercased", replace(solved, "SOURCE_ALIASES = {", ".str.lower().str.strip()", ".str.strip()"), None, ["❌ source has 14 values", "❌ facebook_sessions is 15,832"]
    yield "3.3 session_source overwritten", replace(solved, "SOURCE_ALIASES = {", 'november["source"] = november["session_source"].str.lower().str.strip().replace(SOURCE_ALIASES)', 'november["session_source"] = november["session_source"].str.lower().str.strip().replace(SOURCE_ALIASES)\nnovember["source"] = november["session_source"]'), None, ["❌ november's session_source column has changed"]
    yield "3.3 fb missing", replace(solved, "SOURCE_ALIASES = {", ' "fb": "facebook",', ""), None, ["❌ SOURCE_ALIASES is missing ['fb']"]
    yield "3.3 raw facebook only", replace(solved, "clean_sources =", 'facebook_sessions = november.loc[november["source"]', 'facebook_sessions = november.loc[november["session_source"]'), None, ["❌ facebook_sessions is 10,963"]

    # 3.4 Clean the second half of 2025
    book, solved = load("3.4-remove-rows.ipynb"), load("3.4-remove-rows.ipynb", solved=True)
    yield "3.4 solution", solved, None, [CLEAN, "✅ 618 rows were copies", "✅ 18 rows are dated after December 31, 2025", "✅ 19 rows are the store's own test traffic", "✅ clean has 11,268 rows and 819,781 sessions", DONE]
    yield "3.4 as published", book, None, ["❌ duplicates should be", "❌ clean isn't a DataFrame yet"]
    keys = '(subset=["date", "session_source", "session_medium", "session_campaign"])'
    subset = replace(solved, "duplicates =", "h2.duplicated()", "h2.duplicated" + keys)
    subset = replace(subset, "duplicates =", "h2.drop_duplicates()", "h2.drop_duplicates" + keys)
    yield "3.4 subset of columns", subset, None, ["❌ 1,871 rows share a date, source, medium and campaign"]
    yield "3.4 keep=False", replace(solved, "duplicates =", "deduped = h2.drop_duplicates()", "deduped = h2[~h2.duplicated(keep=False)]"), None, ["❌ deduped has 10,687 rows"]
    yield "3.4 refunds removed", replace(solved, "future_rows =", 'clean = in_range[in_range["session_medium"] != "test"]', 'clean = in_range[(in_range["session_medium"] != "test") & (in_range["revenue"] >= 0)]'), None, ["❌ clean has 9,852 rows"]
    yield "3.4 future rows kept", replace(solved, "future_rows =", 'clean = in_range[in_range["session_medium"] != "test"]', 'clean = deduped[deduped["session_medium"] != "test"]'), None, ["❌ clean has 11,286 rows"]
    yield "3.4 test rows counted in h2", replace(solved, "future_rows =", 'test_rows = (in_range["session_medium"]', 'test_rows = (h2["session_medium"]'), None, ["❌ test_rows is 20"]

    # 3.5 Audit a colleague's cleaned data
    book, solved = load("3.5-validate.ipynb"), load("3.5-validate.ipynb", solved=True)
    yield "3.5 solution", solved, None, [CLEAN, "✅ validate() passes the cleaned table", "✅ Every check fails when its rule is broken", "✅ The colleague's table fails four checks", "✅ clean's 464,344 sessions match", "✅ The colleague's table has 30,590 sessions too many", DONE]
    yield "3.5 as published", book, None, ["❌ validate isn't a function yet"]
    yield "3.5 date compared with text", replace(solved, "def validate(", '"dates in range": bool(df["date"].between(start, end).all()),', '"dates in range": df["date"].min() >= start and df["date"].max() <= end,'), None, ["⚠️ A cell stopped with TypeError", "❌ validate(clean, START, END) stopped with TypeError", "use df[\"date\"].between(start, end).all()"]
    yield "3.5 a check that can't fail", replace(solved, "def validate(", '(df["session_medium"] == "test")', '(df["session_medium"] == "Test")'), None, ["❌ Your checks don't catch a table broken on purpose, one rule at a time: ['no test traffic']", "❌ colleague_checks should fail"]
    yield "3.5 no assert", replace(solved, "clean_checks =", "assert all(clean_checks.values()), clean_checks\n", ""), None, ["❌ Add an assert after clean_checks"]
    yield "3.5 gap the wrong way round", replace(solved, "reconciled =", 'colleague["sessions"].sum() - REPORTED_SESSIONS', 'REPORTED_SESSIONS - colleague["sessions"].sum()'), None, ["❌ colleague_gap is negative"]

    # Final exercise: Clean two years of exports end to end
    book, solved = load("3-clean-two-years.ipynb"), load("3-clean-two-years.ipynb", solved=True)
    yield "final solution", solved, None, [CLEAN, "✅ clean has the 43,035 real rows", "✅ 4,880 rows have their lost campaign labeled", "✅ source has 12 sources", "✅ The 4,585 refund rows are in", "✅ Your six checks pass on clean", "✅ total_sessions matches the platform's 2,506,005", DONE]
    yield "final as published", book, None, ["❌ clean isn't a DataFrame yet", "❌ checks should be validate(clean, START, END)"]
    yield "final no duplicates removed", replace(solved, "clean = raw.copy()", "deduped = clean.drop_duplicates()", "deduped = clean"), None, ["❌ clean has 45,760 rows: the copies from overlapping exports"]
    yield "final March read month first", replace(solved, "DAY_FIRST_MONTHS =", 'date_format = "%d/%m/%Y" if month in DAY_FIRST_MONTHS else "%Y-%m-%d"', 'date_format = "mixed"'), None, ["❌ clean has 43,219 rows: March 2025 was read month first"]
    after = replace(solved, "DAY_FIRST_MONTHS =", '    if not pd.api.types.is_numeric_dtype(export["revenue"]):\n        export["revenue"] = export["revenue"].str.replace("$", "").str.replace(",", "").astype(float)\n', "")
    after = replace(after, "DAY_FIRST_MONTHS =", "raw = pd.concat([read_export(month) for month in MONTHS], ignore_index=True)\n", 'raw = pd.concat([read_export(month) for month in MONTHS], ignore_index=True)\nraw["revenue"] = raw["revenue"].str.replace("$", "").str.replace(",", "").astype(float)\n')
    yield "final revenue converted after stacking", after, None, ["rows have NaN revenue: revenue was converted after stacking"]
    early = replace(solved, "clean = raw.copy()", 'clean = raw.copy()\n', 'clean = raw.copy()\nclean["session_source"] = clean["session_source"].str.lower().str.strip().replace(SOURCE_ALIASES)\n')
    yield "final sources standardized first", early, None, ["❌ clean has 42,529 rows: the sources were standardized before removing duplicates"]
    yield "final future rows kept", replace(solved, "clean = raw.copy()", 'in_range = deduped[deduped["date"] <= END]', "in_range = deduped"), None, ["❌ clean has 43,075 rows: the 40 rows dated after END"]
    yield "final test rows kept", replace(solved, "clean = raw.copy()", 'clean = in_range[in_range["session_medium"] != "test"].copy()', "clean = in_range.copy()"), None, ["❌ clean has 43,095 rows: the 60 test rows"]
    yield "final refunds removed", replace(solved, "clean = raw.copy()", 'clean = in_range[in_range["session_medium"] != "test"].copy()', 'clean = in_range[(in_range["session_medium"] != "test") & (in_range["revenue"] >= 0)].copy()'), None, ["❌ clean has 38,450 rows: the 4,585 refund rows are gone"]
    yield "final campaigns not labeled", replace(solved, "clean = raw.copy()", 'clean["session_campaign"] = clean["session_campaign"].fillna("(not set)")\n', ""), None, ["lost campaigns aren't labeled yet", "❌ Your own checks fail: ['no missing campaigns']"]
