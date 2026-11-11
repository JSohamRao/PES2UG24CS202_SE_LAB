"""Reproduce the expected pre-fix failures without changing the fixed source."""
from pathlib import Path
import os
import shutil
import subprocess
import sys

root = Path(__file__).resolve().parent
work = root / '.work' / 'baseline'
work.mkdir(parents=True, exist_ok=True)
shutil.copyfile(root / 'evidence/baseline/original_movie_tickets.py', work / 'movie_tickets.py')
shutil.copyfile(root / 'test_movie_tickets.py', work / 'test_movie_tickets.py')
shutil.copyfile(root / 'pytest.ini', work / 'pytest.ini')
env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTEST_ADDOPTS='')
commands = [
    ([sys.executable, 'movie_tickets.py'], '\n150,,250\n\n'),
    ([sys.executable, '-m', 'pytest', '-q', '--tb=line', '--color=no',
      '-k', 'no_crash', 'test_movie_tickets.py'], None),
]
for args, stdin in commands:
    print('Running:', subprocess.list2cmdline(args), flush=True)
    result = subprocess.run(args, cwd=work, input=stdin, text=True, env=env)
    if result.returncode != 1:
        raise SystemExit(f'Expected baseline failure (status 1), got {result.returncode}')
print('Original application and fuzz failures reproduced as expected.')
