#!/bin/bash

# exit when any command fails
set -e

cd /home/conniecc1/Editors-Metrics/Editing-movement-metrics
{
  date
  
  echo "Refreshing 01btable"
  /home/conniecc1/venv/bin/jupyter nbconvert --to notebook --inplace --ExecutePreprocessor.timeout=10800  --execute 01b-new-editor-table.ipynb
  
  echo "Refreshing 02calculation"
  /home/conniecc1/venv/bin/jupyter nbconvert --to notebook --inplace --ExecutePreprocessor.timeout=-1  --execute 02-calculation.ipynb

 echo "Refreshing 03report"
  /home/conniecc1/venv/bin/jupyter nbconvert --to notebook --inplace --ExecutePreprocessor.timeout=10800  --execute 03-report.ipynb



  
} >> /home/conniecc1/Editors-Metrics/Editing-movement-metrics/notebook_update.log 2>&1