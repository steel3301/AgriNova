FROM python:3.11-slim
WORKDIR /app
COPY ./backend /app
RUN pip install --upgrade pip && pip install -r requirements.txt
ENV FLASK_APP=run.py
CMD ["gunicorn", "run:app", "-b", "0.0.0.0:5000", "-w", "4"]
