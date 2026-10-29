"""Run every lesson's workbook tests: the solution and the common mistakes, in a real IPython kernel.

Published as tests/run_tests.py in team-simmer/data-analysis-in-python. Each lesson has
tests/lesson-NN/cases.py with a cases(load) function that yields

    (name, cells, order, expected)

- cells: the workbook's code cells, as text (load(name) gives the workbook as published,
  load(name, solved=True) the one with the solution filled in)
- order: the 1-based cell numbers to run, or None for all of them, top to bottom
- expected: lines the check's output must contain (✅, ❌ or ⚠️ messages), or None to just show the output

The workbooks read their data from the course's data store, as they do in Colab.

Run from the repo's root, with the pandas version to test:

    uv run --python 3.13 --with pandas==3.0.2 --with pyarrow --with openpyxl==3.1.5 \
        --with matplotlib==3.10.0 --with seaborn==0.13.2 --with plotly==5.24.1 --with nbformat --with scipy==1.16.3 --with statsmodels==0.15.0 --with scikit-learn==1.6.1 --with ipykernel --with jupyter_client tests/run_tests.py [lesson-02 ...]
"""

import importlib.util
import json
import sys
import tempfile
from pathlib import Path

from jupyter_client.manager import start_new_kernel

TESTS = Path(__file__).resolve().parent
REPO = TESTS.parent
WORK = Path(tempfile.mkdtemp())


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
