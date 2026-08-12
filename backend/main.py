from fastapi import FastAPI

app = FastAPI(title="TravelMind AI")


@app.get("/")
def home():
    return {"message": "TravelMind AI is running!"}