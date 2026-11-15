"""Test lesson 15.'s exercises and checks end to end, on macOS or Windows.

Creates a new campaign-tools project with uv in the user folder, sets up git and nbstripout as topic 15.1.
shows, and does every exercise the way a student does: downloads the notebooks with get_files.py, edits them
with the solutions in solutions.json, runs them with jupyter execute, commits them, and runs check.py. It
also runs the checks on the common mistakes, and compares every check's output with what the topic pages say.

Run it with: uv run --python 3.13 test_local.py BASE_URL
BASE_URL is where lesson 15.'s files are published, such as
https://raw.githubusercontent.com/team-simmer/data-analysis-in-python/main/lesson-15

Exits with 1 if anything doesn't match. In GitHub Actions, it also writes what git printed to the run's
summary, for the recording notes.
"""

import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

BASE = sys.argv[1].rstrip("/")
SOLUTIONS = json.loads((Path(__file__).parent / "solutions.json").read_text(encoding="utf-8"))
# A new folder in the user folder, like a student's ~/simmer-python. SIMMER_TEST_ROOT puts it somewhere else.
ROOT = Path(os.environ.get("SIMMER_TEST_ROOT", Path.home() / "simmer-python-test-15"))
PROJECT = ROOT / "campaign-tools"
ENVIRONMENT = dict(os.environ, PYTHONIOENCODING="utf-8", SIMMER_FILES=BASE)
results = []
notes = []

REPOSITORY = "✅ campaign-tools is a git repository, with your name and email."
NBSTRIPOUT = "✅ nbstripout is set up for this project's notebooks."
COMMITTED = "✅ Everything you changed is committed."
DONE = "Everything is done."
US_REPORT = "✅ The report in market_report.ipynb shows Q3 2024's US numbers: Google Ads 1.81, Meta 1.53 and YouTube 1.36."


