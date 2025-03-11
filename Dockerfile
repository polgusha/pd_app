FROM python:3.11-slim-bookworm

RUN echo 'deb http://mirror.yandex.ru/debian/ bookworm main contrib non-free non-free-firmware deb-src http://mirror.yandex.ru/debian/ bookworm main contrib non-free non-free-firmware deb http://security.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware deb-src http://security.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware deb http://mirror.yandex.ru/debian/ bookworm-updates main contrib non-free non-free-firmware deb-src http://mirror.yandex.ru/debian/ bookworm-updates main contrib non-free non-free-firmware' > /etc/apt/sources.list && \
    apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Сначала копируем только requirements.txt и устанавливаем зависимости
COPY requirements.txt /app/
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

# Затем копируем остальной код
COPY . /app

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://0.0.0.0:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
