#!/usr/bin/env python3
"""
Personal Budget Tracker - Main Application
A command-line interface for managing personal finances

TODO: Complete the CLI interface and menu system

Author: Vandana Arora
Date: 3/28/2025
"""

import os
import sys
from datetime import date, datetime
from decimal import Decimal

# Import our modules
from database.connection import DatabaseConnection
from models.transaction import Transaction
from models.category import Category
from services.transaction_service import TransactionService
from services.report_service import ReportService
from utils.validators import validate_amount, validate_date, validate_transaction_type
from utils.formatters import format_currency, format_date

class BudgetTracker:
    """
    Main application class for the Budget Tracker CLI
    """
    
    def __init__(self):
        """
        Initialize the budget tracker application
        """
        self.db = DatabaseConnection()
        self.running = True
    
    def start(self):
        """
        Start the budget tracker application
        """
        # Check database connection
        print("💰 Personal Budget Tracker")
        print("=" * 30)
        
        if not self.db.test_connection():
            print("❌ Cannot connect to database. Please check your setup.")
            print("💡 Make sure PostgreSQL is running and .env is configured.")
            return
        
               
        # Show welcome dashboard
        self.show_dashboard()
        
        # Main application loop
        while self.running:
            self.show_main_menu()
            choice = input("\nEnter your choice: ").strip()
            self.handle_menu_choice(choice)
    
    def show_dashboard(self):
        """
        Display the main dashboard with key information
        """
        # TODO: Implement dashboard display
        # Use ReportService.generate_summary_dashboard()
        
        summary = ReportService.generate_summary_dashboard()
        print(summary)
    
    def show_main_menu(self):
        """
        Display the main menu options
        """
        print("\n" + "=" * 40)
        print("💰 BUDGET TRACKER - MAIN MENU")
        print("=" * 40)
        print("1. 💵 Add Transaction")
        print("2. 📋 View Transactions")
        print("3. ✏️  Edit Transaction")
        print("4. 🗑️  Delete Transaction")
        print("5. 📈 Generate Reports")
        print("6. 🏷️  Manage Categories")
        print("7. 🔍 Search Transactions")
        print("8. ⚙️  Settings")
        print("9. 🚪 Exit")
        print("=" * 40)
    
    def handle_menu_choice(self, choice):
        """
        Handle user menu selection
        
        Args:
            choice (str): User's menu choice
        """
        # TODO: Implement menu choice handling
        # Route to appropriate methods based on choice
        
        if choice == '1':
            self.add_transaction()
        elif choice == '2':
            self.view_transactions()
        elif choice == '3':
            self.edit_transaction()
        elif choice == '4':
            self.delete_transaction()
        elif choice == '5':
            self.generate_reports()
        elif choice == '6':
            self.manage_categories()
        elif choice == '7':
            self.search_transactions()
        elif choice == '8':
            self.show_settings()
        elif choice == '9':
            self.exit_application()
        else:
            print("❌ Invalid choice. Please try again.")
    
    def add_transaction(self):
        """
        Add a new transaction through user input
        """
        print("\n➕ ADD NEW TRANSACTION")
        print("-" * 25)
        
        try:
            # TODO: Implement transaction input
            # 1. Get transaction type (income/expense)
            # 2. Get amount with validation
            # 3. Get description
            # 4. Get category (show list to choose from)
            # 5. Get date (default to today)
            # 6. Create and save transaction
            
            # Example implementation structure:
            # transaction_type = input("Transaction type (income/expense): ")
            # amount_input = input("Amount: $")
            # description = input("Description: ")
            # ... get other inputs ...
            
            # Use TransactionService.add_transaction() to save
            
            # 1. Get transaction type
            transaction_type = input("Transaction type (income/expense): ").strip().lower()

            if transaction_type not in ["income", "expense"]:
                print("❌ Invalid transaction type")
                return

            # 2. Get amount
            try:
                amount = float(input("Amount: "))
            except ValueError:
                print("Invalid number")

            if amount <= 0:
                print("❌ Amount must be greater than zero")
                return

            # 3. Get description
            description = input("Description: ").strip()
            if not description:
                print("Description is required")
                return

            # 4. Show categories
            print("\nAvailable Categories:")
            print("1. Salary")
            print("2. Freelance")
            print("3. Investment")
            print("4. Food")
            print("5. Transportation")
            print("6. Utilities")
            print("7. Entertainment")
            print("8. Healthcare")
            print("9. Education")
            print("10. Shopping")

            category = int(input("Choose category ID: "))
            if category < 1 or category > 10:
                print("❌ Invalid category")
                return

            # 5. Get date
            transaction_date = input("Date (YYYY-MM-DD): ").strip()

            # 6. Save transaction
            TransactionService.add_transaction(
            amount,
            description,
            transaction_date,
            category,
            transaction_type
             )

            print("✅ Transaction added successfully")
            
        except Exception as e:
            print(f"❌ Error adding transaction: {e}")
    
    def view_transactions(self):
        """
        Display transactions with filtering options
        """
        print("\n📋 VIEW TRANSACTIONS")
        print("-" * 20)
        
        # TODO: Implement transaction viewing
        # 1. Ask for filter options (all, recent, by type, by category)
        # 2. Get transactions using appropriate service method
        # 3. Display in formatted table
        # 4. Show pagination if many transactions

        try:
            print("Filter options:")
            print("1. All transactions")
            print("2. By type (income/expense)")
            print("3. By category")
            print("4. By date range")

            choice = input("Choose filter option: ").strip()

            transactions = []

            # 1. All transactions
            if choice == "1":
                transactions = TransactionService.get_transactions()

            # 2. By type
            elif choice == "2":
                t_type = input("Enter type (income/expense): ").strip().lower()
                transactions = TransactionService.get_transactions(transaction_type=t_type)

            # 3. By category
            elif choice == "3":
                try:
                    category_id = int(input("Enter category ID: "))
                except ValueError:
                    print("❌ Invalid category ID")
                    return

                transactions = TransactionService.get_transactions(category_id=category_id)

            # 4. By date range
            elif choice == "4":
                start_date = input("Start date (YYYY-MM-DD): ").strip()
                end_date = input("End date (YYYY-MM-DD): ").strip()

                transactions = TransactionService.get_transactions(
                start_date=start_date,
                end_date=end_date
                )

            else:
                print("❌ Invalid option")
                return

             # Display results
            if not transactions:
                print("No transactions found.")
                return

            print("\nID | Type | Amount | Category | Date | Description")
            print("-" * 60)

            for t in transactions:
                print(f"{t.id} | {t.type} | {t.amount} | {t.category_id} | {t.transaction_date} | {t.description}")

        except Exception as e:
            print(f"❌ Error viewing transactions: {e}")
        
  
    
    def edit_transaction(self):
        """
        Edit an existing transaction
        """
        print("\n✏️  EDIT TRANSACTION")
        print("-" * 18)
        
        # TODO: Implement transaction editing
        # 1. Show recent transactions for selection
        # 2. Ask for transaction ID to edit
        # 3. Load existing transaction
        # 4. Allow editing individual fields
        # 5. Save changes

        try:
            # 1. Show recent transactions
            transactions = TransactionService.get_transactions(limit=10)

            if not transactions:
                print("No transactions available to edit.")
                return

            print("\nRecent Transactions:")
            print("ID | Type | Amount | Category | Date | Description")
            print("-" * 60)

            for t in transactions:
                print(f"{t.id} | {t.type} | {t.amount} | {t.category_id} | {t.transaction_date} | {t.description}")

            # 2. Ask for transaction ID
            try:
                transaction_id = int(input("\nEnter Transaction ID to edit: "))
            except ValueError:
                print("❌ Invalid ID")
                return

            # 3. Load existing transaction
            transaction = TransactionService.get_transaction_by_id(transaction_id)

            if not transaction:
                print("❌ Transaction not found")
                return

            print("\nLeave field empty to keep current value.")

            # 4. Edit fields
            new_amount = input(f"Amount ({transaction.amount}): ").strip()
            new_description = input(f"Description ({transaction.description}): ").strip()
            new_date = input(f"Date ({transaction.transaction_date}): ").strip()
            new_category = input(f"Category ID ({transaction.category_id}): ").strip()

            # 5. Prepare values (only update if provided)
            updated_amount = new_amount if new_amount else None
            updated_description = new_description if new_description else None
            updated_date = new_date if new_date else None
            updated_category = int(new_category) if new_category else None

            # 6. Call service layer
            success = TransactionService.update_transaction(
                transaction_id,
                amount=updated_amount,
                description=updated_description,
                transaction_date=updated_date,
                category_id=updated_category
            )

            if success:
                print("✅ Transaction updated successfully")
            else:
                print("❌ Failed to update transaction")

        except Exception as e:
            print(f"❌ Error editing transaction: {e}")
        
       
    def delete_transaction(self):
        """
        Delete a transaction
        """
        print("\n🗑️  DELETE TRANSACTION")
        print("-" * 20)
        
        # TODO: Implement transaction deletion
        # 1. Show recent transactions
        # 2. Ask for transaction ID
        # 3. Confirm deletion
        # 4. Delete using service
        
        try:
            # 1. Show recent transactions
            transactions = TransactionService.get_transactions(limit=10)

            if not transactions:
                print("No transactions available to delete.")
                return

            print("\nRecent Transactions:")
            print("ID | Type | Amount | Category | Date | Description")
            print("-" * 60)

            for t in transactions:
                print(f"{t.id} | {t.type} | {t.amount} | {t.category_id} | {t.transaction_date} | {t.description}")

            # 2. Ask for transaction ID
            try:
                transaction_id = int(input("\nEnter Transaction ID to delete: "))
            except ValueError:
                print("❌ Invalid ID")
                return

            # 3. Load existing transaction
            transaction = TransactionService.get_transaction_by_id(transaction_id)

            if not transaction:
                print("❌ Transaction not found")
                return
            
            # 4. Confirm deletion
            confirm = input("Are you sure you want to delete this transaction? (y/n): ").strip().lower()

            if confirm != "y":
                print("Deletion cancelled.")
                return

            # 5. Call service layer
            success = TransactionService.delete_transaction(transaction_id)

            if success:
                print("✅ Transaction deleted successfully")
            else:
                print("❌ Failed to delete transaction")

        except Exception as e:
            print(f"❌ Error deleting transaction: {e}")

    
    def generate_reports(self):
        """
        Generate and display financial reports
        """
        print("\n📈 GENERATE REPORTS")
        print("-" * 18)
        
        print("Report Options:")
        print("1. Balance Summary")
        print("2. Category Report")
        print("3. Monthly Report")
        print("4. Trend Analysis")
        print("5. Export Report to File")
        
        # TODO: Implement report generation
        # Use ReportService methods to generate different reports
        # Allow user to choose report type and parameters
             
        choice = input("\nSelect report type (1-5): ").strip()

        report_content = None

        if choice == "1":
            report_content = ReportService.generate_balance_report()
            print(report_content)

        elif choice == "2":
            print("\nSelect type:")
            print("1. Expense")
            print("2. Income")

            t_choice = input("Enter choice: ").strip()
            transaction_type = "expense" if t_choice == "1" else "income"

            report_content = ReportService.generate_category_report(transaction_type)
            print(report_content)

        elif choice == "3":
            try:
                year = int(input("Enter year (e.g., 2026): "))
                month = int(input("Enter month (1-12): "))
            except ValueError:
                print("❌ Invalid year/month")
                return

            report_content = ReportService.generate_monthly_report(year, month)
            print(report_content)

        elif choice == "4":
            report_content = ReportService.generate_trend_report()
            print(report_content)

        elif choice == "5":
            print("\nExport Options:")
            print("1. Balance Summary")
            print("2. Category Report")
            print("3. Monthly Report")
            print("4. Trend Analysis")

            export_choice = input("Choose report to export: ").strip()

            if export_choice == "1":
                report_content = ReportService.generate_balance_report()

            elif export_choice == "2":
                t_choice = input("Expense or Income? ").strip().lower()
                report_content = ReportService.generate_category_report(t_choice)

            elif export_choice == "3":
                try:
                    year = int(input("Enter year: "))
                    month = int(input("Enter month: "))
                except ValueError:
                    print("❌ Invalid input")
                    return
                report_content = ReportService.generate_monthly_report(year, month)

            elif export_choice == "4":
                report_content = ReportService.generate_trend_report()

            else:
                print("❌ Invalid choice")
                return

            filename = input("Enter filename (e.g., report.txt): ").strip()

            ReportService.export_report_to_file(report_content, filename)
            return

        else:
            print("❌ Invalid choice")
            return

        
    def manage_categories(self):
        """
        Manage transaction categories
        """
        print("\n🏷️  MANAGE CATEGORIES")
        print("-" * 19)
        
        print("Category Options:")
        print("1. View All Categories")
        print("2. Add New Category")
        print("3. Edit Category")
        print("4. Delete Category")

        choice = input("Select option: ").strip()
        
        # TODO: Implement category management
        # CRUD operations for categories
        
        try:
            if choice == "1":
                categories = Category.get_all()
                
                if not categories:
                    print("No categories found.")
                    return

                print("\nID | Name | Type | Description")
                print("-" * 40)
            
                for c in categories:
                    print(f"{c.id} | {c.name} | {c.type} | {c.description}")

            elif choice == "2":
                name = input("Category name: ").strip()
                type_ = input("Type (income/expense): ").strip().lower()
                description = input("Description: ").strip()
                category = Category(name=name, category_type=type_, description=description)
                if category.save():
                    print("✅ Category added successfully")

            elif choice == "3":
                category_id = int(input("Enter category ID to edit: "))
                category = Category.get_by_id(category_id)

                if not category:
                    print("❌ Category not found")
                    return

                name = input(f"Name ({category.name}): ").strip()
                type_ = input(f"Type ({category.type}): ").strip()
                description = input(f"Description ({category.description}): ").strip()

                if name:
                    category.name = name
                if type_:
                    category.type = type_
                if description:
                    category.description = description

                if category.save():
                    print("✅ Category updated successfully")

            elif choice == "4":
                category_id = int(input("Enter category ID to delete: "))
                category = Category.get_by_id(category_id)

                if not category:
                    print("❌ Category not found")
                    return

                confirm = input("Are you sure? (y/n): ").strip().lower()
                if confirm != "y":
                    print("Cancelled.")
                    return

                if category.delete():
                    print("✅ Category deleted successfully")

            else:
                print("❌ Invalid option")

        except Exception as e:
            print(f"❌ Error managing categories: {e}")
    
    def search_transactions(self):
        """
        Search transactions by description or other criteria
        """
        print("\n🔍 SEARCH TRANSACTIONS")
        print("-" * 21)
        
        # TODO: Implement transaction search
        # 1. Get search term from user
        # 2. Use TransactionService.search_transactions()
        # 3. Display matching results
             
        # 1. Get search term from user
        search_term = input("Enter search term (description/category/type): ").strip()

        if not search_term:
            print("❌ Search term cannot be empty.")
            return

        # 2. Call service
        results = TransactionService.search_transactions(search_term)

        # 3. Display results
        if not results:
            print("No matching transactions found.")
            return

        print(f"\n✅ Found {len(results)} matching transaction(s):\n")

        for tx in results:
            print("-" * 40)
            print(f"ID: {tx.id}")
            print(f"Date: {format_date(tx.transaction_date)}")
            print(f"Description: {tx.description}")
            print(f"Category: {tx.category}")
            print(f"Type: {tx.type}")
            print(f"Amount: {format_currency(tx.amount)}")
    
        print("-" * 40)
    
    def show_settings(self):
        """
        Display and manage application settings
        """
        print("\n⚙️  SETTINGS")
        print("-" * 10)
        
        print("Settings Options:")
        print("1. View Database Info")
        print("2. Export All Data")
        print("3. Import Data")
        print("4. Reset Application")

        choice = input("Select option: ").strip()
        
        # TODO: Implement settings management
        # Database info, backup/restore, etc.
        
        try:
            if choice == "1":
                print("\n📊 Database Info:")
                print(self.db.get_connection_info())

            elif choice == "2":
                print("\nExporting all data...")
                data = ReportService.export_all_data()
                filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                ReportService.export_to_file(data, filename)
                print(f"✅ Data exported to {filename}")

            elif choice == "3":
                filename = input("Enter import file path: ").strip()
                ReportService.import_from_file(filename)
                print("✅ Data imported successfully")

            elif choice == "4":
                confirm = input("⚠️ This will delete ALL data. Continue? (y/n): ").strip().lower()
                if confirm == "y":
                    ReportService.reset_application()
                    print("✅ Application reset completed")

            else:
                print("❌ Invalid option")

        except Exception as e:
            print(f"❌ Settings error: {e}")
    
    def exit_application(self):
        """
        Exit the application gracefully
        """
        print("\n👋 Thank you for using Budget Tracker!")
        print("Your financial data has been saved.")
        self.running = False
        self.db.disconnect()

    
    def get_user_input(self, prompt, validator=None, required=True):
        """
        Get validated user input
        
        Args:
            prompt (str): input prompt
            validator (function): Validation function
            required (bool): Whether input is required
            
        Returns:
            str: Validated user input
        """
        # TODO: Implement robust user input handling
        # 1. Display prompt
        # 2. Get input
        # 3. Validate if validator provided
        # 4. Retry on validation error
        # 5. Handle empty input based on required flag
        
        while True:
            user_input = input(prompt).strip()

            if not user_input and required:
                print("❌ This field is required.")
                continue

            if not user_input and not required:
                return None

            if validator:
                try:
                    return validator(user_input)
                except Exception as e:
                    print(f"❌ Invalid input: {e}")
                    continue

            return user_input  
    
    def display_transactions_table(self, transactions, page_size=10):
        """
        Display transactions in a formatted table
        
        Args:
            transactions (list): List of Transaction objects
            page_size (int): Number of transactions per page
        """
        # TODO: Implement transaction table display
        # Use utils.formatters for proper formatting
        # Include pagination for large lists
        
        if not transactions:
            print("No transactions found.")
            return

        total = len(transactions)

        for i in range(0, total, page_size):
            chunk = transactions[i:i + page_size]

            print("\nID | Type | Amount | Category | Date | Description")
            print("-" * 60)

            for t in chunk:
                print(f"{t.id} | {t.type} | {format_currency(t.amount)} | {t.category_id} | {format_date(t.transaction_date)} | {t.description}")

            if i + page_size < total:
                input("\nPress Enter to continue...")

def check_environment():
    """
    Check if the environment is properly set up
    
    Returns:
        bool: True if environment is ready
    """
    # TODO: Implement environment checks
    # 1. Check if .env file exists
    # 2. Check required environment variables
    # 3. Check database connectivity
    # 4. Provide helpful error messages
    
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("💡 Copy .env.example to .env and configure your database settings")
        return False
    
    required_vars = ["DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT"]

    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)

    if missing:
        print(f"❌ Missing environment variables: {', '.join(missing)}")
        return False

    return True

def main():
    """
    Main application entry point
    """
    try:
        # Check environment setup
        if not check_environment():
            print("\n⚠️  Please set up your environment before running the application.")
            print("\n📌 Setup steps:")
            print("   1. Copy .env.example to .env")
            print("   2. Configure database settings in .env")
            print("   3. Run schema.sql to create database tables")
            print("   4. Run seed_data.sql to add sample data (optional)")
            return
        
        # Create and start the application

        app = BudgetTracker()        
        app.start()                        
        
    except KeyboardInterrupt:
        print("\n\n👋 Application terminated by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("🐞 Please report this issue if it persists.")

if __name__ == "__main__":
    main()