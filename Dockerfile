FROM python:alpine

EXPOSE 8000

# Add game_scraper app
COPY ./store_scraper /app
COPY requirements.txt /app

WORKDIR /app

# install python packages
RUN pip install -r ./requirements.txt

# to copy the python dependencies
COPY . /app

# starting gunicorn with 2 workers
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "app:get_app()"]

