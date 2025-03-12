from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from backend.database import get_db, BrokerageAccount


router = APIRouter()

# ✅ Pydantic Model for Requests
class BrokerageAccountCreate(BaseModel):
    user_id: int  # User who owns the account
    broker: str
    account_number: str

# ✅ Fetch Linked Brokerage Accounts for a User
@router.get("/brokerage-accounts/{user_id}", response_model=List[dict])
def get_brokerage_accounts(user_id: int, db: Session = Depends(get_db)):
    accounts = db.query(BrokerageAccount).filter(BrokerageAccount.user_id == user_id).all()
    return [{"id": acc.id, "broker": acc.broker, "account_number": acc.account_number} for acc in accounts]

# ✅ Add a New Brokerage Account
@router.post("/brokerage-accounts")
def add_brokerage_account(account: BrokerageAccountCreate, db: Session = Depends(get_db)):
    new_account = BrokerageAccount(user_id=account.user_id, broker=account.broker, account_number=account.account_number)
    
    # ✅ Store in MySQL
    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return {"message": "Account added", "account": {
        "id": new_account.id, 
        "broker": new_account.broker, 
        "account_number": new_account.account_number
    }}

# ✅ Remove a Brokerage Account
@router.delete("/brokerage-accounts/{account_id}")
def remove_brokerage_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(BrokerageAccount).filter(BrokerageAccount.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    db.delete(account)
    db.commit()
    
    return {"message": "Account removed"}
