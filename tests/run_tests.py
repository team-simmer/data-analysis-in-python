"""Run every lesson's workbook tests: the solution and the common mistakes, in a real IPython kernel.

Published as tests/run_tests.py in team-simmer/data-analysis-in-python. Each lesson has
tests/lesson-NN/cases.py with a cases(load) function that yields

    (name, cells, order, expected)

- cells: the workbook's code cells, as text (load(name) gives the workbook as published,
  load(name, solved=True) the one with the solution filled in)
- order: the 1-based cell numbers to run, or None for all of them, top to bottom
- expected: lines the check's output must contain (✅, ❌ or ⚠️ messages), or None to just show the output

The workbooks read the course's data store, as they do in Colab, but from a local copy: every test case
starts a new kernel, and downloading the data store's files again for each one cost real egress (about
140 GB in November 2026, mostly lessons 11. and 13.'s 236 MB events.parquet). The copy is in $DATA_CACHE
(the workflow keeps it between runs with actions/cache), or in the system's temporary folder. Each run
lists the data store and downloads only the files whose generation has changed (every upload gets a new
one; not every object has an MD5), so a change in the data store still reaches the tests. The monthly course check tests the live data store itself.

Run from the repo's root, with the pandas version to test:

    uv run --python 3.13 --with pandas==3.0.2 --with pyarrow --with openpyxl==3.1.5 \
        --with matplotlib==3.10.0 --with seaborn==0.13.2 --with plotly==5.24.1 --with nbformat --with scipy==1.16.3 --with statsmodels==0.15.0 --with scikit-learn==1.6.1 --with ipykernel --with jupyter_client tests/run_tests.py [lesson-02 ...]
"""

import importlib.util
import json
import os
import sys
import tempfile
import urllib.request
from pathlib import Path

from jupyter_client.manager import start_new_kernel

TESTS = Path(__file__).resolve().parent
REPO = TESTS.parent
WORK = Path(tempfile.mkdtemp())
DATA_URL = "https://storage.googleapis.com/simmer-python-course-data/simmer-store/v1/"
BUCKET, PREFIX = "simmer-python-course-data", "simmer-store/v1/"
DATA_CACHE = Path(os.environ.get("DATA_CACHE") or Path(tempfile.gettempdir()) / "simmer-data-store")


def sync_data_store():
    """Copy the data store to DATA_CACHE, downloading only the files that are missing or changed."""
    listing, token = [], ""
    while True:
        url = f"https://storage.googleapis.com/storage/v1/b/{BUCKET}/o?prefix={PREFIX}&fields=items(name,generation,size),nextPageToken"
        with urllib.request.urlopen(url + (f"&pageToken={token}" if token else "")) as response:
            page = json.load(response)
        listing += page.get("items", [])
        token = page.get("nextPageToken")
        if not token:
            break
    manifest_path = DATA_CACHE / "generations.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    downloaded = 0
    for item in listing:
        if item["name"].endswith("/"):
            continue
        local = DATA_CACHE / item["name"][len(PREFIX):]
        if local.exists() and manifest.get(item["name"]) == item["generation"]:
            continue
        local.parent.mkdir(parents=True, exist_ok=True)
        # Download beside the file and rename, so a run that stops halfway never leaves half a file
        part = local.with_name(f"{local.name}.{os.getpid()}.part")
        urllib.request.urlretrieve(DATA_URL + item["name"][len(PREFIX):], part)
        os.replace(part, local)
        manifest[item["name"]] = item["generation"]
        downloaded += int(item["size"])
    manifest_path.write_text(json.dumps(manifest, indent=1))
    print(f"Data store: {len(listing)} files in {DATA_CACHE}, {downloaded / 1e6:,.1f} MB downloaded")


def local_data(cells):
    """The cells with the data store's URL pointing at the local copy, as a file:// URL that
    pd.read_csv(), pd.read_parquet() and urllib.request.urlretrieve() all read."""
    return [source.replace(DATA_URL, DATA_CACHE.resolve().as_uri() + "/") for source in cells]


def code_cells(notebook):
    return ["".join(cell["source"]) for cell in notebook["cells"] if cell["cell_type"] == "code"]


def loader(lesson):
    def load(name, solved=False):
        folder = TESTS / lesson / "solved" if solved else REPO / lesson
        return code_cells(json.loads((folder / name).read_text(encoding="utf-8")))
    return load


def run(cells, order=None):
    """Run the cells in order (1-based numbers) in a new kernel, and return everything they showed."""
    kernel, client = start_new_kernel(kernel_name="python3", cwd=str(WORK))
    cells = local_data(cells)
    shown = ""
    try:
        for number in order or range(1, len(cells) + 1):
            message_id = client.execute(cells[number - 1])
            while True:
                message = client.get_iopub_msg(timeout=300)
                if message["parent_header"].get("msg_id") != message_id:
                    continue
                kind, content = message["msg_type"], message["content"]
                if kind == "stream":
                    shown += content["text"]
                elif kind == "execute_result":
                    shown += content["data"]["text/plain"] + "\n"
                elif kind == "error":
                    shown += f"{content['ename']}: {content['evalue']}\n"
                elif kind == "status" and content["execution_state"] == "idle":
                    break
    finally:
        kernel.shutdown_kernel()
    return shown


def replace(cells, starts, old, new):
    """Return the cells with old replaced by new in the first cell that starts with starts."""
    cells = list(cells)
    i = next(i for i, source in enumerate(cells) if source.startswith(starts))
    assert old in cells[i], (starts, old)
    cells[i] = cells[i].replace(old, new)
    return cells


def lesson_cases(lesson):
    spec = importlib.util.spec_from_file_location(f"cases_{lesson}", TESTS / lesson / "cases.py")
    module = importlib.util.module_from_spec(spec)
    module.replace = replace
    spec.loader.exec_module(module)
    return module.cases(loader(lesson))


def main():
    import pandas
    lessons = sys.argv[1:] or sorted(p.name for p in TESTS.glob("lesson-*") if (p / "cases.py").exists())
    kernel_pandas = run(["import pandas; print(pandas.__version__)"]).strip()
    print(f"Python {sys.version.split()[0]}, pandas {pandas.__version__} (kernel: pandas {kernel_pandas})\n")
    if kernel_pandas != pandas.__version__:
        sys.exit("The kernel doesn't run this environment's pandas, so the tests wouldn't test it.")
    sync_data_store()
    failed = 0
    for lesson in lessons:
        print(f"## {lesson}")
        for name, cells, order, expected in lesson_cases(lesson):
            shown = run(cells, order)
            if expected is None:
                print(f"SHOW {name}\n{shown}")
                continue
            missing = [line for line in expected if line not in shown]
            failed += bool(missing)
            print(("PASS " if not missing else "FAIL ") + name)
            if missing:
                print("  missing: " + "; ".join(missing) + "\n  output:\n" + shown)
        print()
    print(f"{failed} failed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
