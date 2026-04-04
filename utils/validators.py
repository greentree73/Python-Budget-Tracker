#!/usr/bin/env python3
"""
Validation Utilities
Input validation functions for the budget tracker

TODO: Complete the validation functions
"""

from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation
import re

def validate_amount(amount_input):
    """
    Validate and convert amount input to Decimal
    
    Args:
        amount_input (str/float/int): Input amount
        
    Returns:
        Decimal: Validated amount
        
    Raises:
        ValueError: If amount is invalid
    """
    # TODO: Implement amount validation
    # 1. Convert to string if needed
    # 2. Remove currency symbols ($, commas)
    # 3. Check if amount is positive
    # 4. Convert to Decimal
    # 5. Ensure max 2 decimal places for currency
    
    if amount_input is None:
        raise ValueError("Amount cannot be empty")

    # Convert to string and clean
    amount_str = str(amount_input).replace("$", "").replace(",", "").strip()

    try:
        amount = Decimal(amount_str)
    except InvalidOperation:
        raise ValueError("Invalid amount format")

    if amount <= 0:
        raise ValueError("Amount must be positive")

    # Ensure max 2 decimal places
    if abs(amount.as_tuple().exponent) > 2:
        raise ValueError("Amount cannot have more than 2 decimal places")

    return amount


def validate_date(date_input):
    """
    Validate and convert date input to date object
    
    Args:
        date_input (str/date): Input date
        
    Returns:
        date: Validated date object
        
    Raises:
        ValueError: If date is invalid
    """
    # TODO: Implement date validation
    # 1. If already a date object, return it
    # 2. If string, try common formats (YYYY-MM-DD, MM/DD/YYYY, etc.)
    # 3. Check if date is not in the future (optional)
    # 4. Check if date is not too old (optional, e.g., > 10 years ago)
    
    if isinstance(date_input, date):
        return date_input

    if not isinstance(date_input, str):
        raise ValueError("Invalid date input")

    date_input = date_input.strip().lower()

    today = date.today()

    formats = ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"]

    parsed_date = None

    for fmt in formats:
        try:
            parsed_date = datetime.strptime(date_input, fmt).date()
            break
        except ValueError:
            continue

    if date_input == "today":
        parsed_date = today

    if not parsed_date:
        raise ValueError("Invalid date format")

    # Optional constraints
    if parsed_date > today:
        raise ValueError("Date cannot be in the future")

    if parsed_date < today - timedelta(days=365 * 10):
        raise ValueError("Date is too far in the past")

    return parsed_date


def validate_transaction_type(transaction_type):
    """
    Validate transaction type
    
    Args:
        transaction_type (str): Transaction type input
        
    Returns:
        str: Validated transaction type ('income' or 'expense')
        
    Raises:
        ValueError: If type is invalid
    """
    # TODO: Implement type validation
    # 1. Convert to lowercase and strip whitespace
    # 2. Accept variations: 'in', 'income', '+' for income
    #                       'out', 'expense', 'exp', '-' for expense
    # 3. Return standardized 'income' or 'expense'
    
    if not transaction_type:
        raise ValueError("Transaction type is required")

    t = str(transaction_type).strip().lower()

    income_aliases = {"income", "in", "+"}
    expense_aliases = {"expense", "exp", "out", "-"}

    if t in income_aliases:
        return "income"
    elif t in expense_aliases:
        return "expense"
    else:
        raise ValueError("Invalid transaction type")


def validate_description(description):
    """
    Validate transaction description
    
    Args:
        description (str): Description input
        
    Returns:
        str: Validated and cleaned description
        
    Raises:
        ValueError: If description is invalid
    """
    # TODO: Implement description validation
    # 1. Strip whitespace
    # 2. Check minimum length (e.g., 3 characters)
    # 3. Check maximum length (e.g., 200 characters)
    # 4. Optional: Clean up extra whitespace
    
    if not description:
        raise ValueError("Description cannot be empty")

    desc = str(description).strip()

    if len(desc) < 3:
        raise ValueError("Description must be at least 3 characters")

    if len(desc) > 200:
        raise ValueError("Description cannot exceed 200 characters")

    # Clean extra whitespace
    desc = re.sub(r"\s+", " ", desc)

    return desc


