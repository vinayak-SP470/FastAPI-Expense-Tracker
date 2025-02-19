from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, auth, models
from app.database import engine
from app.database import get_db
from sqlalchemy import func
from starlette.responses import JSONResponse
from app.auth import get_current_user
from sqlalchemy import func

router = APIRouter(prefix="/expenses", tags=["Expenses"])

# Function to add an expense for the authenticated user
@router.post("/")
def create_expense(expense: schemas.ExpenseCreate, 
                   db: Session = Depends(get_db), 
                   current_user: models.User = Depends(auth.get_current_user)):
    if expense.amount <= 0:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Invalid amount",
                "success": False,
                "statuscode": 400,
                "message": "Expense amount must be greater than zero"
            }
        )

    new_expense = crud.add_expense(db, expense, current_user.id)
    db.commit()
    
    return {
        "data": {
            "id": new_expense.id,
            "category": new_expense.category,
            "amount": new_expense.amount,
            "description": new_expense.description,
            "date": new_expense.date,
            "user_id": new_expense.user_id
        },
        "success": True,
        "statuscode": 201,
        "message": "Expense added successfully"
    }
    
# Function to retrieve all expenses with pagination for the authenticated user
@router.get("/")
def get_expenses(page: int = 1, 
                 limit: int = 10, 
                 category: str = None, 
                 days: int = None, 
                 db: Session = Depends(get_db), 
                 current_user: models.User = Depends(auth.get_current_user)):
    if page < 1 or limit < 1:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Invalid pagination values",
                "success": False,
                "statuscode": 400,
                "message": "Page and limit values must be greater than zero"
            }
        )

    skip = (page - 1) * limit
    expenses = crud.get_expenses(db=db, skip=skip, limit=limit, category=category, days=days, user_id=current_user.id)
    total_count = crud.get_expenses_count(db=db, category=category, days=days, user_id=current_user.id)

    return {
        "data": {
            "expenses": expenses,
            "totalcount": total_count,
            "page": page
        },
        "success": True,
        "statuscode": 200,
        "message": "Expenses retrieved successfully"
    }

    
# Function to retrieve a specific expense by ID for the authenticated user
@router.get("/{expense_id}/")
def get_expense_by_id(
    expense_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)):
    expense = crud.get_expense_by_id(db=db, expense_id=expense_id, user_id=current_user.id)
    
    if not expense:
        return JSONResponse(
            status_code=404,
            content={
                "error": "Invalid expense ID",
                "success": False,
                "statuscode": 404,
                "message": f"No expense found for ID {expense_id}."
            }
        )

    return {
        "data": expense,
        "success": True,
        "statuscode": 200,
        "message": "Expense retrieved successfully"
    }


# Function to update an expense for the authenticated user
@router.put("/{expense_id}/")
def update_expense(expense_id: int, 
                   updated_data: schemas.ExpenseUpdate, 
                   db: Session = Depends(get_db), 
                   current_user: models.User = Depends(get_current_user)):
    expense = crud.get_expense_by_id(db=db, expense_id=expense_id, user_id=current_user.id)
    if not expense:
        return JSONResponse(
            status_code=404,
            content={
                "error": "Invalid expense ID",
                "success": False,
                "statuscode": 404,
                "message": f"Expense with ID {expense_id} not found."
            }
        )

    if updated_data.amount is not None and updated_data.amount <= 0:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Invalid amount",
                "success": False,
                "statuscode": 400,
                "message": "Expense amount must be greater than zero"
            }
        )

    updated_expense = crud.update_expense(db=db, expense_id=expense_id, updated_data=updated_data, user_id=current_user.id)

    return {
        "data": updated_expense,
        "success": True,
        "statuscode": 200,
        "message": "Expense updated successfully"
    }

# Function to delete an expense for the authenticated user
@router.delete("/{expense_id}/")
def delete_expense(expense_id: int, 
                   db: Session = Depends(get_db), 
                   current_user: models.User = Depends(get_current_user)):
    expense = crud.get_expense_by_id(db=db, expense_id=expense_id, user_id=current_user.id)
    if not expense:
        return JSONResponse(
            status_code=404,
            content={
                "error": "Invalid expense ID",
                "success": False,
                "statuscode": 404,
                "message": f"Expense with ID {expense_id} not found"
            }
        )

    crud.delete_expense(db=db, expense_id=expense_id, user_id=current_user.id)

    return {
        "data": "Expense deleted successfully",
        "success": True,
        "statuscode": 200,
        "message": f"Expense with ID {expense_id} deleted successfully"
    }

# Function to generate a monthly expense report for the authenticated user
@router.get("/report/monthly")
def get_monthly_expense_report(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    category: str = None):
    query = (db.query(
        func.to_char(models.Expense.date, 'YYYY-MM').label('month'),
        func.sum(models.Expense.amount).label('total_spent'))
        .filter(models.Expense.user_id == current_user.id)
        .group_by('month')
        .order_by('month'))

    if category:
        query = query.filter(models.Expense.category == category)

    result = query.all()

    if not result:
        return {
            "data": [],
            "success": True,
            "statuscode": 200,
            "message": "No expenses found for the given category.",
        }

    return {
        "data": [{"month": row.month, "total_spent": row.total_spent} for row in result],
        "success": True,
        "statuscode": 200,
        "message": "Monthly expense report generated successfully.",
    }

