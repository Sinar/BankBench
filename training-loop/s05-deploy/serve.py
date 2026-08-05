#!/usr/bin/env python3
"""Minimal REST API wrapping the S-02 fine-tuned checkpoint.

Env vars:
  MODEL_PATH  -- path to the fine-tuned checkpoint dir (default: ../s02-finetune/out/checkpoint-final)
  API_KEY     -- bearer token required on every request (generate with `openssl rand -hex 16`)

Run:
  export MODEL_PATH=../s02-finetune/out/checkpoint-final
  export API_KEY=$(openssl rand -hex 16)
  uvicorn serve:app --host 0.0.0.0 --port 8000
"""
import os

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_PATH = os.environ.get("MODEL_PATH", "../s02-finetune/out/checkpoint-final")
API_KEY = os.environ.get("API_KEY")

if not API_KEY:
    raise SystemExit("Set API_KEY before starting the server -- don't run this endpoint unauthenticated.")

app = FastAPI(title="BankBench-MY fine-tuned checkpoint API")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)


class Prompt(BaseModel):
    text: str
    max_new_tokens: int = 200


def check_auth(request: Request):
    auth = request.headers.get("authorization", "")
    if auth != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Missing or invalid bearer token")


@app.post("/generate")
def generate(p: Prompt, request: Request):
    check_auth(request)
    inputs = tokenizer(p.text, return_tensors="pt")
    out = model.generate(**inputs, max_new_tokens=p.max_new_tokens)
    completion = tokenizer.decode(out[0], skip_special_tokens=True)
    return {"completion": completion, "model_path": MODEL_PATH}


@app.get("/health")
def health():
    return {"status": "ok", "model_path": MODEL_PATH}
