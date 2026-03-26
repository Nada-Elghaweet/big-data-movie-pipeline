FROM python:3.11-slim

RUN pip install --no-cache-dir pandas numpy matplotlib

RUN pip install --no-cache-dir seaborn scikit-learn scipy requests jupyter

RUN mkdir -p /app/pipeline/

WORKDIR /app/pipeline/

COPY . /app/pipeline/

CMD ["bash"]