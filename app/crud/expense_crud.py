from sqlalchemy.orm import Session
from app.models.expense import Expense
from app.schemas.expense_schemas import ExpenseCreate

def create_expense(db: Session, expense: ExpenseCreate):
    db_expense = Expense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    return db_expense

def get_expenses(db: Session):
    return db.query(Expense).all()

def get_statistics(db: Session):
    expenses = db.query(Expense).all()
    total = sum(exp.amount for exp in expenses)
    by_category = {}

    for exp in expenses:
        by_category[exp.category] = by_category.get(exp.category, 0) + exp.amount

    return {"total": total, "by_category": by_category}

def update_expense(db: Session, expense_id: int, updated_data: ExpenseCreate):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if not db_expense:
        return None  

    db_expense.description = updated_data.description
    db_expense.amount = updated_data.amount
    db_expense.category = updated_data.category
    db_expense.date = updated_data.date

    db.commit()
    db.refresh(db_expense)
    return db_expense

def delete_expense(db: Session, expense_id: int):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not db_expense:
        return None  
    
    db.delete(db_expense)
    db.commit()
    return True