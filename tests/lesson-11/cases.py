"""Lesson 11.'s workbook tests: the solution, the workbook as published, and the common mistakes.

Published as tests/lesson-11/cases.py in team-simmer/data-analysis-in-python and run by
tests/run_tests.py, which provides replace(cells, starts, old, new). Each case is
(name, cells, order, expected lines in the check's output).
"""

CLEAN = "✅ Every cell in this session ran once"
DONE = "Everything matches, in a clean run"


def twice(cells):
    """Run every cell, then the check again: the check should warn that it has run before."""
    return list(range(1, len(cells) + 1)) + [len(cells)]


def cases(load):
    # 11.1 Find where each channel leaks
    book, solved = load("11.1-session-funnel.ipynb"), load("11.1-session-funnel.ipynb", solved=True)
    yield "11.1 solution", solved, None, [CLEAN, "✅ 2,506,005 sessions, one per user and session ID", "✅ 1,331,075 sessions viewed an item, 158,637 added to the cart", "✅ Email converts 6.30% of its sessions and Paid Video 0.65%", "✅ Paid Video: only 3.9% of its item views go into the cart", DONE]
    yield "11.1 as published", book, None, ["❌ sessions should be a DataFrame", "❌ funnel should be a DataFrame", "❌ weakest_cart_channel should be the channel group with the lowest add_to_cart rate"]
    yield "11.1 inner join", replace(solved, "step_events =", 'how="left", validate="one_to_one"', 'how="inner", validate="one_to_one"'), None, ["❌ The sessions table has 1,331,075 rows"]
    yield "11.1 session ID alone", replace(replace(solved, "step_events =", '[step_events["user_pseudo_id"], step_events["ga_session_id"]]', 'step_events["ga_session_id"]'), "step_events =", 'on=["user_pseudo_id", "ga_session_id"], how="left", validate="one_to_one"', 'left_on="ga_session_id", right_index=True, how="left", validate="many_to_one"'), None, ["❌ 1,366,847 sessions viewed an item"]
    yield "11.1 counts not flags", replace(solved, "step_events =", "sessions[STEPS] = sessions[STEPS].fillna(0) > 0", "sessions[STEPS] = sessions[STEPS].fillna(0)"), None, ["❌ The step columns should be True or False"]
    yield "11.1 rates of sessions", replace(solved, "counts =", '"add_to_cart": counts["add_to_cart"] / counts["view_item"]', '"add_to_cart": counts["add_to_cart"] / counts["sessions"]'), None, ["❌ funnel's add_to_cart for Email is 0.1140: the share of all sessions"]
    yield "11.1 idxmax", replace(solved, "counts =", 'funnel["add_to_cart"].idxmin()', 'funnel["add_to_cart"].idxmax()'), None, ["❌ weakest_cart_channel is Email, the strongest"]
    yield "11.1 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # 11.2 Track quarterly cohorts
    book, solved = load("11.2-cohort-retention.ipynb"), load("11.2-cohort-retention.ipynb", solved=True)
    yield "11.2 solution", solved, None, [CLEAN, "✅ 40,126 new customers in 8 quarterly cohorts", "✅ 57,595 orders, each with the calendar quarters", "✅ 18.1% of the customers who started in Q3 2024 ordered again in Q4", "✅ 11.6% of new customers order again in the quarter after they start", DONE]
    yield "11.2 as published", book, None, ["❌ new_customers should be a DataFrame", "❌ cohort_orders should be a DataFrame", "❌ retention should be a DataFrame", "❌ quarter_1_retention should be"]
    yield "11.2 with 2023 customers", replace(solved, "new_customers =", '(customers["created_at"] >= START) & ', ""), None, ["❌ The new_customers table has 53,251 rows"]
    yield "11.2 months", replace(solved, "new_customers =", 'to_period("Q")', 'to_period("M")'), None, ["❌ cohort_sizes should be a Series with one number per quarter"]
    yield "11.2 months over three", replace(solved, "cohort_orders =", """((cohort_orders["created_at"].dt.year - cohort_orders["created_at_customer"].dt.year) * 4
                                   + cohort_orders["created_at"].dt.quarter - cohort_orders["created_at_customer"].dt.quarter)""", """((cohort_orders["created_at"].dt.year - cohort_orders["created_at_customer"].dt.year) * 12
                                   + cohort_orders["created_at"].dt.month - cohort_orders["created_at_customer"].dt.month) // 3"""), None, ["❌ quarters_since should count calendar quarters"]
    yield "11.2 orders not customers", replace(solved, "active =", 'aggfunc="nunique"', 'aggfunc="count"'), None, ["❌ retention for 2024Q3 in quarter 1 is 0.2241: it counts orders"]
    yield "11.2 empty cohort as zero", replace(solved, "active =", "cohort_sizes[active[1].notna()].sum()", "cohort_sizes.sum()"), None, ["❌ quarter_1_retention is 0.0941"]
    yield "11.2 mean of rates", replace(solved, "active =", "active[1].sum() / cohort_sizes[active[1].notna()].sum()", "retention[1].mean()"), None, ["❌ quarter_1_retention is 0.1161: the mean of the cohorts' rates"]
    yield "11.2 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # 11.3 Score every customer
    book, solved = load("11.3-rfm-segments.ipynb"), load("11.3-rfm-segments.ipynb", solved=True)
    yield "11.3 solution", solved, None, [CLEAN, "✅ 41,776 customers, with 61,702 orders and $5,444,750.57 of spend", "✅ The scores: a fifth of the customers", "✅ rfm_segment() names every combination", "✅ 14,069 Lost customers, and 1,448 Champions", DONE]
    yield "11.3 as published", book, None, ["❌ rfm should be a DataFrame", "❌ rfm_segment should be a function", "❌ segment_counts should be a Series"]
    yield "11.3 cancelled orders", replace(solved, "rfm = valid_orders", "rfm = valid_orders", "rfm = orders"), None, ["❌ The rfm table has 43,509 customers"]
    yield "11.3 recency not reversed", replace(solved, 'rfm["r_score"] =', "labels=[5, 4, 3, 2, 1]", "labels=[1, 2, 3, 4, 5]"), None, ["❌ The most recent customers have an r_score of 1"]
    yield "11.3 ranked frequency", replace(solved, 'rfm["r_score"] =', 'pd.cut(rfm["frequency"], bins=[0, 1, 2, 3, 5, np.inf], labels=[1, 2, 3, 4, 5])', 'pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])'), None, ["❌ f_score splits the one-order customers into five equal groups"]
    yield "11.3 scores as categories", replace(solved, 'rfm["r_score"] =', 'rfm["m_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5]).astype(int)', 'rfm["m_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])'), None, ["❌ The scores should be whole numbers"]
    yield "11.3 rules out of order", replace(solved, "def rfm_segment", """    if r_score >= 4 and f_score >= 4:
        return "Champions"
    if f_score >= 3:
        return "Loyal"
""", """    if f_score >= 3:
        return "Loyal"
    if r_score >= 4 and f_score >= 4:
        return "Champions"
"""), None, ["❌ rfm_segment(5, 5) should return 'Champions'. It returns 'Loyal'", "❌ segment_counts should be"]
    yield "11.3 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # 11.4 Find the customer types
    book, solved = load("11.4-customer-clusters.ipynb"), load("11.4-customer-clusters.ipynb", solved=True)
    yield "11.4 solution", solved, None, [CLEAN, "✅ 41,776 customers: 7.9% of their orders used a coupon", "✅ Five columns on one scale", "✅ The silhouette score peaks at 4 clusters, 0.522", "✅ Four types: 2,673 customers who buy with a coupon", "loyal_high_value", DONE]
    yield "11.4 as published", book, None, ["❌ features should be a DataFrame", "❌ scaled should be a 41,776 × 5 array", "❌ inertias and silhouettes should be dictionaries", "❌ The features table should have a cluster column"]
    yield "11.4 no logs", replace(solved, "logged =", 'scaled = StandardScaler().fit_transform(logged)', 'scaled = StandardScaler().fit_transform(features)'), None, ["❌ scaled has no logs"]
    yield "11.4 not scaled", replace(solved, "logged =", 'scaled = StandardScaler().fit_transform(logged)', 'scaled = features.to_numpy()'), None, ["❌ scaled is the features table as it is"]
    yield "11.4 lowest inertia", replace(solved, "inertias =", "best_k = max(silhouettes, key=silhouettes.get)", "best_k = min(inertias, key=inertias.get)"), None, ["❌ best_k is 8, the lowest inertia"]
    yield "11.4 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # 11 final: Compare Email and Paid Social
    book, solved = load("11-email-vs-paid-social.ipynb"), load("11-email-vs-paid-social.ipynb", solved=True)
    yield "11 final solution", solved, None, [CLEAN, "✅ 65,075 orders before CUTOFF", "✅ 7,545 customers created from January to June 2024", "✅ Within a year, 35.3% of Email's customers ordered again, and 19.6% of Paid Social's: 1.8 times as many", "✅ Every customer's RFM segment", "✅ 7.6% of Email's customers are Champions", "Everything matches, in a clean run. Read your text cell again"]
    yield "11 final as published", book, None, ["❌ orders should be a DataFrame", "❌ h1_customers should be a DataFrame", "❌ repeat_rates should be a Series", "❌ rfm should be a DataFrame", "❌ segment_mix should be a DataFrame"]
    yield "11 final no cutoff", replace(solved, "customers =", 'orders = orders[orders["created_at"] < CUTOFF]\n', ""), None, ["❌ The orders table has all 65,106 orders"]
    yield "11 final first order counted", replace(solved, "h1_orders =", '(h1_orders["created_at"] > h1_orders["first_order"])', '(h1_orders["created_at"] >= h1_orders["first_order"])'), None, ["❌ repeat_rates is close to 1 for every channel"]
    yield "11 final no window", replace(solved, "h1_orders =", """
                  & (h1_orders["created_at"] <= h1_orders["first_order"] + pd.Timedelta(days=365))""", ""), None, ["❌ repeat_rates for Email is 0.4246"]
    yield "11 final cancelled left out", replace(solved, "h1_orders =", 'h1_orders = orders[orders["customer_id"].isin(h1_customers["customer_id"])]', 'h1_orders = orders[orders["customer_id"].isin(h1_customers["customer_id"]) & (orders["status"] != "Cancelled")]'), None, ["❌ repeat_rates for Email is 0.3360"]
    yield "11 final cohort by first order", replace(solved, "customers =", 'h1_customers = customers[(customers["created_at"] >= COHORT_START) & (customers["created_at"] < COHORT_END)]', 'first_seen = orders.groupby("customer_id")["created_at"].min()\nh1_customers = customers[customers["customer_id"].isin(first_seen[(first_seen >= COHORT_START) & (first_seen < COHORT_END)].index)]'), None, ["❌ The h1_customers table has 8,801 customers"]
    yield "11 final scored within the cohort", replace(solved, "valid_orders =", 'valid_orders = orders[orders["status"] != "Cancelled"]', 'valid_orders = orders[(orders["status"] != "Cancelled") & orders["customer_id"].isin(h1_customers["customer_id"])]'), None, ["❌ The rfm table should have the 41,776 customers", "❌ segment_mix shows 12.9% of Email's customers as Champions"]
    yield "11 final check run twice", solved, twice(solved), ["⚠️ This cell has run before"]
