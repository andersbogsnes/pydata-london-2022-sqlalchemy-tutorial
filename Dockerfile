FROM python:3.9



RUN apt-get update         && \
    apt-get install -y        \
            sqlite3           \
            libpq-dev      && \
    python -m pip install virtualenv && \
    virtualenv -p 3.9 /opt/venv

ENV PATH="/opt/venv/bin:$PATH" \
    SHELL="/bin/bash"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt && pip install pgcli

WORKDIR app

COPY notebooks notebooks
COPY data data

CMD ["jupyter", "lab", "--no-browser", "--ip", "0.0.0.0", "--allow-root"]