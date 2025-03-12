from fastapi import FastAPI, Depends  # ✅ Import FastAPI and Dependencies
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
import json
import math

from backend.auth import router as auth_router, verify_token  # ✅ Import Authentication Router
from backend.broker import brokerage_accounts

from .database import init_db

init_db()  # Call this to ensure the table is created


from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

app = FastAPI()

from backend import  profile
app.include_router(profile.router) 




# ✅ Set up authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", scopes={})

# ✅ Allow frontend (http://localhost:5173) to access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to ["http://localhost:5173"] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include the authentication router (After `app` is defined)
app.include_router(auth_router, prefix="/auth")

@app.get("/")
def home():
    return {"message": "Welcome to the AI Trading Platform"}

@app.get("/protected")
def protected_route(username: str = Depends(verify_token)):
    return {"message": f"Welcome, {username}! You have access to this protected route."}

@app.get("/market-data/{symbol}")
async def get_market_data(symbol: str):
    try:
        data = await fetch_market_data(symbol)  # Fetch market data
        
        # ✅ Check if data is a Ticker object
        if hasattr(data, '__dict__'):
            data_dict = {k: v for k, v in vars(data).items() if not callable(v) and not isinstance(v, object)}
        else:
            data_dict = dict(data)  # Convert to dictionary if possible

        # ✅ Handle NaN values safely and remove unsupported types
        cleaned_data = {
            k: (None if isinstance(v, float) and math.isnan(v) else v)
            for k, v in data_dict.items()
            if isinstance(v, (int, float, str, list, dict))  # ✅ Only allow JSON-safe types
        }

        return cleaned_data  # ✅ Return cleaned JSON-safe data

    except Exception as e:
        return {"error": str(e)}

app.include_router(brokerage_accounts.router)