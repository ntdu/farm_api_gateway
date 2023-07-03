FROM python:3.9

# RUN apt-get update -y && apt-get install -y --no-install-recommends \
#     mime-support \
#     telnet \
#     iputils-ping \
#     curl \
#     htop \
#     vim \
#     procps \
#     net-tools \
#     python3-dev \
#     && rm -rf /var/lib/apt/lists/*

# RUN mkdir -p /app/statics /app/log/{uwsgi,gunicorn,uvicorn}

WORKDIR /app


COPY pyproject.toml /app/

RUN pip3 install --upgrade pip \
&& pip3 install poetry \
&& poetry config virtualenvs.in-project true \
&& poetry install
# # RUN pip3 install poetry \
# #     && poetry install

COPY . /app/

CMD ["sh", "/app/scripts/run_dev.sh"]