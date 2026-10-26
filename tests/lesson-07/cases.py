"""Lesson 7.'s workbook tests: the solution, the workbook as published, and the common mistakes.

Published as tests/lesson-07/cases.py in team-simmer/data-analysis-in-python and run by
tests/run_tests.py, which provides replace(cells, starts, old, new). Each case is
(name, cells, order, expected lines in the check's output).
"""

CLEAN = "✅ Every cell in this session ran once"
DONE = "Everything matches, in a clean run"


def twice(cells):
    """Run every cell, then the check again: the check should warn that it has run before."""
    return list(range(1, len(cells) + 1)) + [len(cells)]


def cases(load):
    # 7.1 Flatten Black Friday week's events
    book, solved = load("7.1-flatten-events.ipynb"), load("7.1-flatten-events.ipynb", solved=True)
    yield "7.1 solution", solved, None, [CLEAN, "✅ The sample has 4 events and 5 items", "✅ The events table has 12,511 events and 37 columns", "✅ Purchase revenue by the session's medium: (none) $2,492.83, email $2,436.17, and paid social only $254.75", "✅ 1,665 events carry 1,799 items", DONE]
    yield "7.1 as published", book, None, ["❌ sample_table isn't a DataFrame yet", "❌ records should be a list", "❌ revenue_by_medium should be a Series", "❌ item_events should be"]
    yield "7.1 sample not flattened", replace(solved, "sample_table =", "pd.json_normalize(sample_events)", "pd.json_normalize(sample_events, max_level=0)"), None, ["❌ The sample_table table has a geo column"]
    yield "7.1 empty list dropped", replace(solved, "sample_table =", 'sample_table.explode("items")', 'sample_table.explode("items").dropna(subset=["items"])'), None, ["❌ The sample_item_rows table has 5 rows"]
    yield "7.1 item count from rows", replace(solved, "sample_table =", 'sample_table["items"].str.len().sum()', "len(sample_item_rows)"), None, ["❌ sample_item_count is 6"]
    yield "7.1 read_json", replace(solved, "with open(", "events = pd.json_normalize(records)", "events = pd.read_json(EVENTS_FILE, lines=True)"), None, ["❌ The events table has a device column"]
    yield "7.1 read_json then flattened", replace(solved, "with open(", "events = pd.json_normalize(records)", 'events = pd.json_normalize(pd.read_json(EVENTS_FILE, lines=True).to_dict("records"))'), None, ["❌ The events table's user_pseudo_id is a float"]
    yield "7.1 read_json with dtype=False", replace(solved, "with open(", "events = pd.json_normalize(records)", 'events = pd.json_normalize(pd.read_json(EVENTS_FILE, lines=True, dtype=False).to_dict("records"))'), None, ["✅ The events table has 12,511 events"]
    yield "7.1 first-touch medium", replace(solved, "purchases =", "session_traffic_source_last_click.manual_campaign.medium", "traffic_source.medium"), None, ["❌ revenue_by_medium's paid_social is $1,280.03"]
    yield "7.1 purchases counted", replace(solved, "purchases =", '["ecommerce.purchase_revenue"].sum()', '["ecommerce.purchase_revenue"].count()'), None, ["❌ revenue_by_medium counts events"]
    yield "7.1 all events exploded", replace(solved, "item_events =", 'item_rows = item_events.explode("items")', 'item_rows = events.explode("items")'), None, ["❌ The item_rows table has 12,645 rows"]
    yield "7.1 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # 7.2 Unnest the campaigns and viewed items
    book, solved = load("7.2-campaigns-and-items.ipynb"), load("7.2-campaigns-and-items.ipynb", solved=True)
    yield "7.2 solution", solved, None, [CLEAN, "✅ The events table has 12,511 events, and 16 parameter columns", "✅ The sessions' campaigns: 1,171 sessions with a campaign, 811 without UTM tags, and 18 that were tagged but lost their campaign", "✅ 1,115 viewed items, most of them Pants (226) and Swim (162)", "✅ The viewed items add up to their events' value: $68,004.85 both ways", DONE]
    yield "7.2 as published", book, None, ["❌ events isn't a DataFrame yet", "❌ session_starts should be", "❌ viewed_items should be a DataFrame", "❌ item_value and event_value should be numbers"]
    yield "7.2 params not added", replace(solved, "for record in records:", 'for record in records:\n    record["params"] = {param["key"]: param["value"] for param in record["event_params"]}\n', ""), None, ["❌ The events table has no params.campaign.string_value column"]
    yield "7.2 campaigns without NaN", replace(solved, "session_starts =", "value_counts(dropna=False)", "value_counts()"), None, ["❌ campaign_sessions adds up to 1,171 sessions"]
    yield "7.2 every missing campaign", replace(solved, "session_starts =", 'session_starts["params.source.string_value"].notna() & ', ""), None, ["❌ lost_campaigns is 829"]
    yield "7.2 every event's items", replace(solved, "view_records =", 'if record["event_name"] == "view_item"]', "]"), None, ["❌ The viewed_items table has 1,799 rows"]
    yield "7.2 no device column", replace(solved, "view_records =", ', ["device", "category"]', ""), None, ["❌ The viewed_items table should have the columns event_timestamp, user_pseudo_id and device.category"]
    yield "7.2 user_id in meta", replace(solved, "view_records =", '["event_timestamp", "user_pseudo_id"', '["event_timestamp", "user_id"'), None, ["⚠️ A cell stopped with", "❌ viewed_items should be a DataFrame"]
    yield "7.2 by item_category", replace(solved, "view_records =", 'viewed_items["item_category2"]', 'viewed_items["item_category"]'), None, ["❌ views_by_category counts item_category"]
    yield "7.2 every event's value", replace(solved, "item_value =", 'view_events["params.value.double_value"]', 'events["params.value.double_value"]'), None, ["❌ event_value is $92,361.63"]
    yield "7.2 check run twice", solved, twice(solved), ["⚠️ This cell has run before"]

    # Final exercise: Rebuild the purchase report from raw events
    book, solved = load("7-purchase-report.ipynb"), load("7-purchase-report.ipynb", solved=True)
    yield "final solution", solved, None, [CLEAN, "✅ The events table has 12,511 events", "✅ 234 units in 217 items and 150 purchases. Women brought $6,479.78 of item revenue, 63.5% of the week's.", "✅ The item report reconciles: $10,198.06", DONE]
    yield "final as published", book, None, ["❌ records should be a list", "❌ purchase_items should be a DataFrame", "❌ purchase_revenue should be a number"]
    everything = replace(solved, "purchase_records =", 'if record["event_name"] == "purchase"]', "]")
    yield "final every event's items", replace(everything, "purchase_records =", 'string_value"]])', 'string_value"]], errors="ignore")'), None, ["⚠️ A cell stopped with", "❌ The purchase_items table has 1,799 rows"]
    checkouts = replace(solved, "purchase_records =", 'if record["event_name"] == "purchase"]', 'if record["event_name"] in ("purchase", "begin_checkout")]')
    yield "final checkout items too", replace(checkouts, "purchase_records =", 'string_value"]])', 'string_value"]], errors="ignore")'), None, ["⚠️ A cell stopped with", "❌ The purchase_items table has 456 rows"]
    yield "final ecommerce transaction ID", replace(solved, "purchase_records =", '["params", "transaction_id", "string_value"]', '["ecommerce", "transaction_id"]'), None, ["✅ 234 units in 217 items and 150 purchases", DONE]
    yield "final by item_category2", replace(solved, "category_report =", 'groupby("item_category")', 'groupby("item_category2")'), None, ["❌ The category_report table is by item_category2"]
    yield "final price, not item_revenue", replace(solved, "category_report =", '[["item_revenue", "quantity"]].sum()', '[["price", "quantity"]].sum().rename(columns={"price": "item_revenue"})'), None, ["❌ The category_report table's item_revenue for Women is $5,887.01"]
    yield "final rows, not units", replace(solved, "category_report =", '[["item_revenue", "quantity"]].sum()', '.agg({"item_revenue": "sum", "quantity": "count"})'), None, ["❌ The category_report table's quantity for Women is 139"]
    yield "final items sold as rows", replace(solved, "category_report =", 'items_sold = purchase_items["quantity"].sum()', "items_sold = len(purchase_items)"), None, ["❌ items_sold is 217"]
    yield "final items sold as purchases", replace(solved, "category_report =", 'items_sold = purchase_items["quantity"].sum()', "items_sold = len(purchases)"), None, ["❌ items_sold is 150"]
    repeated = replace(solved, "purchase_records =", '["params", "transaction_id", "string_value"]]', '["params", "transaction_id", "string_value"], ["ecommerce", "purchase_revenue"]]')
    repeated = replace(repeated, "purchase_revenue =", 'purchases["params.value.double_value"].sum()', 'purchase_items["ecommerce.purchase_revenue"].astype(float).sum()')
    yield "final revenue on every item row", repeated, None, ["❌ purchase_revenue is $19,099.34"]
    yield "final revenue with tax and shipping", replace(solved, "purchase_revenue =", 'purchases["params.value.double_value"].sum()', '(purchases["params.value.double_value"] + purchases["params.tax.double_value"] + purchases["params.shipping.double_value"]).sum()'), None, ["❌ purchase_revenue is $11,634.75"]
    yield "final every event's value", replace(solved, "purchase_revenue =", 'purchases["params.value.double_value"]', 'events["params.value.double_value"]'), None, ["❌ purchase_revenue is $92,361.63"]
    yield "final check run twice", solved, twice(solved), ["⚠️ This cell has run before"]
