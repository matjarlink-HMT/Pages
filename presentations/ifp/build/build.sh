#!/bin/bash
set -e
cd "$(dirname "$0")"
python3 merge.py
python3 style.py
rm -f IFP_Complete.pptx
cd merged && zip -Xrq ../IFP_Complete.pptx . && cd ..
python3 /root/.claude/skills/pptx/scripts/office/validate.py IFP_Complete.pptx
