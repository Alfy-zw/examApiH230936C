FROM python:3.9.19
WORKDIR /app
COPY /src /app
RUN pip install -r requirements.txt
EXPOSE 3000
CMD python main.py
 