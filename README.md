# Data Analysis in Python: exercise workbooks

Exercise workbooks for Simmer's [Data Analysis in Python](https://www.teamsimmer.com) course, part of the Complete Python for Data Analysts program.

Open a workbook from its link in the course. In Colab, choose **File → Save a copy in Drive** and work in your copy. Every workbook reads its data from the course's data store, so there's nothing to upload.

| Lesson | Workbook | Open |
|--------|----------|------|
| 2 | Load April 2024's sessions with the right types | [Open in Colab](https://colab.research.google.com/github/team-simmer/data-analysis-in-python/blob/main/lesson-02/2.1-load-april.ipynb) |
| 2 | Profile May 2024's sessions | [Open in Colab](https://colab.research.google.com/github/team-simmer/data-analysis-in-python/blob/main/lesson-02/2.2-profile-may.ipynb) |
| 2 | Find July's email orders | [Open in Colab](https://colab.research.google.com/github/team-simmer/data-analysis-in-python/blob/main/lesson-02/2.3-email-orders.ipynb) |
| 2 | Rank August's best rows | [Open in Colab](https://colab.research.google.com/github/team-simmer/data-analysis-in-python/blob/main/lesson-02/2.4-rank-august.ipynb) |
| 2 | Stack 2024's twelve exports | [Open in Colab](https://colab.research.google.com/github/team-simmer/data-analysis-in-python/blob/main/lesson-02/2.5-stack-2024.ipynb) |
| 2 | Answer a manager's questions about June 2024 | [Open in Colab](https://colab.research.google.com/github/team-simmer/data-analysis-in-python/blob/main/lesson-02/2-june-questions.ipynb) |

## Tests

`tests/` runs every workbook's solution, and the common mistakes, in a real IPython kernel, and checks what the "Check your work" cell says about each. The Workbook tests workflow runs them on pandas 2.2.3 (Colab's default), 3.0.2 and the latest pandas, on every change and every Monday, because the course's code has to work the same on all of them.

The workbooks and tests are built from the course's source files. Please don't send pull requests here.
