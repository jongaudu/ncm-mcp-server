FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ncm_mcp_server/ ./ncm_mcp_server/

EXPOSE 3000

CMD ["python", "-m", "ncm_mcp_server.server"]
