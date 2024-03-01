from fastapi import Depends, FastAPI
from database import SessionLocal, engine
import models
import crud
from sqlalchemy.orm import Session

from schemas import CreateExpenseSchema

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# create expenses (1.2)
@app.post("/expenses")
def create_expenses(create_expense: CreateExpenseSchema, db: Session = Depends(get_db)):
    return crud.create_expense(db, create_expense)


# list of expenses (1.3)
@app.get("/expenses")
def get_expenses(db: Session = Depends(get_db)):
    return crud.get_expenses(db)


# list of expenses using filter (1.4)
@app.get("/expenses/month/{year}/{month}")
def get_expenses_with_filters(year: int, month: int, db: Session = Depends(get_db)):
    return crud.get_expenses_with_filters(year, month, db)




@app.get("/totals")
def get_total(salary:int, db:Session = Depends(get_db)):
    return crud.get_total(db, salary)