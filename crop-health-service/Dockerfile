FROM python:3.9

WORKDIR /app

COPY pyproject.toml /app/

RUN pip3 install --upgrade pip \
&& pip3 install poetry \
&& poetry config virtualenvs.in-project true \
&& poetry install

COPY . /app/

CMD ["sh", "/app/scripts/run_dev.sh"]