#!/bin/bash
cd /home/kavia/workspace/code-generation/college-management-system-166210-166221/college_management_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

