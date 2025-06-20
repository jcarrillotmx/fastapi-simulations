from fastapi import FastAPI
import sys

print("=== Check Python Executable ===")
print("Python executable:", sys.executable)
print("===============================")

app = FastAPI()


@app.get("/")
def read_root():
    return {"python_executable": sys.executable}