def run(*command, folder=PROJECT):
    """Run a command, and return everything it printed."""
    done = subprocess.run(list(command), cwd=folder, env=ENVIRONMENT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return done.stdout + done.stderr


def note(title, text):
    notes.append(f"### {title}\n\n```text\n{text.strip()}\n```\n")


def expect(name, shown, lines):
    missing = [line for line in lines if line not in shown]
    results.append((name, not missing))
    print(("PASS " if not missing else "FAIL ") + name)
    if missing:
        print("  missing: " + "; ".join(missing) + "\n  output:\n" + shown)


def check(name, exercise, lines):
    expect(name, run("uv", "run", f"{BASE}/check.py", exercise), lines)


def edit(notebook, cells):
    """Replace the notebook's cells: {"parameters": source, "helpers": source, "report": source}."""
    path = PROJECT / notebook
    data = json.loads(path.read_text(encoding="utf-8"))
    code = [cell for cell in data["cells"] if cell["cell_type"] == "code"]
    for (name, source) in cells.items():
        code[["parameters", "helpers", "report"].index(name)]["source"] = source.splitlines(keepends=True)
    path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def execute(notebook):
    shown = run("uv", "run", "jupyter", "execute", "--inplace", notebook)
    if "Traceback" in shown or "Error" in shown.replace("Executing notebook", ""):
        print(shown)


def commit(message, *paths):
    shown = run("git", "add", *paths) + run("git", "commit", "-m", message)
    return shown


def remove(path):
    def writable(function, name, _):
        os.chmod(name, stat.S_IWRITE)
        function(name)

    if path.exists():
        shutil.rmtree(path, onexc=writable)


def main():
    sys.stdout.reconfigure(errors="replace")
    remove(ROOT)
    ROOT.mkdir()
    note("git --version", run("git", "--version", folder=ROOT))

    # The project as Foundations lessons 9. and 10. left it, with git installed
    note("uv init", run("uv", "init", "--no-package", "--python", "3.13", "campaign-tools", folder=ROOT))
    note("git status in a new uv project", run("git", "status"))
    for setting in [("user.name", "Simmer Test"), ("user.email", "test@example.com"), ("commit.gpgsign", "false")]:
        run("git", "config", *setting)
    run("uv", "add", "--dev", "jupyterlab")
    run("uv", "add", "pandas")
    run("uv", "add", "--dev", "nbstripout")

    # Topic 15.1.
    check("15.1 before nbstripout", "15.1", [REPOSITORY, "❌ nbstripout isn't set up for this project"])
    note("uv run nbstripout --install", run("uv", "run", "nbstripout", "--install"))
    expect("get_files 15.1", run("uv", "run", f"{BASE}/get_files.py", "15.1"), ["✅ Downloaded market_report.ipynb", "✅ Added .ipynb_checkpoints/ to .gitignore"])
    expect("get_files 15.1 again", run("uv", "run", f"{BASE}/get_files.py", "15.1"), ["Already there, not replaced: market_report.ipynb"])
    execute("market_report.ipynb")
    check("15.1 not committed", "15.1", [NBSTRIPOUT, "❌ market_report.ipynb isn't committed yet"])
    note("The first commit: git add and git commit", commit("Add the market report for Q2 2024", "market_report.ipynb"))
    note("git status after a commit", run("git", "status"))
    check("15.1 one commit", "15.1", ["❌ market_report.ipynb has 1 commit"])
    edit("market_report.ipynb", {"parameters": 'import pandas as pd\n\nSTART, END = "2024-07-01", "2024-09-30"  # Q3 2024\nMARKET = "us"'})
    execute("market_report.ipynb")
    note("git diff after changing the dates", run("git", "diff"))
    check("15.1 not committed again", "15.1", ["❌ These aren't committed yet: market_report.ipynb"])
    commit("Report Q3 2024 instead of Q2", "market_report.ipynb")
    note("git log --oneline", run("git", "log", "--oneline"))
    check("15.1 solution", "15.1", [REPOSITORY, NBSTRIPOUT, "✅ market_report.ipynb has 2 commits.", "✅ Your last commit of market_report.ipynb has no outputs.",
                                    "✅ Your last commit reports Q3 2024, and the one before it Q2 2024.", US_REPORT, COMMITTED, DONE])

    # Topic 15.2.
    module = SOLUTIONS["modules"]["15.2"]
    (PROJECT / "campaign_tools.py").write_text(module.replace("import pandas as pd\n", ""), encoding="utf-8")
    check("15.2 helpers still in the notebook", "15.2", ["❌ campaign_tools.py doesn't import pandas", "❌ market_report.ipynb still defines read_export(), read_sessions(), campaign_key(), read_spend()"])
    (PROJECT / "campaign_tools.py").write_text(module, encoding="utf-8")
    edit("market_report.ipynb", SOLUTIONS["cells"]["15.2"])
    execute("market_report.ipynb")
    note("git status with a new module", run("git", "status"))
    check("15.2 not committed", "15.2", ["✅ campaign_tools.py imports, with campaign_key(), read_sessions() and read_spend().", "❌ These aren't committed yet: campaign_tools.py, market_report.ipynb"])
    commit("Move the helpers into campaign_tools.py", "campaign_tools.py", "market_report.ipynb")
    check("15.2 solution", "15.2", [REPOSITORY, NBSTRIPOUT, "✅ campaign_tools.py imports, with campaign_key(), read_sessions() and read_spend().",
                                    "✅ market_report.ipynb imports its helpers from campaign_tools, and defines none of its own.", US_REPORT,
                                    "✅ Your last commit of market_report.ipynb has no outputs.", COMMITTED, DONE])

    # Topic 15.3.
    (PROJECT / "campaign_tools.py").write_text(SOLUTIONS["modules"]["15.3"], encoding="utf-8")
    edit("market_report.ipynb", SOLUTIONS["cells"]["15.3"])
    check("15.3 not run", "15.3", ["❌ There's no reports/us.csv"])
    execute("market_report.ipynb")
    commit("Report every market, one CSV file each", "campaign_tools.py", "market_report.ipynb", "reports")
    check("15.3 solution", "15.3", [REPOSITORY, NBSTRIPOUT, "✅ campaign_tools.py imports, with campaign_key(), read_sessions(), read_spend() and market_report().",
                                    "✅ reports/us.csv has Q3 2024's US numbers: Google Ads 1.81, Meta 1.53 and YouTube 1.36.",
                                    "✅ reports/ca.csv has Q3 2024's Canadian numbers: Google Ads 2.67, Meta 4.24 and YouTube 1.56.",
                                    "✅ Your last commit of market_report.ipynb has no outputs.", COMMITTED, DONE])

    # The final exercise
    expect("get_files final", run("uv", "run", f"{BASE}/get_files.py", "final"), ["✅ Downloaded campaign_roas.ipynb"])
    check("final not committed", "final", ["❌ campaign_roas.ipynb has 0 commits"])
    commit("Add Alex's campaign ROAS notebook as received", "campaign_roas.ipynb")
    check("final helpers still in the notebook", "final", ["❌ campaign_roas.ipynb has 1 commit", "❌ campaign_roas.ipynb still defines read_export()"])
    (PROJECT / "campaign_tools.py").write_text(SOLUTIONS["modules"]["final"], encoding="utf-8")
    edit("campaign_roas.ipynb", SOLUTIONS["cells"]["final"])
    execute("campaign_roas.ipynb")
    commit("Run campaign ROAS for every market with campaign_tools", "campaign_tools.py", "campaign_roas.ipynb", "reports")
    check("final solution", "final", [REPOSITORY, NBSTRIPOUT, "✅ campaign_roas.ipynb has 2 commits, starting with your colleague's version.",
                                      "✅ campaign_roas.ipynb imports its helpers from campaign_tools, and defines none of its own.",
                                      "✅ campaign_tools.py imports, with campaign_report() next to the helpers and market_report().",
                                      "✅ reports/campaigns_us.csv has 2025's 21 US campaigns, from 2025_us_search_blackfriday (4.73) to 2025_us_facebook_blackfriday (1.00).",
                                      "✅ reports/campaigns_ca.csv has 2025's 21 Canadian campaigns, from 2025_ca_instagram_summersale (7.38).",
                                      "✅ Your last commit of campaign_roas.ipynb has no outputs.", COMMITTED, DONE])

    # A commit made without nbstripout's filter keeps the outputs, and the check's fix removes them
    run("git", "-c", "filter.nbstripout.clean=cat", "add", "--renormalize", "campaign_roas.ipynb")
    run("git", "commit", "-m", "Commit with outputs")
    check("final outputs committed", "final", ["❌ Your last commit of campaign_roas.ipynb has outputs", "git add --renormalize campaign_roas.ipynb"])
    run("git", "add", "--renormalize", "campaign_roas.ipynb")
    run("git", "commit", "-m", "Remove the outputs")
    check("final outputs removed", "final", ["✅ Your last commit of campaign_roas.ipynb has no outputs.", DONE])

    remove(ROOT)
    failed = [name for name, passed in results if not passed]
    print(f"\n{len(results) - len(failed)} passed, {len(failed)} failed")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as file:
            file.write(f"## Lesson 15 on {sys.platform}\n\n{len(results) - len(failed)} passed, {len(failed)} failed: {', '.join(failed) or 'none'}\n\n" + "\n".join(notes))
    sys.exit(1 if failed else 0)


main()
