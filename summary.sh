#!/bin/bash

set -e  

python ingest.py movies_updated.csv  
jupyter nbconvert --to notebook --execute preprocess.ipynb --output preprocess_output.ipynb
jupyter nbconvert --to notebook --execute analytics.ipynb --output analytics_output.ipynb
jupyter nbconvert --to notebook --execute visualize.ipynb --output visualize_output.ipynb
jupyter nbconvert --to notebook --execute cluster.ipynb --output cluster_output.ipynb

echo "Pipeline finished! All outputs are in /app/pipeline."