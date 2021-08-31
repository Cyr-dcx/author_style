FROM python:3.8.6-buster

COPY model_camembert /model_camembert
COPY author_style /author_style
COPY api /api
COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install scikit-learn
RUN pip install gensim

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
