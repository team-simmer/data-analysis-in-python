"""Check your work for lesson 15.: the campaign-tools project, its git history, module, notebooks and reports.

Run it in your campaign-tools folder, with uv run and the exercise's name, as the topic page shows:

    uv run https://raw.githubusercontent.com/team-simmer/data-analysis-in-python/main/lesson-15/check.py 15.1

It reads the project's files and its git history, and imports campaign_tools.py. It doesn't change anything.
"""

import csv
import importlib
import json
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

PROJECT = "campaign-tools"
EXERCISES = ["15.1", "15.2", "15.3", "final"]
USAGE = "Usage: uv run https://raw.githubusercontent.com/team-simmer/data-analysis-in-python/main/lesson-15/check.py EXERCISE\nEXERCISE is 15.1, 15.2, 15.3 or final."
HELPERS = ["read_export", "read_sessions", "campaign_key", "read_spend"]
# Q3 2024, by platform: (spend, ROAS)
Q2_US_GOOGLE_SPEND = "29048.99"
REPORTS = {
    "us": ("US", {"Google Ads": (41543.36, 1.81), "Meta": (11160.84, 1.53), "YouTube": (4357.55, 1.36)}),
    "ca": ("Canadian", {"Google Ads": (6257.47, 2.67), "Meta": (2662.75, 4.24), "YouTube": (2344.31, 1.56)}),
}
# 2025, by campaign: (number of campaigns, first campaign and its ROAS, last campaign and its ROAS, total spend)
CAMPAIGNS = {
    "us": ("US", 21, ("2025_us_search_blackfriday", 4.73), ("2025_us_facebook_blackfriday", 1.00), 247466.10),
    "ca": ("Canadian", 21, ("2025_ca_instagram_summersale", 7.38), ("2025_ca_youtube_awareness", 2.25), 71238.98),
}
FIX_COMMIT = 'Run git add --renormalize {name}, then git commit -m "Remove the outputs".'


def git(*args):
    """Run git with args in this folder, and return (it worked, what it printed)."""
    done = subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return done.returncode == 0, done.stdout.strip()


def committed_notebook(name, commit="HEAD"):
    """Return the notebook as it is in a commit, or None."""
    worked, text = git("show", f"{commit}:{name}")
    if not worked:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def code(notebook):
    return ["".join(cell["source"]) for cell in notebook.get("cells", []) if cell.get("cell_type") == "code"]


def has_outputs(notebook):
    return any(cell.get("outputs") or cell.get("execution_count") for cell in notebook.get("cells", []) if cell.get("cell_type") == "code")


def output_text(notebook):
    """Return everything the notebook's saved outputs show, as text."""
    text = ""
    for cell in notebook.get("cells", []):
        for output in cell.get("outputs", []):
            text += "".join(output.get("text", "")) + "".join(output.get("data", {}).get("text/plain", ""))
    return text


