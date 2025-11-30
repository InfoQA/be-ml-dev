from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Supaya frontend React bisa mengakses API
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Format JSON yang diharuskan oleh API
class RequestBody(BaseModel):
    message: str

@app.post("/")
def home():
    return {"message": "API is running"}

# Endpoint POST yang menerima JSON
@app.post("/process")
def your_api(body: RequestBody):
    return {"received": body}
