#!/usr/bin/env python
"""Minimal test"""
import sys
import os

os.chdir('c:\\Users\\HP\\EstateX-Roshn-Hackathon')

print("1. Importing FastAPI...")
from fastapi import FastAPI
print("   OK")

print("2. Creating app...")
app = FastAPI()

print("3. Defining root route...")
@app.get("/")
def root():
    return {"msg": "test"}

print("4. Done!")
print(f"   App: {app}")
print(f"   Routes: {len(app.routes)}")
