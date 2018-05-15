#!/usr/bin/env bash

export PYTHONPATH=$PYTHONPATH:"$(pwd)"/django_dsl

if [[ "$VIRTUAL_ENV" = "" ]]; then
    if [ ! -d venv ]; then
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
    else
        source venv/bin/activate
    fi
fi

FAIL_UNDER="100"
flake8 .
result_flake8="$?"
if [ "$result_flake8" -ne 0 ]; then
    echo "Tests failed : PEP-8 Not Compliant"
    exit "$result_flake8"
fi
coverage erase
coverage run django_dsl/tests/tests_lexer.py
result_run="$?"
if [ "$result_run" -ne 0 ]; then
    echo "Tests failed"
    exit "$result_run"
fi
coverage run -a django_dsl/tests/tests_parser.py
result_run="$?"
if [ "$result_run" -ne 0 ]; then
    echo "Tests failed"
    exit "$result_run"
fi
coverage report --fail-under="$FAIL_UNDER"
result_report="$?"
coverage html --skip-covered
# Upload coverage to Codacy
if [[ "$TRAVIS" = true && "$CODACY_PROJECT_TOKEN" != "" && "$TRAVIS_JOB_NUM_MIN" = "1" ]]; then
    coverage xml
    python-codacy-coverage -r coverage.xml
fi
if [ "$result_report" -ne 0 ]; then
    echo "Tests failed : Coverage under $FAIL_UNDER %"
    exit "$result_report"
fi
# Upload to pypi
if [[ "$TRAVIS" = true ]]; then
    python setup.py bdist_wheel
    twine upload -u "$PYPI_USERNAME" -p "$PYPI_PASSWORD" dist/*
fi

exit 0
