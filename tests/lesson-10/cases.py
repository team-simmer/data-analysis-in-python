"""Lesson 10.'s workbook tests: the solution, the workbook as published, and the common mistakes.

Published as tests/lesson-10/cases.py in team-simmer/data-analysis-in-python and run by
tests/run_tests.py, which provides replace(cells, starts, old, new). Each case is
(name, cells, order, expected lines in the check's output).
"""

CLEAN = "✅ Every cell in this session ran once"
DONE = "Everything matches, in a clean run"


def twice(cells):
    """Run every cell, then the check again: the check should warn that it has run before."""
    return list(range(1, len(cells) + 1)) + [len(cells)]


def cases(load):
    # 10.1 Model the Paid Search return
    book, solved = load("10.1-revenue-from-spend.ipynb"), load("10.1-revenue-from-spend.ipynb", solved=True)
    yield "10.1 solution", solved, None, [CLEAN, "✅ 104 full weeks: $305,812.10 of Paid Search spend and $728,259.69 of revenue, ROAS 2.38", "✅ On spend alone, each extra dollar comes with $3.19 of revenue", "✅ With demand held constant, each extra dollar comes with $1.98, somewhere from $1.60 to $2.37", DONE]
    yield "10.1 as published", book, None, ["❌ weekly should be a DataFrame", "❌ naive_return should be a number", "❌ spend_return should be a number"]
    yield "10.1 days", replace(solved, "search_daily =", 'weekly = search_daily.resample("W").sum()\nweekly = weekly[days == 7]', "weekly = search_daily"), None, ["❌ The weekly table has 731 rows"]
    yield "10.1 partial week", replace(solved, "search_daily =", "weekly = weekly[days == 7]\n", ""), None, ["❌ The weekly table has 105 rows"]
    yield "10.1 every channel", replace(solved, "search_daily =", 'campaign_days[campaign_days["channel"] == "search"]', "campaign_days"), None, ["❌ The weekly table's spend adds up to", "That's every channel's spend"]
    yield "10.1 intercept", replace(solved, "naive_model =", 'naive_model.params["spend"]', 'naive_model.params["Intercept"]'), None, ["❌ naive_return is -2,385.24: that's the intercept"]
    yield "10.1 reversed", replace(solved, "naive_model =", 'smf.ols("revenue ~ spend", data=weekly).fit()\nnaive_return = naive_model.params["spend"]', 'smf.ols("spend ~ revenue", data=weekly).fit()\nnaive_return = naive_model.params["revenue"]'), None, ["❌ naive_return is 0.2239: that's spend explained by revenue"]
    yield "10.1 no control", replace(solved, "model =", '"revenue ~ spend + organic"', '"revenue ~ spend"'), None, ["❌ spend_return is 3.193, the same as naive_return"]
    yield "10.1 organic coefficient", replace(solved, "model =", 'spend_return = model.params["spend"]', 'spend_return = model.params["organic"]'), None, ["❌ spend_return is 0.839: that's the organic coefficient"]
    yield "10.1 naive interval", replace(solved, "model =", 'model.conf_int().loc["spend"]', 'naive_model.conf_int().loc["spend"]'), None, ["❌ return_low and return_high are naive_model's interval"]
    yield "10.1 90% interval", replace(solved, "model =", "model.conf_int()", "model.conf_int(alpha=0.1)"), None, ["❌ return_low and return_high are a 90% interval"]
    yield "10.1 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # 10.2 Forecast Q2 transactions
    book, solved = load("10.2-weekly-forecast.ipynb"), load("10.2-weekly-forecast.ipynb", solved=True)
    yield "10.2 solution", solved, None, [CLEAN, "✅ Trained on 65 weeks, to the week ending March 30, 2025, and held out the 13 weeks of Q2 2025", "✅ The same week last year is 32.4% off on average", "✅ A trend alone is 50.8% off", "✅ A trend and the season are 8.1% off in a typical week, against 32.4% for the baseline", DONE]
    yield "10.2 as published", book, None, ["❌ The weekly table should have two more columns", "❌ baseline_mape should be a number", "❌ trend_mape should be a number", "❌ seasonal_mape should be a number"]
    yield "10.2 UInt32 week", replace(solved, 'weekly["t"] =', ".week.astype(int)", ".week"), None, ["⚠️ A cell stopped with TypeError", "❌ week_of_year is UInt32"]
    yield "10.2 cut week in test", replace(solved, 'weekly["t"] =', "(weekly.index > TRAIN_END)", "(weekly.index >= TRAIN_END)"), None, ["❌ The test table has 14 weeks"]
    yield "10.2 baseline in percent", replace(solved, "baseline =", "baseline_mape = (", "baseline_mape = 100 * ("), None, ["❌ baseline_mape is 32.39: in percent"]
    yield "10.2 trend in logs", replace(solved, "trend_model =", "np.exp(trend_model.predict(test))", "trend_model.predict(test)"), None, ["❌ trend_mape is 0.988: the forecast is still in logs"]
    yield "10.2 linear trend", replace(replace(solved, "trend_model =", '"np.log(transactions) ~ t"', '"transactions ~ t"'), "trend_model =", "np.exp(trend_model.predict(test))", "trend_model.predict(test)"), None, ["✅ A trend alone is 54.1% off"]
    yield "10.2 leaky", replace(solved, "model =", "data=train", "data=weekly[weekly.index <= TEST_END]"), None, ["❌ seasonal_mape is 0.0397: too good"]
    yield "10.2 leaky, all weeks", replace(solved, "model =", "data=train", "data=weekly"), None, ["❌ seasonal_mape is 0.0417: too good"]
    yield "10.2 additive", replace(replace(solved, "model =", '"np.log(transactions) ~ t + C(week_of_year)"', '"transactions ~ t + C(week_of_year)"'), "model =", "np.exp(model.predict(test))", "model.predict(test)"), None, ["❌ seasonal_mape is 0.0893: the model isn't in logs"]
    yield "10.2 no season", replace(solved, "model =", " + C(week_of_year)", ""), None, ["❌ seasonal_mape is the same as trend_mape"]
    yield "10.2 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # 10 final: Forecast Q4 2025 and score it
    book, solved = load("10-q4-forecast.ipynb"), load("10-q4-forecast.ipynb", solved=True)
    yield "10 final solution", solved, None, [CLEAN, "✅ 104 full weeks: trained on the 91 to September 28, 2025, and held out the 13 of Q4", "✅ In a typical week of Q4 2025, the forecast was 6.2% off", "✅ For the quarter, the forecast said $1,130,903 and Q4 brought $1,151,343: -1.8%", "✅ The chart shows the forecast against the actual weeks", "Everything matches, in a clean run. Read your text cell again"]
    yield "10 final as published", book, None, ["❌ weekly should be a DataFrame", "❌ forecast should be a Series", "❌ forecast_total and actual_total should be numbers", "❌ forecast_ax should be the Axes"]
    yield "10 final partial week", replace(solved, "daily =", "weekly = weekly[days_per_week == 7].copy()", "weekly = weekly.copy()"), None, ["❌ The weekly table has 105 rows"]
    yield "10 final UInt32 week", replace(solved, "daily =", ".week.astype(int)", ".week"), None, ["⚠️ A cell stopped with", "❌ week_of_year is UInt32"]
    yield "10 final cut week in test", replace(solved, "train =", "(weekly.index > TRAIN_END)", "(weekly.index >= TRAIN_END)"), None, ["❌ The test table has 14 weeks"]
    yield "10 final leaky", replace(solved, "model =", "data=train", "data=weekly"), None, ["❌ mape is 0.0311: too good"]
    yield "10 final no season", replace(solved, "model =", " + C(week_of_year)", ""), None, ["❌ mape is 0.2997: the model has a trend, but no yearly season"]
    yield "10 final additive", replace(replace(solved, "model =", '"np.log(revenue) ~ t + C(week_of_year)"', '"revenue ~ t + C(week_of_year)"'), "model =", "np.exp(model.predict(test))", "model.predict(test)"), None, ["❌ mape is 0.1355: the model isn't in logs"]
    yield "10 final forecast in logs", replace(solved, "model =", "np.exp(model.predict(test))", "model.predict(test)"), None, ["❌ forecast's values are around", "they're still in logs"]
    yield "10 final mape in percent", replace(solved, "model =", "mape = (", "mape = 100 * ("), None, ["❌ mape is 6.15: in percent"]
    yield "10 final t restarted", replace(solved, "train =", "len(train), len(test)", "test = test.assign(t=range(len(test)))\nlen(train), len(test)"), None, ["❌ mape is 0.4776: the test weeks' t starts again from 0"]
    yield "10 final no forecast line", replace(solved, "forecast_ax =", 'forecast.plot(ax=forecast_ax, label="Forecast")\n', ""), None, ["❌ forecast_ax should have two lines", "but not the forecast"]
    yield "10 final no legend", replace(solved, "forecast_ax =", "forecast_ax.legend()\n", ""), None, ["❌ The chart has no legend"]
    yield "10 final no title", replace(solved, "forecast_ax =", 'forecast_ax.set_title("Weekly revenue, Q4 2025: forecast from the weeks to September 28 against the actual weeks")\n', ""), None, ["❌ The chart has no title"]
    yield "10 final check run twice", solved, twice(solved), ["⚠️ This cell has run before"]
