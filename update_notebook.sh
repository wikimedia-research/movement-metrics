#!/bin/bash

# exit when any command fails
set -e

cd /home/conniecc1/Editors-Metrics/Editing-movement-metrics
{
  date
  
  #echo "Fetching revert status of title descriptions"
  #Rscript revert_rate_title-descriptions.R
  
  # echo "Refreshing report v1"
  # /home/bearloga/venv/bin/jupyter nbconvert --ExecutePreprocessor.timeout=900 --execute --to html suggested-edits-v1.ipynb
  # cp suggested-edits-v1.html /srv/published-datasets/wikipedia-android-app-reports
  
  #echo "Fetching revert status of image captions"
  #Rscript revert_rate_image-captions.R
  
  #echo "Refreshing 01atable"
# /home/conniecc1/venv/bin/jupyter nbconvert--to notebook --inplace  --execute Untitled.ipynb
  #/home/conniecc1/venv/bin/jupyter nbconvert --to notebook --inplace --ExecutePreprocessor.timeout=10800  --execute 01a-editor-month-table.ipynb
  
  #echo "Refreshing 01btable"
  #/home/conniecc1/venv/bin/jupyter nbconvert --to notebook --inplace --ExecutePreprocessor.timeout=10800  --execute 01b-new-editor-table.ipynb
  
  echo "Refreshing 02calculation"
  /home/conniecc1/venv/bin/jupyter nbconvert --to notebook --inplace --ExecutePreprocessor.timeout=-1  --execute 02-calculation.ipynb

echo "Refreshing 03report"
  /home/conniecc1/venv/bin/jupyter nbconvert --to notebook --inplace --ExecutePreprocessor.timeout=10800  --execute 03-report.ipynb



  
} >> /home/conniecc1/Editors-Metrics/Editing-movement-metrics/notebook_update.log 2>&1