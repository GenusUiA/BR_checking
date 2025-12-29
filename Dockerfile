# Используем Python 3.13
FROM python:3.13-slim

# Устанавливаем зависимости для Playwright и system audio (частично)
RUN apt-get update && apt-get install -y \
    wget curl gnupg \
    mpg123 \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libxcomposite1 libxrandr2 libxdamage1 libxfixes3 libx11-xcb1 libxkbcommon0 libglib2.0-0 \
    libgbm1 libasound2 \
    ca-certificates fonts-liberation libappindicator3-1 libatspi2.0-0 libdrm2 libxshmfence1 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Создаём рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY requirements.txt .
COPY . .

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем браузеры Playwright
RUN python -m playwright install

# Запуск скрипта
CMD ["python", "checker.py"]
