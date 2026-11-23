# Test agent image: Python + Selenium + pytest + Chromium + ChromeDriver
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        chromium \
        chromium-driver \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir selenium pytest

WORKDIR /tests
COPY test_site.py /tests/test_site.py

CMD ["pytest", "-v", "test_site.py"]
