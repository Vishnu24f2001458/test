from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
import re

app = FastAPI()

EXPECTED_SECRET = "mysecretkey24f2001458"

class QuizRequest(BaseModel):
    email: str
    secret: str
    url: str

@app.post("/quiz")
def quiz_handler(data: QuizRequest):

    if EXPECTED_SECRET and data.secret != EXPECTED_SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret")

    result = {
        "fetched": False,
        "answer": None,
        "submitted": False,
        "error": None
    }

    try:
        resp = requests.get(data.url, timeout=10)
        html = resp.text
        result["fetched"] = True
        
        match = re.search(r"answer[:=]\s*(\d+)", html, re.IGNORECASE)
        if match:
            result["answer"] = match.group(1)

    except Exception as e:
        result["error"] = str(e)

    return {
        "status": "ok",
        "result": result
    }

