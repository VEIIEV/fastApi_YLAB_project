FROM python:3.10-slim
COPY . .

RUN pip install poetry
RUN poetry install
CMD ["poetry", "run","uvicorn", "python_code.main:app",  "--reload", "--host", "0.0.0.0", "--port", "8000"]
