"""Download a lesson 15 notebook into your campaign-tools project.

Run it in your campaign-tools folder, with uv run and the exercise's name, as the topic page shows:

    uv run https://raw.githubusercontent.com/team-simmer/data-analysis-in-python/main/lesson-15/get_files.py 15.1

It downloads the exercise's notebook from Simmer's GitHub repository into the folder, and never replaces a file
that's already there, so your work is safe if you run it again. It also makes sure .gitignore tells git to
leave the project's .venv and JupyterLab's checkpoint folders alone. It doesn't change anything else.
"""

import os
import sys
import tomllib
import urllib.request
from pathlib import Path

# Where the notebooks are. Simmer's tests set SIMMER_FILES to test a new version before it's published.
FILES = os.environ.get("SIMMER_FILES", "https://raw.githubusercontent.com/team-simmer/data-analysis-in-python/main/lesson-15").rstrip("/")
PROJECT = "campaign-tools"
EXERCISES = {"15.1": "market_report.ipynb", "final": "campaign_roas.ipynb"}
IGNORED = [".venv", ".ipynb_checkpoints/"]
USAGE = "Usage: uv run https://raw.githubusercontent.com/team-simmer/data-analysis-in-python/main/lesson-15/get_files.py EXERCISE\nEXERCISE is 15.1 or final."


def download(url, path):
    """Download url to path, unless the file is already there. Return what was done."""
    if path.exists():
        return f"Already there, not replaced: {path.name}"
    partial = path.with_name(path.name + ".part")
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            partial.write_bytes(response.read())
    except OSError as error:
        partial.unlink(missing_ok=True)
        sys.exit(f"❌ Couldn't download {url}: {error}\n   Check your internet connection and run this again.")
    partial.rename(path)
    return f"✅ Downloaded {path.name}"


def ignore(folder):
    """Add the lines in IGNORED that .gitignore doesn't have yet. Return what was done."""
    gitignore = folder / ".gitignore"
    text = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    lines = {line.strip().rstrip("/") for line in text.splitlines()}
    missing = [entry for entry in IGNORED if entry.rstrip("/") not in lines]
    if not missing:
        return None
    if text and not text.endswith("\n"):
        text += "\n"
    gitignore.write_text(text + "\n".join(missing) + "\n", encoding="utf-8")
    return f"✅ Added {' and '.join(missing)} to .gitignore"


def main():
    sys.stdout.reconfigure(errors="replace")
    if len(sys.argv) != 2 or sys.argv[1] not in EXERCISES:
        sys.exit(USAGE)
    folder = Path.cwd()
    pyproject = folder / "pyproject.toml"
    if not pyproject.exists():
        sys.exit(f"❌ {folder} isn't a project folder: it has no pyproject.toml. Nothing was downloaded.\n   Go to the project first: cd ~/simmer-python/{PROJECT}")
    name = tomllib.loads(pyproject.read_text(encoding="utf-8")).get("project", {}).get("name")
    if name != PROJECT:
        sys.exit(f"❌ This is the {name} project, but lesson 15. is done in {PROJECT}. Nothing was downloaded.\n   Go to it first: cd ~/simmer-python/{PROJECT}")

    notebook = EXERCISES[sys.argv[1]]
    print(download(f"{FILES}/{notebook}", folder / notebook))
    done = ignore(folder)
    if done:
        print(done)
    print(f"\nStart JupyterLab with uv run jupyter lab, and open {notebook}.")


main()
