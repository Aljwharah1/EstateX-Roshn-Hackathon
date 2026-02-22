#!/usr/bin/env python
"""Test script to verify app can start"""
import sys
import os

os.chdir('c:\\Users\\HP\\EstateX-Roshn-Hackathon')
sys.path.insert(0, '.')

print("=== EstateX Server Startup Test ===\n")

try:
    print("1. Importing FastAPI...")
    from fastapi import FastAPI
    print("   SUCCESS\n")
    
    print("2. Importing app.main...")
    from app.main import app
    print("   SUCCESS\n")
    
    print("3. Checking app configuration...")
    print(f"   App title: {app.title}")
    print(f"   App routes: {len(app.routes)} routes\n")
    
    print("4. Listing routes:")
    for route in app.routes:
        if hasattr(route, 'path'):
            print(f"   - {route.path}")
    print()
    
    print("✓ App is ready to run!")
    print("\nTo start the server, run:")
    print("uvicorn app.main:app --host 127.0.0.1 --port 8000\n")
    
except Exception as e:
    print(f"✗ ERROR: {type(e).__name__}")
    print(f"  {e}\n")
    
    import traceback
    print("Full traceback:")
    traceback.print_exc()
    sys.exit(1)
