# Используем официальный Python образ с поддержкой Rust
FROM python:3.11-slim

# Установим необходимые системные библиотеки
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Rust (нужен для сборки Pydantic v2+ и некоторых C-зависимостей)
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости и устанавливаем
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь исходный код
COPY . .

# Указываем переменные окружения (если нужно)
# ENV BOT_TOKEN=your-token

# Команда запуска
CMD ["python", "main.py"]
