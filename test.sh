#!/usr/bin/env bash

WORKING_DIR="$(dirname "$0")"/

cd "${WORKING_DIR}" || exit 1

function init() {
  export PYTHONPATH=$PYTHONPATH:"${WORKING_DIR}"/django_dsl
}

function check() {
  flake8 "${WORKING_DIR}"/django_dsl
  result_flake8="$?"
  if [ "$result_flake8" -ne 0 ]; then
      echo "Tests failed : PEP-8 Not Compliant"
      exit "$result_flake8"
  fi
}

function run_coverage() {
  FAIL_UNDER="100"
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
}

function usage() {
    echo "Run tests"
    printf "\\t-h --help\\n"
    printf "\\t-c --coverage\\n"
    printf "\\t-s --check\\n"
    printf "\\t-a --all\\n"
    printf "\\n"
    printf "Examples:\\n"
    printf "\\t./test.sh -c\\n"
}


while [ "$1" != "" ]; do
    PARAM=$(echo "$1" | awk -F= '{print $1}')
    # VALUE=$(echo "$1" | awk -F= '{print $2}')
    case $PARAM in
    -h | --help)
        usage
        exit
        ;;
    -c | --coverage)
        init
        coverage
        exit
        ;;
    -s | --check)
        check
        exit
        ;;
    -a | --all)
        init
        check
        run_coverage
        exit
        ;;
    *)
        echo "ERROR: unknown parameter \"$PARAM\""
        usage
        exit 1
        ;;
    esac
    shift
done

init
check
run_coverage