def read_notebook(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def check_repository(folder, results):
    """Check git, the repository, the name and email, and nbstripout. Return False if the rest can't be checked."""
    if shutil.which("git") is None:
        results.append((False, "git isn't installed, or this terminal can't find it. Install it as topic 15.1. shows, then open a new terminal window."))
        return False
    worked, top = git("rev-parse", "--show-toplevel")
    if not worked:
        results.append((False, "campaign-tools isn't a git repository yet. Run git init in this folder."))
        return False
    if Path(top).resolve() != folder.resolve():
        results.append((False, f"The git repository here is {top}, not the campaign-tools folder. Run git init in this folder, so campaign-tools has a repository of its own."))
        return False
    name, email = git("config", "user.name")[1], git("config", "user.email")[1]
    if not name or not email:
        results.append((False, 'git doesn\'t know who you are. Run git config --global user.name "Your Name" and git config --global user.email "you@example.com".'))
        return False
    results.append((True, "campaign-tools is a git repository, with your name and email."))
    clean_filter = git("config", "--get", "filter.nbstripout.clean")[1]
    attribute = git("check-attr", "filter", "--", "notebook.ipynb")[1]
    if not clean_filter or not attribute.endswith("nbstripout"):
        results.append((False, "nbstripout isn't set up for this project. Run uv add --dev nbstripout, then uv run nbstripout --install."))
        return False
    results.append((True, "nbstripout is set up for this project's notebooks."))
    return True


def check_module(folder, results, functions):
    """Import campaign_tools.py and check that it has the functions. Return the module, or None."""
    if not (folder / "campaign_tools.py").exists():
        results.append((False, "There's no campaign_tools.py in campaign-tools. Create it next to the notebook (topic 15.2.)."))
        return None
    sys.path.insert(0, str(folder))
    try:
        module = importlib.import_module("campaign_tools")
    except Exception as error:
        results.append((False, f"campaign_tools.py can't be imported: {type(error).__name__}: {error}. Fix the line it names."))
        return None
    if not hasattr(module, "pd"):
        results.append((False, "campaign_tools.py doesn't import pandas. Add import pandas as pd at the top: a module only sees what it imports itself."))
        return None
    missing = [name for name in functions if not callable(getattr(module, name, None))]
    if missing:
        results.append((False, f"campaign_tools.py has no {', '.join(name + '()' for name in missing)}. Add {'it' if len(missing) == 1 else 'them'} to the module."))
        return None
    if module.campaign_key(module.pd.Series([" 2024_US_Search_Brand "]))[0] != "2024_us_search_brand":
        results.append((False, "campaign_key() in campaign_tools.py doesn't strip and lowercase campaign names. Copy it from the notebook as it was."))
        return None
    return module


def check_imports(name, notebook, results):
    sources = code(notebook)
    defined = [helper for helper in HELPERS if any(f"def {helper}(" in source for source in sources)]
    imports = any("from campaign_tools import" in source or "import campaign_tools" in source for source in sources)
    if defined:
        results.append((False, f"{name} still defines {', '.join(helper + '()' for helper in defined)}. Replace the Helpers cell with an import from campaign_tools."))
    elif not imports:
        results.append((False, f"{name} doesn't import anything from campaign_tools. Replace the Helpers cell with from campaign_tools import ..."))
    else:
        results.append((True, f"{name} imports its helpers from campaign_tools, and defines none of its own."))


def check_report_outputs(name, notebook, results):
    text = output_text(notebook)
    expected = REPORTS["us"][1]
    if not text.strip():
        results.append((False, f"{name} has no outputs. In JupyterLab, choose Kernel → Restart Kernel and Run All Cells…, and save it."))
    elif Q2_US_GOOGLE_SPEND in text:
        results.append((False, f"{name} still shows Q2 2024's report. Change START, END to Q3 2024, restart the kernel and run all cells, and save."))
    elif not all(f"{spend:.2f}" in text and f"{roas:.2f}" in text for spend, roas in expected.values()):
        results.append((False, f"{name} doesn't show Q3 2024's US numbers: Google Ads 1.81, Meta 1.53 and YouTube 1.36. Check START, END and MARKET, restart the kernel and run all cells, and save."))
    else:
        results.append((True, f"The report in {name} shows Q3 2024's US numbers: Google Ads 1.81, Meta 1.53 and YouTube 1.36."))


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def check_market_csv(folder, market, results):
    label, expected = REPORTS[market]
    path = folder / "reports" / f"{market}.csv"
    if not path.exists():
        results.append((False, f"There's no reports/{market}.csv. Run the notebook's loop over MARKETS, with Kernel → Restart Kernel and Run All Cells…."))
        return
    rows = read_csv(path)
    if not rows or not {"platform", "spend", "roas"} <= set(rows[0]):
        results.append((False, f"reports/{market}.csv should have the columns platform, spend, revenue and roas, without the index: to_csv(..., index=False)."))
        return
    found = {row["platform"]: (float(row["spend"]), float(row["roas"])) for row in rows}
    if any(platform not in found or abs(found[platform][0] - spend) > 0.005 or abs(found[platform][1] - roas) > 0.005 for platform, (spend, roas) in expected.items()):
        results.append((False, f"reports/{market}.csv doesn't have Q3 2024's {label} numbers. Check that market_report() uses its market parameter, not MARKET from the notebook."))
        return
    numbers = ", ".join(f"{platform} {roas:.2f}" for platform, (spend, roas) in expected.items())
    results.append((True, f"reports/{market}.csv has Q3 2024's {label} numbers: {numbers.replace(', YouTube', ' and YouTube')}."))


def check_campaign_csv(folder, market, results):
    label, count, first, last, spend = CAMPAIGNS[market]
    path = folder / "reports" / f"campaigns_{market}.csv"
    if not path.exists():
        results.append((False, f"There's no reports/campaigns_{market}.csv. Run the notebook's loop over MARKETS, with Kernel → Restart Kernel and Run All Cells…."))
        return
    rows = read_csv(path)
    if not rows or not {"platform", "campaign", "spend", "revenue", "roas"} <= set(rows[0]):
        results.append((False, f"reports/campaigns_{market}.csv should have the columns platform, campaign, spend, revenue and roas, without the index: to_csv(..., index=False)."))
        return
    total = sum(float(row["spend"]) for row in rows)
    if len(rows) != count or abs(total - spend) > 0.05:
        results.append((False, f"reports/campaigns_{market}.csv should have 2025's {count} {label} campaigns, with ${spend:,.2f} of spend. It has {len(rows)} rows and ${total:,.2f}. Check that campaign_report() uses its market parameter, and the dates."))
    elif rows[0]["campaign"] != first[0] or abs(float(rows[0]["roas"]) - first[1]) > 0.005:
        results.append((False, f"reports/campaigns_{market}.csv should start with {first[0]} ({first[1]:.2f}): sort by roas, highest first."))
    else:
        if market == "us":
            results.append((True, f"reports/campaigns_us.csv has 2025's {count} US campaigns, from {first[0]} ({first[1]:.2f}) to {last[0]} ({last[1]:.2f})."))
        else:
            results.append((True, f"reports/campaigns_{market}.csv has 2025's {count} {label} campaigns, from {first[0]} ({first[1]:.2f})."))


def check_stripped(name, results):
    notebook = committed_notebook(name)
    if notebook is None:
        results.append((False, f"{name} isn't committed. git add it, and commit."))
    elif has_outputs(notebook):
        results.append((False, f"Your last commit of {name} has outputs: it was committed before nbstripout was set up. {FIX_COMMIT.format(name=name)}"))
    else:
        results.append((True, f"Your last commit of {name} has no outputs."))


def check_committed(paths, results):
    worked, status = git("status", "--porcelain", "--", *paths)
    if status:
        changed = sorted({line.split(maxsplit=1)[1].strip('"') for line in status.splitlines()})
        results.append((False, f"These aren't committed yet: {', '.join(changed)}. git add them, and commit."))
    else:
        results.append((True, "Everything you changed is committed."))


def check_your_work(exercise):
    folder = Path.cwd()
    pyproject = folder / "pyproject.toml"
    if not pyproject.exists():
        print(f"❌ There's no pyproject.toml in {folder}. Use cd to go to the {PROJECT} folder, then run this check again.")
        return False
    name = tomllib.loads(pyproject.read_text(encoding="utf-8")).get("project", {}).get("name")
    if name != PROJECT:
        print(f"❌ This is the {name} project. Lesson 15. is done in {PROJECT}: cd ~/simmer-python/{PROJECT}, then run this check again.")
        return False

    results = []
    if check_repository(folder, results):
        notebook_name = "campaign_roas.ipynb" if exercise == "final" else "market_report.ipynb"
        notebook = read_notebook(folder / notebook_name)
        if notebook is None:
            command = "final" if exercise == "final" else "15.1"
            results.append((False, f"There's no {notebook_name} in campaign-tools. Get it with get_files.py {command}, as the exercise shows."))
        elif exercise == "15.1":
            commits = git("log", "--format=%H", "--", notebook_name)[1].split()
            if not commits:
                results.append((False, f"{notebook_name} isn't committed yet. git add it, and commit."))
            elif len(commits) == 1:
                results.append((False, f"{notebook_name} has 1 commit. Change it to Q3 2024, rerun it, save it, and commit it again."))
            else:
                results.append((True, f"{notebook_name} has {len(commits)} commits."))
                check_stripped(notebook_name, results)
                last, before = committed_notebook(notebook_name, commits[0]), committed_notebook(notebook_name, commits[1])
                last_code, before_code = "\n".join(code(last or {})), "\n".join(code(before or {}))
                if "2024-07-01" not in last_code or "2024-09-30" not in last_code:
                    results.append((False, 'Your last commit doesn\'t report Q3 2024. Set START, END = "2024-07-01", "2024-09-30", rerun and save, and commit.'))
                elif "2024-04-01" not in before_code:
                    results.append((False, "The commit before your last one doesn't report Q2 2024. The history should show the change from Q2 to Q3."))
                else:
                    results.append((True, "Your last commit reports Q3 2024, and the one before it Q2 2024."))
            check_report_outputs(notebook_name, notebook, results)
            check_committed([notebook_name], results)
        elif exercise == "15.2":
            if check_module(folder, results, HELPERS):
                results.append((True, "campaign_tools.py imports, with campaign_key(), read_sessions() and read_spend()."))
            check_imports(notebook_name, notebook, results)
            check_report_outputs(notebook_name, notebook, results)
            check_stripped(notebook_name, results)
            check_committed(["campaign_tools.py", notebook_name], results)
        elif exercise == "15.3":
            if check_module(folder, results, HELPERS + ["market_report"]):
                results.append((True, "campaign_tools.py imports, with campaign_key(), read_sessions(), read_spend() and market_report()."))
            check_market_csv(folder, "us", results)
            check_market_csv(folder, "ca", results)
            check_stripped(notebook_name, results)
            check_committed(["campaign_tools.py", notebook_name, "reports"], results)
        else:
            commits = git("log", "--format=%H", "--", notebook_name)[1].split()
            if len(commits) < 2:
                results.append((False, f"{notebook_name} has {len(commits)} commit{'' if len(commits) == 1 else 's'}. Commit it as you got it, then again after your changes."))
            elif not any("def read_export(" in source for source in code(committed_notebook(notebook_name, commits[-1]) or {})):
                results.append((None, f"{notebook_name} has {len(commits)} commits, but the first one already has your changes. Next time, commit a colleague's notebook before you change it, so the history shows what you changed."))
            else:
                results.append((True, f"{notebook_name} has {len(commits)} commits, starting with your colleague's version."))
            check_imports(notebook_name, notebook, results)
            if check_module(folder, results, HELPERS + ["market_report", "campaign_report"]):
                results.append((True, "campaign_tools.py imports, with campaign_report() next to the helpers and market_report()."))
            check_campaign_csv(folder, "us", results)
            check_campaign_csv(folder, "ca", results)
            check_stripped(notebook_name, results)
            check_committed(["campaign_tools.py", notebook_name, "reports"], results)

    for passed, message in results:
        print({True: "✅ ", False: "❌ ", None: "⚠️ "}[passed] + message)
    if any(passed is False for passed, message in results):
        print("\nFix the first ❌, then run this check again.")
        return False
    print("\nEverything is done.")
    return True


def main():
    sys.stdout.reconfigure(errors="replace")
    if len(sys.argv) != 2 or sys.argv[1] not in EXERCISES:
        sys.exit(USAGE)
    sys.exit(0 if check_your_work(sys.argv[1]) else 1)


main()
