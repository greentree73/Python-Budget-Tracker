#!/usr/bin/env python3
"""
Transaction Service
Business logic for managing transactions

TODO: Complete the transaction service methods
"""

from datetime import date, datetime
from decimal import Decimal
from models.transaction import Transaction
from models.category import Category
from utils.validators import validate_amount, validate_date
from utils.formatters import format_currency

class TransactionService:
    """
    Service class for transaction operations
    """
    
    @staticmethod
    def add_transaction(amount, description, transaction_date, category_id, transaction_type):
        """
        Add a new transaction
        
        Args:
            amount (str/float): Transaction amount
            description (str): Transaction description
            transaction_date (str/date): Transaction date
            category_id (int): Category ID
            transaction_type (str): 'income' or 'expense'
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # TODO: Validate and convert inputs
            # 1. Convert amount to Decimal using validate_amount()
            # 2. Convert transaction_date to date object using validate_date()
            # 3. Validate transaction_type is 'income' or 'expense'
            # 4. Check that description is not empty
            
            # TODO: Create and save Transaction object
            # transaction = Transaction(...)
            # return transaction.save()
            
            # 1. Validate amount
            amount = validate_amount(amount)

            # 2. Validate date
            transaction_date = validate_date(transaction_date)

            # 3. Validate type
            transaction_type = transaction_type.strip().lower()
            if transaction_type not in ["income", "expense"]:
                raise ValueError("Transaction type must be 'income' or 'expense'")

            # 4. Validate description
            if not description.strip():
                raise ValueError("Description cannot be empty")

            # 5. Create transaction object
            transaction = Transaction(
            amount=amount,
            description=description.strip(),
            transaction_date=transaction_date,
            category_id =category_id,
            transaction_type=transaction_type
            )

            # 6. Save transaction
            return transaction.save()
           
        except Exception as e:
            print(f"❌ Error adding transaction: {e}")
            return False
    
    @staticmethod
    def update_transaction(transaction_id, amount=None, description=None, 
                         transaction_date=None, category_id=None):
        """
        Update an existing transaction
        
        Args:
            transaction_id (int): Transaction ID to update
            amount (str/float, optional): New amount
            description (str, optional): New description
            transaction_date (str/date, optional): New date
            category_id (int, optional): New category ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        # TODO: Implement transaction update
        # 1. Get existing transaction by ID
        # 2. Update only provided fields
        # 3. Validate updated data
        # 4. Save changes
        
        try:
            # 1. Get existing transaction
            transaction = Transaction.get_by_id(transaction_id)

            if not transaction:
                raise ValueError("Transaction not found")

            # 2. Update fields if provided

            if amount is not None:
                transaction.amount = validate_amount(amount)

            if description is not None:
                if not description.strip():
                    raise ValueError("Description cannot be empty")
                transaction.description = description.strip()

            if transaction_date is not None:
                transaction.transaction_date = validate_date(transaction_date)

            if category_id is not None:
                transaction.category_id = category_id

            # 3. Save changes
            return transaction.save()

        except Exception as e:
            print(f"❌ Error updating transaction: {e}")
            return False
    
    @staticmethod
    def delete_transaction(transaction_id):
        """
        Delete a transaction
        
        Args:
            transaction_id (int): Transaction ID to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        
        try: 
            # 1. Get transaction by ID
            transaction = Transaction.get_by_id(transaction_id)
       
            if not transaction:
                print("❌ Transaction not found")
                return False
        
            # 2. Delete transaction
            return transaction.delete()

        except Exception as e:
            print(f"❌ Error deleting transaction: {e}")
            return False
        
        
    @staticmethod
    def get_transactions(limit=None, transaction_type=None, category_id=None,
                        start_date=None, end_date=None):
        """
        Get transactions with optional filtering
        
        Args:
            limit (int, optional): Maximum number to return
            transaction_type (str, optional): 'income' or 'expense'
            category_id (int, optional): Category ID filter
            start_date (date, optional): Start date filter
            end_date (date, optional): End date filter
            
        Returns:
            list: List of Transaction objects
        """
        # TODO: Implement transaction filtering
        # Use appropriate Transaction class methods based on filters
        
        # Filter by type
        if transaction_type:
            transaction_type = transaction_type.strip().lower()
            transactions = [t for t in transactions if t.type == transaction_type]

        # Filter by category
        if category_id:
            transactions = [t for t in transactions if t.category_id == category_id]

        # Filter by date range
        if start_date:
            start_date = validate_date(start_date)
            transactions = [t for t in transactions if t.transaction_date >= start_date]

        if end_date:
            end_date = validate_date(end_date)
            transactions = [t for t in transactions if t.transaction_date <= end_date]

        # Apply limit
        if limit:
            transactions = transactions[:limit]

        return transactions@staticmethod
    def get_transactions(limit=None, transaction_type=None, category_id=None,
                        start_date=None, end_date=None):
        """
        Get transactions with optional filtering
        
        Args:
            limit (int, optional): Maximum number to return
            transaction_type (str, optional): 'income' or 'expense'
            category_id (int, optional): Category ID filter
            start_date (date, optional): Start date filter
            end_date (date, optional): End date filter
            
        Returns:
            list: List of Transaction objects
        """
        # TODO: Implement transaction filtering
        # Use appropriate Transaction class methods based on filters
        
        transactions = Transaction.get_all()
        # Filter by type
        if transaction_type:
            transaction_type = transaction_type.strip().lower()
            transactions = [t for t in transactions if t.type == transaction_type]

        # Filter by category
        if category_id:
            transactions = [t for t in transactions if t.category_id == category_id]

        # Filter by date range
        if start_date:
            start_date = validate_date(start_date)
            transactions = [t for t in transactions if t.transaction_date >= start_date]

        if end_date:
            end_date = validate_date(end_date)
            transactions = [t for t in transactions if t.transaction_date <= end_date]

        # Apply limit
        if limit:
            transactions = transactions[:limit]

        return transactions



    @staticmethod
    def get_transaction_by_id(transaction_id):
        return Transaction.get_by_id(transaction_id)
    
    @staticmethod
    def search_transactions(search_term):
        """
        Search transactions by description
        
        Args:
            search_term (str): Term to search for
            
        Returns:
            list: List of matching Transaction objects
        """
        # TODO: Implement transaction search
        # Get all transactions and filter by description containing search_term
        
        if not search_term:
            return []

        transactions = Transaction.get_all()
        search_term = search_term.lower()

        return [
              t for t in transactions
            if search_term.lower() in (
                (t.description or "").lower() +
                " " +
                (t.category or "").lower() +
                " " +
                (t.type or "").lower()   
            )
        ]

    
    @staticmethod
    def get_transaction_summary():
        """
        Get summary of all transactions
        
        Returns:
            dict: Summary with totals, counts, etc.
        """
        # TODO: Calculate transaction summary
        # Get all transactions and calculate:
        # - total_income
        # - total_expenses  
        # - net_balance (income - expenses)
        # - transaction_count
        # - average_income, average_expense
        
        transactions = Transaction.get_all()
        
        summary = {
            'total_income': Decimal('0'),
            'total_expenses': Decimal('0'),
            'net_balance': Decimal('0'),
            'transaction_count': len(transactions),
            'income_count': 0,
            'expense_count': 0
        }
        
        # TODO: Loop through transactions and calculate totals
        for t in transactions:
            if t.type == 'income':
                summary['total_income'] += t.amount
                summary['income_count'] += 1
            elif t.type == 'expense':
                summary['total_expenses'] += t.amount
                summary['expense_count'] += 1

        summary['net_balance'] = summary['total_income'] - summary['total_expenses']
        return summary
    
    @staticmethod
    def get_spending_by_category(transaction_type='expense'):
        """
        Get spending/income totals by category
        
        Args:
            transaction_type (str): 'income' or 'expense'
            
        Returns:
            dict: Category names mapped to total amounts
        """
        # TODO: Calculate category totals
        # 1. Get all transactions of specified type
        # 2. Group by category and sum amounts
        # 3. Return as dictionary {category_name: total_amount}
        
        transactions = Transaction.get_all()

        category_totals = {}

        for t in transactions:
            if t.type != transaction_type:
                continue

            # Use category_id (since no category name in transaction model)
            key = f"Category {t.category_id}" if t.category_id else "Uncategorized"
            if key not in category_totals:
                category_totals[key] = Decimal('0')
            category_totals[key] += t.amount

        return category_totals

    
    @staticmethod
    def get_monthly_summary(year=None, month=None):
        """
        Get summary for a specific month
        
        Args:
            year (int, optional): Year (default: current year)
            month (int, optional): Month (default: current month)
            
        Returns:
            dict: Monthly summary data
        """
        if not year:
            year = date.today().year
        if not month:
            month = date.today().month
            
        # TODO: Get transactions for specified month
        # Calculate monthly totals

        transactions = Transaction.get_all()

        monthly_transactions = [
        t for t in transactions
            if t.transaction_date.year == year and t.transaction_date.month == month
        ]

        summary = {
        'total_income': Decimal('0'),
        'total_expenses': Decimal('0'),
        'net_balance': Decimal('0'),
        'transaction_count': len(monthly_transactions)
        }

        for t in monthly_transactions:
            if t.type == 'income':
                summary['total_income'] += t.amount
            elif t.type == 'expense':
                summary['total_expenses'] += t.amount

        summary['net_balance'] = summary['total_income'] - summary['total_expenses']

        return summary
        

def main():
    """
    Test the TransactionService
    """
    print("💼 Testing Transaction Service")
    print("=" * 35)
    
    # Test getting transaction summary
    print("📊 Transaction Summary:")
    summary = TransactionService.get_transaction_summary()
    
    print(f"  Total Income: {format_currency(summary['total_income'])}")
    print(f"  Total Expenses: {format_currency(summary['total_expenses'])}")
    print(f"  Net Balance: {format_currency(summary['net_balance'])}")
    print(f"  Transaction Count: {summary['transaction_count']}")
    
    # Test spending by category
    print("\n📋 Spending by Category:")
    category_spending = TransactionService.get_spending_by_category()
    
    for category, amount in category_spending.items():
        print(f"  {category}: {format_currency(amount)}")
    
    print("\n💡 Complete the TODO sections to see full functionality!")

if __name__ == "__main__":
    main()