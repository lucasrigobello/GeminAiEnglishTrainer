FROM python:3.9.13

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8501

CMD streamlit run "Speaking Practice.py"