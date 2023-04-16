import subprocess
import sys

def run_cmd(cmd):
    result = subprocess.run([*cmd.split(), *(sys.argv[1:])])
    exit(result.returncode)

def lint():
    run_cmd('flake8 --exclude=migrations src')

def tests_ci():
    run_cmd('pytest --cov=. --cov-report=xml')

def tests():
    run_cmd('pytest')
