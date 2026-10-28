"""Lesson 9.'s workbook tests: the solution, the workbook as published, and the common mistakes.

Published as tests/lesson-09/cases.py in team-simmer/data-analysis-in-python and run by
tests/run_tests.py, which provides replace(cells, starts, old, new). Each case is
(name, cells, order, expected lines in the check's output).
"""

CLEAN = "✅ Every cell in this session ran once"
DONE = "Everything matches, in a clean run"


def twice(cells):
    """Run every cell, then the check again: the check should warn that it has run before."""
    return list(range(1, len(cells) + 1)) + [len(cells)]


def cases(load):
    # 9.1 Calculate the checkout test's lift
    book, solved = load("9.1-lift-per-variant.ipynb"), load("9.1-lift-per-variant.ipynb", solved=True)
    yield "9.1 solution", solved, None, [CLEAN, "✅ One row for each of the 80,054 users in the test, 3,851 of them converted", "✅ A converted 4.57% of its users and B 5.07%, with $4.06 and $4.45 of revenue per user", "✅ B's conversion rate is +10.9% on A's, +0.50 percentage points, and its revenue per user +9.9%", DONE]
    yield "9.1 as published", book, None, ["❌ users should be a DataFrame", "❌ results should be a DataFrame", "❌ conversion_lift and revenue_lift should be numbers"]
    yield "9.1 inner join", replace(solved, "users =", ', how="left"', ""), None, ["❌ The users table has 3,851 rows"]
    yield "9.1 revenue not filled", replace(solved, "users =", 'users["revenue"] = users["revenue"].fillna(0)\n', ""), None, ["❌ The users table's revenue has 76,203 missing values"]
    yield "9.1 average order value", replace(solved, "results =", 'results["revenue_per_user"] = results["revenue"] / results["users"]', 'results["revenue_per_user"] = results["revenue"] / results["conversions"]'), None, ["❌ revenue_per_user is $88.69 for A"]
    yield "9.1 rate in percent", replace(solved, "results =", 'results["conversion_rate"] = results["conversions"] / results["users"]', 'results["conversion_rate"] = results["conversions"] / results["users"] * 100'), None, ["❌ results' conversion_rate is in percent"]
    yield "9.1 lift reversed", replace(solved, "conversion_lift =", 'results.loc["B", "conversion_rate"] / results.loc["A", "conversion_rate"]', 'results.loc["A", "conversion_rate"] / results.loc["B", "conversion_rate"]'), None, ["❌ conversion_lift is -0.0980"]
    yield "9.1 difference, not lift", replace(solved, "conversion_lift =", 'results.loc["B", "conversion_rate"] / results.loc["A", "conversion_rate"] - 1', '(results.loc["B", "conversion_rate"] - results.loc["A", "conversion_rate"]) * 100'), None, ["❌ conversion_lift is 0.4969: that's the difference in rates, in percentage points"]
    yield "9.1 lift in percent", replace(solved, "conversion_lift =", 'conversion_lift = results.loc["B", "conversion_rate"] / results.loc["A", "conversion_rate"] - 1', 'conversion_lift = (results.loc["B", "conversion_rate"] / results.loc["A", "conversion_rate"] - 1) * 100'), None, ["❌ conversion_lift is in percent"]
    yield "9.1 lift of conversions", replace(solved, "conversion_lift =", 'results.loc["B", "conversion_rate"] / results.loc["A", "conversion_rate"]', 'results.loc["B", "conversions"] / results.loc["A", "conversions"]'), None, ["❌ conversion_lift is 0.0194: that's the lift in the number of conversions"]
    yield "9.1 lift of total revenue", replace(solved, "conversion_lift =", 'results.loc["B", "revenue_per_user"] / results.loc["A", "revenue_per_user"]', 'results.loc["B", "revenue"] / results.loc["A", "revenue"]'), None, ["❌ revenue_lift is 0.0101: that's the lift in total revenue"]
    yield "9.1 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # 9.2 Check the checkout test's split
    book, solved = load("9.2-srm-check.ipynb"), load("9.2-srm-check.ipynb", solved=True)
    yield "9.2 solution", solved, None, [CLEAN, "✅ srm_p_value() returns 1.0 for an even split of 10,000 users and 0.048 for 5,000 against 5,200", "✅ A sample ratio mismatch: B has 47.9% of the users, and a 50/50 split would give one this uneven with a chance of 1.7e-32", DONE]
    yield "9.2 as published", book, None, ["❌ srm_p_value should be a function", "❌ variant_counts should be a Series"]
    yield "9.2 returns the statistic", replace(solved, "def srm_p_value", "stats.chisquare(counts).pvalue", "stats.chisquare(counts).statistic"), None, ["❌ srm_p_value([5000, 5200]) returns 3.92"]
    yield "9.2 no docstring", replace(solved, "def srm_p_value", '    """Return the p-value of a chi-square test that the counts were split evenly between the variants."""\n', ""), None, ["❌ srm_p_value() has no docstring"]
    yield "9.2 two arguments", replace(replace(solved, "def srm_p_value", "def srm_p_value(counts):", "def srm_p_value(count_a, count_b):\n    counts = [count_a, count_b]"), "variant_counts =", "srm_p_value(variant_counts)", 'srm_p_value(variant_counts["A"], variant_counts["B"])'), None, ["❌ srm_p_value(pd.Series({\"A\": 5000, \"B\": 5200})) stopped with TypeError", "✅ A sample ratio mismatch"]
    yield "9.2 binomial test", replace(solved, "def srm_p_value", "return stats.chisquare(counts).pvalue", "return stats.binomtest(int(list(counts)[1]), int(sum(counts))).pvalue"), None, ["✅ srm_p_value() returns 1.0 for an even split of 10,000 users and 0.049", "✅ A sample ratio mismatch", DONE]
    yield "9.2 conversions", replace(solved, "variant_counts =", 'variant_counts = users["variant"].value_counts()', 'variant_counts = users.groupby("variant")["converted"].sum()'), None, ["❌ variant_counts has the conversions, 1,907 and 1,944"]
    yield "9.2 A's share", replace(solved, "variant_counts =", 'share_b = variant_counts["B"]', 'share_b = variant_counts["A"]'), None, ["❌ share_b is 0.5210: that's A's share"]
    yield "9.2 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # 9.3 Find the users B lost
    book, solved = load("9.3-mismatch-cause.ipynb"), load("9.3-mismatch-cause.ipynb", solved=True)
    yield "9.3 solution", solved, None, [CLEAN, "✅ B's share of each browser's users runs from 0.0% to 50.9%", "✅ B has no users in Android Webview or Safari (in-app)", "✅ Without the in-app browsers, the split holds (p = 0.078, above 0.001), and B's lift drops from +10.9% to +3.6%", DONE]
    yield "9.3 as published", book, None, ["❌ browser_split should be a DataFrame", "❌ broken_browsers should be a list", "❌ fixed_users should be the users table without the broken browsers"]
    yield "9.3 normalized crosstab", replace(solved, "browser_split =", 'pd.crosstab(users["browser"], users["variant"])', 'pd.crosstab(users["browser"], users["variant"], normalize="index")'), None, ["❌ browser_split should count each browser's users by variant"]
    yield "9.3 share under half", replace(solved, "broken_browsers =", 'browser_split["B"] == 0', 'browser_split["share_b"] < 0.5'), None, ["❌ broken_browsers has every browser where B's share is under 50%"]
    yield "9.3 failed at 0.05", replace(solved, "broken_browsers =", 'list(browser_split[browser_split["B"] == 0].index)', '[browser for browser in browser_split.index if srm_p_value(browser_split.loc[browser, ["A", "B"]]) < 0.05]'), None, ["❌ broken_browsers has Safari, whose split fails at 0.05 (p = 0.014)"]
    yield "9.3 no mobile", replace(solved, "fixed_users =", 'users[~users["browser"].isin(broken_browsers)]', 'users[users["device_category"] != "mobile"]'), None, ["❌ The fixed_users table has 32,100 rows: every mobile user is gone"]
    yield "9.3 one browser", replace(solved, "fixed_users =", 'users[~users["browser"].isin(broken_browsers)]', 'users[users["browser"] != "Safari (in-app)"]'), None, ["❌ The fixed_users table still has Android Webview's users"]
    yield "9.3 lift of all users", replace(solved, "fixed_users =", 'fixed_rates = fixed_users.groupby', 'fixed_rates = users.groupby'), None, ["❌ fixed_lift is 0.1087: that's the lift of all users"]
    yield "9.3 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # 9.4 Test the checkout lift
    book, solved = load("9.4-significance.ipynb"), load("9.4-significance.ipynb", solved=True)
    yield "9.4 solution", solved, None, [CLEAN, "✅ On all users, the z-test gives p = 0.0010", "✅ On comparable users, p = 0.27: not significant. B's rate minus A's is between -0.13 and +0.48 percentage points", DONE]
    yield "9.4 as published", book, None, ["❌ naive_p should be a number", "❌ fixed_p should be a number"]
    yield "9.4 one-sided naive", replace(solved, "counts =", 'counts.loc[["B", "A"], "count"])', 'counts.loc[["B", "A"], "count"], alternative="larger")'), None, ["❌ naive_p is 0.000515: that's a one-sided test"]
    yield "9.4 one-sided fixed", replace(solved, "fixed_counts =", 'fixed_counts.loc[["B", "A"], "count"])', 'fixed_counts.loc[["B", "A"], "count"], alternative="larger")'), None, ["❌ fixed_p is 0.1333: that's a one-sided test"]
    yield "9.4 one-sided, wrong way", replace(solved, "fixed_counts =", 'proportions_ztest(fixed_counts.loc[["B", "A"], "sum"], fixed_counts.loc[["B", "A"], "count"])', 'proportions_ztest(fixed_counts.loc[["A", "B"], "sum"], fixed_counts.loc[["A", "B"], "count"], alternative="larger")'), None, ["❌ fixed_p is 0.8667: a one-sided test in the wrong direction"]
    yield "9.4 Yates", replace(solved, "fixed_counts =", 'z, fixed_p = proportions_ztest(fixed_counts.loc[["B", "A"], "sum"], fixed_counts.loc[["B", "A"], "count"])', 'from scipy import stats\nfixed_p = stats.chi2_contingency([[1944, 38348 - 1944], [1853, 37861 - 1853]]).pvalue'), None, ["❌ fixed_p is 0.2738: that's chi2_contingency() with Yates' correction"]
    yield "9.4 interval reversed", replace(solved, "fixed_counts =", 'confint_proportions_2indep(fixed_counts.loc["B", "sum"], fixed_counts.loc["B", "count"], fixed_counts.loc["A", "sum"], fixed_counts.loc["A", "count"])', 'confint_proportions_2indep(fixed_counts.loc["A", "sum"], fixed_counts.loc["A", "count"], fixed_counts.loc["B", "sum"], fixed_counts.loc["B", "count"])'), None, ["❌ ci_low and ci_high are A's rate minus B's"]
    yield "9.4 interval in points", replace(solved, "fixed_counts =", "significant = fixed_p < 0.05", "ci_low, ci_high = ci_low * 100, ci_high * 100\nsignificant = fixed_p < 0.05"), None, ["❌ ci_low and ci_high are in percentage points"]
    yield "9.4 Wald interval", replace(solved, "fixed_counts =", 'fixed_counts.loc["A", "count"])', 'fixed_counts.loc["A", "count"], method="wald")'), None, ["✅ On comparable users, p = 0.27", DONE]
    yield "9.4 interval of all users", replace(solved, "fixed_counts =", 'confint_proportions_2indep(fixed_counts.loc["B", "sum"], fixed_counts.loc["B", "count"], fixed_counts.loc["A", "sum"], fixed_counts.loc["A", "count"])', 'confint_proportions_2indep(counts.loc["B", "sum"], counts.loc["B", "count"], counts.loc["A", "sum"], counts.loc["A", "count"])'), None, ["❌ ci_low and ci_high are the interval for all users"]
    yield "9.4 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # 9.5 Size the checkout test
    book, solved = load("9.5-sample-size.ipynb"), load("9.5-sample-size.ipynb", solved=True)
    yield "9.5 solution", solved, None, [CLEAN, "✅ A's comparable users converted at 4.89%, and B's +3.6% on that", "✅ Detecting a +3.6% lift from 4.89% takes 242,212 users per variant: 6.4 times what each variant had", "✅ At 6,351 users per variant a week, the test needed 39 weeks, not 6", DONE]
    yield "9.5 as published", book, None, ["❌ baseline_rate and observed_lift should be numbers", "❌ users_needed should be a number", "❌ users_per_week should be a number"]
    yield "9.5 all users' baseline", replace(solved, "rates =", "fixed_users.groupby", "users.groupby"), None, ["❌ baseline_rate is 0.0457"]
    yield "9.5 not rounded up", replace(solved, "effect =", "users_needed = math.ceil(NormalIndPower().solve_power(effect_size=effect, alpha=0.05, power=0.8))", "users_needed = NormalIndPower().solve_power(effect_size=effect, alpha=0.05, power=0.8)"), None, ["❌ users_needed is 242,211.02"]
    yield "9.5 both variants", replace(solved, "effect =", "users_needed = math.ceil(", "users_needed = 2 * math.ceil("), None, ["❌ users_needed is 484,424: both variants together"]
    yield "9.5 one-sided", replace(solved, "effect =", "power=0.8)", 'power=0.8, alternative="larger")'), None, ["❌ users_needed is 190,790"]
    yield "9.5 power 0.9", replace(solved, "effect =", "power=0.8)", "power=0.9)"), None, ["❌ users_needed is 324,253"]
    yield "9.5 textbook formula", replace(solved, "effect =", "users_needed = math.ceil(NormalIndPower().solve_power(effect_size=effect, alpha=0.05, power=0.8))", "from scipy import stats\nrate_b = baseline_rate * (1 + observed_lift)\nusers_needed = math.ceil((stats.norm.ppf(0.975) + stats.norm.ppf(0.8)) ** 2 * (baseline_rate * (1 - baseline_rate) + rate_b * (1 - rate_b)) / (rate_b - baseline_rate) ** 2)"), None, ["✅ Detecting a +3.6% lift from 4.89% takes 242,226 users per variant", DONE]
    yield "9.5 weekly users of both variants", replace(solved, "users_per_week =", "len(fixed_users) / 2 / TEST_WEEKS", "len(fixed_users) / TEST_WEEKS"), None, ["❌ users_per_week is 12,701.5"]
    yield "9.5 weekly users of all users", replace(solved, "users_per_week =", "len(fixed_users) / 2", "len(users) / 2"), None, ["❌ users_per_week is 6,671.17"]
    yield "9.5 weeks not rounded up", replace(solved, "users_per_week =", "weeks_needed = math.ceil(users_needed / users_per_week)", "weeks_needed = users_needed / users_per_week"), None, ["❌ weeks_needed is 38.14"]
    yield "9.5 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # Final exercise: Write the readout for desktop users
    book, solved = load("9-desktop-readout.ipynb"), load("9-desktop-readout.ipynb", solved=True)
    yield "9 final solution", solved, None, [CLEAN, "✅ 80,054 users in the test, 27,856 of them on desktop, 1,401 of whom converted", "✅ The desktop split holds: 13,867 in A and 13,989 in B, p = 0.465, far above 0.001", "✅ On desktop, B converts +3.9% relative to A: 5.13% against 4.93%", "✅ p = 0.46, not significant. B's rate minus A's is between -0.32 and +0.71 percentage points: from -7% to +14% relative to A", "✅ Detecting +3.9% on desktop takes 201,507 users per variant: 87 weeks of desktop traffic, against the test's 6", "Everything matches, in a clean run. Read your text cell again"]
    yield "9 final as published", book, None, ["❌ users should be the assignments", "❌ There's no srm_p", "❌ lift should be a number", "❌ p_value should be a number", "❌ users_needed should be a number"]
    yield "9 final inner join", replace(solved, "assignments = pd.read_csv(ASSIGNMENTS_FILE", ', how="left"', ""), None, ["❌ The users table has 3,851 rows"]
    yield "9 final all users", replace(solved, "assignments = pd.read_csv(ASSIGNMENTS_FILE", 'desktop_users = users[users["device_category"] == "desktop"]', "desktop_users = users"), None, ["❌ The desktop_users table has all 80,054 users"]
    yield "9 final split not checked", replace(solved, "def srm_p_value", 'srm_p = srm_p_value(desktop_users["variant"].value_counts())\ndesktop_users["variant"].value_counts(), srm_p', 'desktop_users["variant"].value_counts()'), None, ["❌ There's no srm_p: check the split before you read the result"]
    yield "9 final all users' split", replace(solved, "def srm_p_value", 'srm_p = srm_p_value(desktop_users["variant"]', 'srm_p = srm_p_value(users["variant"]'), None, ["❌ srm_p is 1.7e-32: that's all users' split"]
    yield "9 final lift reversed", replace(solved, "rates =", 'lift = rates["B"] / rates["A"] - 1', 'lift = rates["A"] / rates["B"] - 1'), None, ["❌ lift is -0.0376: that's A relative to B"]
    yield "9 final one-sided", replace(solved, "rates =", 'counts.loc[["B", "A"], "count"])', 'counts.loc[["B", "A"], "count"], alternative="larger")'), None, ["❌ p_value is 0.2307: a one-sided test"]
    yield "9 final interval reversed", replace(solved, "rates =", 'confint_proportions_2indep(counts.loc["B", "sum"], counts.loc["B", "count"], counts.loc["A", "sum"], counts.loc["A", "count"])', 'confint_proportions_2indep(counts.loc["A", "sum"], counts.loc["A", "count"], counts.loc["B", "sum"], counts.loc["B", "count"])'), None, ["❌ ci_low and ci_high are A's rate minus B's"]
    yield "9 final not rounded up", replace(solved, "effect =", "users_needed = math.ceil(NormalIndPower().solve_power(effect_size=effect, alpha=0.05, power=0.8))", "users_needed = NormalIndPower().solve_power(effect_size=effect, alpha=0.05, power=0.8)"), None, ["❌ users_needed is 201,506.25"]
    yield "9 final weeks from all users", replace(solved, "effect =", "len(desktop_users) / 2 / TEST_WEEKS", "len(users) / 2 / TEST_WEEKS"), None, ["❌ weeks_needed is 31: that uses all users per week, not desktop users"]
    yield "9 final weeks from both variants", replace(solved, "effect =", "len(desktop_users) / 2 / TEST_WEEKS", "len(desktop_users) / TEST_WEEKS"), None, ["❌ weeks_needed is 44: users_per_week counts both variants"]
    yield "9 final check run twice", solved, twice(solved), ["⚠️ This cell has run before"]
