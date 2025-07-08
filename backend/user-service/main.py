from fastapi import FastAPI
app = FastAPI()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

@app.get("/health")
def healthCheck():
    print("health check")
    return {"status": 200, "message": "OK"}

@app.get("/")
def root():
    return {"message": "Hello World"}