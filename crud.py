from fastapi.exceptions import HTTPException
import models
from sqlalchemy import extract
from sqlalchemy.sql import func


def create_expense(db, expense_details):
    """
    The function `create_expense` adds a new expense record to a database using the provided expense
    details.
    
    :param db: The `db` parameter in the `create_expense` function is typically a database session
    object that allows you to interact with the database. It is used to add a new expense record to the
    database based on the `expense_details` provided. The function creates a new expense object using
    the details provided
    :param expense_details: The `expense_details` parameter likely contains details of an expense that
    needs to be created in the database. It is probably a data structure that holds information such as
    the amount, description, date, category, etc
    :return: The function `create_expense` is returning the `db_expense` object that was created and
    added to the database.
    """
    try:
        db_expense = models.Expenses(**expense_details.dict())
        db.add(db_expense)
        db.commit()
        db.refresh(db_expense)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occured:{str(e)}")
    return db_expense


def get_expenses(db):
    """
    The function `get_expenses` retrieves all expenses from a database using SQLAlchemy ORM and handles
    exceptions by raising an HTTPException with a 500 status code if an error occurs.
    
    :param db: The `db` parameter in the `get_expenses` function is likely an object representing a
    database connection or session. It is used to query the database for expenses data. The function
    attempts to query all expenses from the database using the `query` method on the `db` object. If an
    :return: The function `get_expenses(db)` is returning the result of querying all expenses from the
    database using the `db` connection. If the query is successful, it will return a list of expenses.
    If an exception occurs during the query, it will raise an HTTPException with a status code of 500
    and provide details of the error that occurred.
    """
    try:
        result = db.query(models.Expenses).all()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occured:{str(e)}")
    return result


def get_expenses_with_filters(year, month, db):
    """
    The function `get_expenses_with_filters` retrieves expenses from a database based on the specified
    year and month.
    
    :param year: The `year` parameter is used to specify the year for which you want to retrieve
    expenses from the database
    :param month: The `month` parameter in the `get_expenses_with_filters` function represents the
    specific month for which you want to retrieve expenses from the database. It is typically an integer
    value representing the month (e.g., 1 for January, 2 for February, and so on)
    :param db: The `db` parameter is likely an instance of a database session or connection that allows
    you to interact with a database. In this case, it seems to be used to query the database for
    expenses based on the provided year and month. The function uses this `db` object to query the
    database for
    :return: The function `get_expenses_with_filters` is returning a list of expenses from the database
    that match the specified year and month criteria.
    """
    try:
        result = db.query(models.Expenses).filter(extract('year', models.Expenses.created_at) == year,
                                                  extract('month', models.Expenses.created_at) == month).all()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occured:{str(e)}")
    return result


def get_total(db, salary):
    """
    The function `get_total` calculates the total expenses, remaining amount, and salary based on the
    input parameters.
    
    :param db: The `db` parameter seems to be an object that allows querying a database. It is likely
    used to interact with a database to retrieve information such as total expenses
    :param salary: The `salary` parameter in the `get_total` function represents the total amount of
    money earned by an individual within a specific period, typically before any deductions or expenses.
    This amount is used to calculate the remaining amount after deducting the total expenses incurred
    during the same period
    :return: The function `get_total` returns a dictionary containing the total expenses, salary, and
    remaining amount after deducting the total expenses from the salary.
    """
    try:
        total_expense = db.query(
            func.sum(models.Expenses.amount).label("total_expense")).scalar()
        remaining_amount = salary - total_expense

        result = {
            "total_expense": total_expense,
            "salary": salary,
            "remaining_amount": remaining_amount
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An Error Occured:{str(e)}")

    return result
