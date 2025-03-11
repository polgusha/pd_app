FROM python:3.11-slim

# Обновляем список источников и устанавливаем необходимые пакеты
RUN echo "deb http://deb.debian.org/debian bookworm main contrib non-free" > /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian-security bookworm-security main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian bookworm-updates main contrib non-free" >> /etc/apt/sources.list && \
    apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    libgl1-mesa-glx \
    && apt-get clean \
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
