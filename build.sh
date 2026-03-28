#!/bin/bash
set -e
cd "$(dirname "$0")"
zip -r OpenProject.alfredworkflow info.plist list_projects.py open_project.py icon.png
echo "Built: OpenProject.alfredworkflow"
