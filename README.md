# Software Engineering Labs

Course: UE23CS341A, PES University.

Labs 1-3 retain their existing PDF files. Lab 4 retains its imported code and
Git history. Lab 5 contains only the selected PDF report.
Lab 6 contains the movie ticket coverage tests, measured results, screenshots,
and the original two coverage commits.

| Lab | Topic | Tools and deliverables | Original source |
|-----|-------|------------------------|-----------------|
| 1 | Requirements engineering and use-case modelling | Requirements table, UML, PDF | Existing repository: [Lab 1 report](PES2UG24CS202_Jamula_Soham_Rao_Lab1.pdf) |
| 2 | Agile backlog creation and sprint simulation | Jira, PDF | Existing repository: [Lab 2 report](PES2UG24CS202_JAMULA_SOHAM_RAO_LAB2.pdf) |
| 3 | Architecture selection and modelling | UML, PDF | Existing repository: [Lab 3](PES2UG24CS202_LAB3.pdf) and [architecture report](PES2UG24CS202_Lab_3_Architecture.pdf) |
| 4 | Connect Four development with an AI assistant | Python, unittest, gameplay evidence | [JSohamRao/15_connect_four](https://github.com/JSohamRao/15_connect_four), branch `main`; imported into [lab4](lab4/) |
| 5 | Static code analysis of a museum catalog | Pylint, Bandit, and Flake8 results in a PDF report | [Selected Lab 5 PDF](lab5/PES2UG24CS202_LAB5.pdf), supplied from Downloads |
| 6 | Code and branch coverage analysis of movie tickets | Python, pytest, coverage.py, two test suites, terminal screenshots | [Lab 6](lab6/README.md), imported from [JSohamRao/L6_L7_15_movie_tickets](https://github.com/JSohamRao/L6_L7_15_movie_tickets) |

## Lab 4

Run from `lab4/`:

```powershell
python main.py
python -m unittest discover -s tests -v
```

The imported README documents the assignment and the status of its gameplay
videos and chat-history link. Retain those evidence labels when submitting.

## Lab 5

The selected submission document is
[PES2UG24CS202_LAB5.pdf](lab5/PES2UG24CS202_LAB5.pdf), copied byte-for-byte from
`C:\Users\soham\Downloads\PES2UG24CS202_LAB5.pdf`.

The PDF contains the issue table, verification results, and answers to the
four reflection questions. Lab 5 is submitted as a report only.

## Lab 6

The completed assignment is under `lab6/`, preserving the fork's directory
layout and Git history. The two suites cover all 38 application statements
and all 28 measured branches; all 70 tests pass. Both terminal screenshots
and the baseline/final reports are included.

From the repository root in PowerShell:

```powershell
Set-Location lab6
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r '.\Lab 6\requirements.txt'
Set-Location '.\Lab 6'
..\.venv\Scripts\python.exe -m pytest -q
```

See the [Lab 6 README](lab6/README.md) for the separate line and branch
coverage commands, screenshots, and analysis.

## Extending the repository

Add future work under `lab7/`, `lab8/`, and subsequent lab folders. Keep
lab-specific tests and documentation inside their folders, and use root
`.github/workflows/` for any future GitHub Actions workflows.
