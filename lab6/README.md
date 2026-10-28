# Lab 6: Code and Branch Coverage Analysis

Jamula Soham Rao | PES2UG24CS202 | Section D

Assignment 15: Movie Tickets. Fork of
[SETAPESU26/L6_L7_15_movie_tickets](https://github.com/SETAPESU26/L6_L7_15_movie_tickets).
The supplied application and starter tests are unchanged.

## Code coverage stage

The original two tests cover 19/38 application statements (50%). The expanded
code coverage suite has 14 passing test cases and covers 38/38 statements
(100%), exceeding the handout's 90% target. Coverage is restricted to
`movie_tickets.py` so test code does not inflate the result.

- [Code coverage tests](Lab%206/CodeCoverageTest_movie_tickets_application.py)
- [Terminal screenshot](Lab%206/screenshots/code_coverage.png)
- [Measured report](Lab%206/evidence/line/coverage.txt)
- [Machine-readable report](Lab%206/evidence/line/coverage.json)
- [Original baseline reports](Lab%206/evidence/baseline/)

## Reproduce

From the repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r '.\Lab 6\requirements.txt'
Set-Location '.\Lab 6'
..\.venv\Scripts\python.exe -m coverage run --source=movie_tickets -m pytest -q CodeCoverageTest_movie_tickets_application.py
..\.venv\Scripts\python.exe -m coverage report -m --fail-under=90
```

Line coverage shows executed statements. It does not by itself establish that
both outcomes of every decision or every combination of decisions were tested.
Full coverage also does not prove the absence of bugs.

## Branch coverage stage

The separate branch suite contains 54 passing test cases. It covers all 28
measured control-flow branches and all 38 executable statements, with zero
partial branches. The original suite, line suite and branch suite together
pass all 70 tests.

| Measurement | Original 2 tests | Code suite: 14 tests | Branch suite: 54 tests |
|---|---:|---:|---:|
| Application statements executed | 19/38 (50%) | 38/38 (100%) | 38/38 (100%) |
| Application branches executed | 11/28 (39.29%) | 28/28 (100%)* | 28/28 (100%) |
| Missing statements | 19 | 0 | 0 |
| Missing branches | 17 | 0* | 0 |

\* The line suite was also measured separately with `--branch`; that result is
saved in `Lab 6/evidence/line/branch_comparison.json`. This application's line
suite already reaches full measured branch coverage. The second suite expands
boundary and condition combinations, rather than claiming an artificial
coverage increase between stages.

- [Branch coverage tests](Lab%206/BranchCoverageTest_movie_tickets_application.py)
- [Terminal screenshot](Lab%206/screenshots/branch_coverage.png)
- [Measured report](Lab%206/evidence/branch/coverage.txt)
- [Machine-readable report](Lab%206/evidence/branch/coverage.json)

From `Lab 6/`, after the setup above:

```powershell
..\.venv\Scripts\python.exe -m coverage run --branch --source=movie_tickets -m pytest -q BranchCoverageTest_movie_tickets_application.py
..\.venv\Scripts\python.exe -m coverage report -m --fail-under=90
..\.venv\Scripts\python.exe -m pytest -q
```

Both coverage commands must exit successfully. The JSON report separately
confirms 28 covered branches out of 28; coverage.py's terminal `Cover` column
in branch mode combines statement and branch coverage.

## Test design and analysis

| Function | Important cases asserted |
|---|---|
| `ticket_price` | All three seat types; unknown seats; invalid hours -1 and 24; valid hours 0, 11, 12, 17, 18, 23; weekday/weekend; ages 2, 3, 12, 13, 59, 60, 61; free infants; interacting time/weekend/age adjustments |
| `group_discount` | Invalid ticket counts -1 and 0; counts 1, 4, 5, 9, 10, 11 for student and non-student groups; no student bonus below five tickets |
| `snack_combo` | Small, medium, large and fallback sizes, each with and without a coupon |

Expected results are fixed numeric examples, not calculated by calling or
copying the application logic in a second implementation. Errors assert both
the exception type and the exact message. The tests preserve the supplied
behaviour that any snack size other than small/medium uses the default price.
The application has not been changed to make tests pass.

Line coverage measures executed statements; branch coverage measures decision
outcomes. Function coverage asks whether each function was called (all three
are exercised here). Path coverage asks whether every complete execution path
was taken. No claim of complete path coverage or MC/DC is made: coverage.py's
branch metric does not independently count every operand of `and`/`or`, even
though the branch suite explicitly tests their important combinations.

## Submission evidence

The two screenshots were captured from genuine successful terminal runs and
supplied by the student. Only the final results above 90% are shown in
screenshots; baseline results are retained as text and JSON for analysis.

The first added commit contains the code coverage suite and its screenshot.
The second contains the branch coverage suite and its screenshot. Both are
committed to this personal fork; the course repository remains the upstream.

`show_line_coverage.ps1` and `show_branch_coverage.ps1` rerun the displayed
commands and fail if tests or the coverage target fail. From `Lab 6/`, use
`-Python '..\.venv\Scripts\python.exe'` after creating the repository-local
virtual environment. They save raw coverage data under the corresponding
evidence directory. Text/JSON reports in Git preserve the measured submission
results; they are not automatically overwritten by these display scripts.
