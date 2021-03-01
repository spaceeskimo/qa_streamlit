FROM python:3.8

WORKDIR /app

ARG PIPENV_TIMEOUT=3600

RUN python3 -m pip install pipenv

# install dependencies first for better cacheability
COPY Pipfile ./
RUN pipenv install

COPY . .

# Expose port
ENV PORT 8501

CMD ["pipenv", "run", "streamlit", "run", "main.py"]

# streamlit-specific commands for config
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /root/.streamlit/credentials.toml'

RUN bash -c 'echo -e "\
[server]\n\
enableCORS = false\n\
" > /root/.streamlit/config.toml'
