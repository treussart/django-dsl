#!/usr/bin/env bash

export PYTHONPATH=$PYTHONPATH:"$(pwd)"/django_dsl

if [[ "$VIRTUAL_ENV" = "" ]]; then
    if [ ! -d venv ]; then
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        pip install -r test-requirements.txt
    else
        source venv/bin/activate
    fi
fi

FAIL_UNDER="87"
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
if [ "$result_report" -ne 0 ]; then
    echo "Tests failed : Coverage under $FAIL_UNDER %"
    exit "$result_report"
fi
exit