def validate_category_name(name):
    """
    Validate category name
    
    Args:
        name (str): Category name input
        
    Returns:
        str: Validated category name
        
    Raises:
        ValueError: If name is invalid
    """
    # TODO: Implement category name validation
    # 1. Strip whitespace and title case
    # 2. Check length (2-50 characters)
    # 3. Allow letters, numbers, spaces, and basic punctuation
    # 4. No leading/trailing spaces
    
    if not name:
        raise ValueError("Category name cannot be empty")

    name = str(name).strip().title()

    if len(name) < 2 or len(name) > 50:
        raise ValueError("Category name must be between 2 and 50 characters")

    if not re.match(r"^[A-Za-z0-9\s\-&]+$", name):
        raise ValueError("Category name contains invalid characters")

    return name

def validate_positive_integer(value, field_name="value"):
    """
    Validate positive integer input
    
    Args:
        value (str/int): Input value
        field_name (str): Field name for error messages
        
    Returns:
        int: Validated integer
        
    Raises:
        ValueError: If value is invalid
    """
    # TODO: Implement positive integer validation
    # 1. Convert to int
    # 2. Check if positive (> 0)
    # 3. Provide meaningful error messages using field_name
    
    try:
        val = int(value)
    except (ValueError, TypeError):
        raise ValueError(f"{field_name} must be an integer")

    if val <= 0:
        raise ValueError(f"{field_name} must be positive")

    return val

def is_valid_email(email):
    """
    Basic email validation (optional feature)
    
    Args:
        email (str): Email address
        
    Returns:
        bool: True if valid format
    """
    # TODO: Implement basic email validation using regex
    # Pattern: basic email format with @ and domain
    
    if not email:
        return False

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email))

def validate_date_range(start_date, end_date):
    """
    Validate a date range
    
    Args:
        start_date (date): Start date
        end_date (date): End date
        
    Returns:
        tuple: (start_date, end_date) validated
        
    Raises:
        ValueError: If date range is invalid
    """
    # TODO: Implement date range validation
    # 1. Ensure start_date <= end_date
    # 2. Check reasonable range (not more than 10 years)
    # 3. Both dates not in the future
    
    if not isinstance(start_date, date) or not isinstance(end_date, date):
        raise ValueError("Start and end dates must be date objects")

    if start_date > end_date:
        raise ValueError("Start date cannot be after end date")

    if end_date > date.today():
        raise ValueError("End date cannot be in the future")

    if end_date - start_date > timedelta(days=365 * 10):
        raise ValueError("Date range cannot exceed 10 years")

    return start_date, end_date


def sanitize_input(user_input, max_length=None):
    """
    Sanitize user input for security
    
    Args:
        user_input (str): Raw user input
        max_length (int, optional): Maximum length
        
    Returns:
        str: Sanitized input
    """
    if not isinstance(user_input, str):
        user_input = str(user_input)
    
    # TODO: Implement input sanitization
    # 1. Strip whitespace
    # 2. Remove or escape dangerous characters
    # 3. Limit length if max_length provided
    # 4. Handle Unicode properly
    
    # Strip whitespace
    cleaned = user_input.strip()

    # Remove dangerous characters
    cleaned = re.sub(r"[<>\"'%;()&+]", "", cleaned)

    if max_length and len(cleaned) > max_length:
        cleaned = cleaned[:max_length]

    return cleaned

def main():
    """
    Test the validation functions
    """
    print("✓ Testing Validation Utilities")
    print("=" * 35)
    
    # Test amount validation
    print("\n💰 Testing amount validation:")
    test_amounts = ["25.50", "$1,234.56", "100", "-50", "abc", "0"]
    
    for amount in test_amounts:
        try:
            result = validate_amount(amount)
            print(f"  '{amount}' → {result} ✓")
        except Exception as e:
            print(f"  '{amount}' → Error: {e} ❌")
    
    # Test date validation
    print("\n📅 Testing date validation:")
    test_dates = ["2024-03-15", "03/15/2024", "today", "2030-01-01", "invalid"]
    
    for date_str in test_dates:
        try:
            result = validate_date(date_str)
            print(f"  '{date_str}' → {result} ✓")
        except Exception as e:
            print(f"  '{date_str}' → Error: {e} ❌")
    
    # Test transaction type validation
    print("\n🏷️  Testing transaction type validation:")
    test_types = ["income", "expense", "in", "out", "exp", "+", "-", "invalid"]
    
    for type_str in test_types:
        try:
            result = validate_transaction_type(type_str)
            print(f"  '{type_str}' → '{result}' ✓")
        except Exception as e:
            print(f"  '{type_str}' → Error: {e} ❌")
    
    print("\n💡 Complete the TODO sections to see full validation!")

if __name__ == "__main__":
    main()