from sqlalchemy.orm import Session
from app import  models, schemas

# Get all expenses for the authenticated user
def get_expenses(db: Session, user_id: int, skip: int = 0, limit: int = 10, category: str = None, days: int = None):
    query = db.query(models.Expense).filter(models.Expense.user_id == user_id) 

    if category:
        query = query.filter(models.Expense.category == category)
    
    if days:
        from datetime import datetime, timedelta
        start_date = datetime.utcnow() - timedelta(days=days)
        query = query.filter(models.Expense.date >= start_date)

    return query.offset(skip).limit(limit).all()

# Create a new expense
def add_expense(db: Session, expense: schemas.ExpenseCreate, user_id: int):
    db_expense = models.Expense(user_id=user_id,**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

# Get an expense by ID
# def get_expense_by_id(db: Session, expense_id: int):
#     return db.query(models.Expense).filter(models.Expense.id == expense_id).first()
def get_expense_by_id(db: Session, expense_id: int, user_id: int):
    return db.query(models.Expense).filter(
        models.Expense.id == expense_id,
        models.Expense.user_id == user_id).first()

# Get total count of expenses
def get_expenses_count(db: Session, user_id: int, category: str = None, days: int = None):
    query = db.query(models.Expense).filter(models.Expense.user_id == user_id)

    if category:
        query = query.filter(models.Expense.category == category)

    if days:
        from datetime import datetime, timedelta
        start_date = datetime.utcnow() - timedelta(days=days)
        query = query.filter(models.Expense.date >= start_date)

    return query.count()

# Update an existing expense
def update_expense(db: Session, user_id: int, expense_id: int, updated_data: schemas.ExpenseUpdate):
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id, models.Expense.user_id == user_id).first()
    if db_expense:
        update_dict = updated_data.dict(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(db_expense, key, value)
        db.commit()
        db.refresh(db_expense)
    return db_expense

# Delete an expense
def delete_expense(db: Session, user_id: int, expense_id: int):
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id, models.Expense.user_id == user_id).first()
    if db_expense:
        db.delete(db_expense)
        db.commit()
        return True 
    return False  
