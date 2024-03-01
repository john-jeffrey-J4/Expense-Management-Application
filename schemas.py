from pydantic import BaseModel


class CreateExpenseSchema(BaseModel):
    name: str
    amount: float
    category: str
