# ── Base Image ────────────────────────────────────────
FROM python:3.10-slim

# ── Set Working Directory ─────────────────────────────
WORKDIR /app

# ── Copy Requirements & Install ───────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy App Files ────────────────────────────────────
COPY app/ ./app/
COPY model/ ./model/
COPY conftest.py .

# ── Expose Port ───────────────────────────────────────
EXPOSE 8000

# ── Run Command ───────────────────────────────────────
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]