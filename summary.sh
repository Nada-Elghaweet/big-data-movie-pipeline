#!/bin/bash
set -e

CONTAINER_NAME=big_data_movies_containerr

docker run --name $CONTAINER_NAME big_data_movies \
bash -c "python ingest.py movies_updated.csv && \
python preprocess.py && \
python analytics.py && \
python visualize.py && \
python cluster.py"

mkdir -p results

docker cp $CONTAINER_NAME:/app/pipeline/data_raw.csv ./results/
docker cp $CONTAINER_NAME:/app/pipeline/data_preprocessed.csv ./results/
docker cp $CONTAINER_NAME:/app/pipeline/insight1.txt ./results/
docker cp $CONTAINER_NAME:/app/pipeline/insight2.txt ./results/
docker cp $CONTAINER_NAME:/app/pipeline/insight3.txt ./results/
docker cp $CONTAINER_NAME:/app/pipeline/summary_histograms.png ./results/
docker cp $CONTAINER_NAME:/app/pipeline/summary_scatter.png ./results/
docker cp $CONTAINER_NAME:/app/pipeline/summary_pairplot.png ./results/
docker cp $CONTAINER_NAME:/app/pipeline/summary_heatmap.png ./results/
docker cp $CONTAINER_NAME:/app/pipeline/clusters.txt ./results/
docker cp $CONTAINER_NAME:/app/pipeline/clusters_A_plot.png ./results/
docker cp $CONTAINER_NAME:/app/pipeline/clusters_B.png ./results/
docker cp $CONTAINER_NAME:/app/pipeline/clusters_C.png ./results/

docker stop $CONTAINER_NAME
docker rm $CONTAINER_NAME

echo "Pipeline finished! All results are now in ./results/"