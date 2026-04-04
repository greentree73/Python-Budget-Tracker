#!/usr/bin/env python3
"""
Report Service
Generates financial reports and analytics

TODO: Complete the report generation methods
"""

from datetime import date, datetime, timedelta
from decimal import Decimal
from models.transaction import Transaction
from models.category import Category
from services.transaction_service import TransactionService
from utils.formatters import format_currency, format_date
from collections import defaultdict


class ReportService:
    """
    Service class for generating financial reports
    """
    
    @staticmethod
    def generate_balance_report():
        """
        Generate a balance report showing current financial status
        
        Returns:
            str: Formatted balance report
        """
        print("📊 Generating Balance Report...")
        
        # TODO: Get transaction summary
        summary = TransactionService.get_transaction_summary()
        
        report = []
        report.append("\n" + "=" * 50)
        report.append("💰 PERSONAL BUDGET BALANCE REPORT")
        report.append("=" * 50)
        
        # TODO: Add balance information to report
        # Format currency amounts nicely
        # Show income, expenses, and net balance

        report.append(f"Total Income: {format_currency(summary.get('total_income', 0))}")
        report.append(f"Total Expenses: {format_currency(summary.get('total_expenses', 0))}")
        report.append(f"Net Balance: {format_currency(summary.get('net_balance', 0))}")
        report.append(f"Total Transactions: {summary.get('transaction_count', 0)}")
        
        report.append("\nGenerated: " + format_date(date.today()))
        report.append("=" * 50)
        
        return "\n".join(report)
    
    @staticmethod
    def generate_category_report(transaction_type='expense', top_n=10):
        """
        Generate a report showing spending/income by category
        
        Args:
            transaction_type (str): 'income' or 'expense'
            top_n (int): Number of top categories to show
            
        Returns:
            str: Formatted category report
        """
        print(f"🏷️  Generating {transaction_type.title()} by Category Report...")
        
        report = []
        report.append("\n" + "=" * 50)
        report.append(f"📋 {transaction_type.upper()} BY CATEGORY REPORT")
        report.append("=" * 50)
        
        # TODO: Get category spending data
        category_data = TransactionService.get_spending_by_category(transaction_type)
        
        # TODO: Sort categories by amount (highest first)
        # Show top N categories with percentages
        
        if not category_data:
            report.append("No data available.")
        else:
            # Sort categories by amount (descending)
            sorted_categories = sorted(category_data.items(), key=lambda x: x[1], reverse=True)
            total = sum(category_data.values())
            
            report.append(f"{'Category':<20}{'Amount':<15}{'Percentage'}")
            report.append("-" * 50)

            for category, amount in sorted_categories[:top_n]:
                percentage = (amount / total * 100) if total > 0 else 0
                report.append(f"{category:<20}{format_currency(amount):<15}{percentage:.2f}%")

        report.append("\nGenerated: " + format_date(date.today()))
        report.append("=" * 50)
        
        return "\n".join(report)
    
    @staticmethod
    def generate_monthly_report(year=None, month=None):
        """
        Generate a monthly financial report
        
        Args:
            year (int, optional): Year (default: current)
            month (int, optional): Month (default: current)
            
        Returns:
            str: Formatted monthly report
        """
        if not year:
            year = date.today().year
        if not month:
            month = date.today().month
            
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        
        print(f"📅 Generating {month_names[month-1]} {year} Report...")
        
        report = []
        report.append("\n" + "=" * 50)
        report.append(f"📅 MONTHLY REPORT - {month_names[month-1].upper()} {year}")
        report.append("=" * 50)
        
        # TODO: Get monthly data
        monthly_data = TransactionService.get_monthly_summary(year, month)
        
        # TODO: Add monthly statistics
        # - Total income for month
        # - Total expenses for month
        # - Net change
        # - Number of transactions
        # - Average transaction size
        # - Top spending categories

        report.append(f"Total Income: {format_currency(monthly_data.get('total_income', 0))}")
        report.append(f"Total Expenses: {format_currency(monthly_data.get('total_expenses', 0))}")
        report.append(f"Net Balance: {format_currency(monthly_data.get('net_balance', 0))}")
        report.append(f"Transaction Count: {monthly_data.get('transaction_count', 0)}")

        # average transaction
        if monthly_data.get('transaction_count', 0) > 0:
            avg = (monthly_data['total_income'] + monthly_data['total_expenses']) / monthly_data['transaction_count']
            report.append(f"Average Transaction: {format_currency(avg)}")

        # Get all expense categories
        expense_categories = TransactionService.get_spending_by_category('expense')

        # Sort and get top categories
        if expense_categories:
            sorted_categories = sorted(expense_categories.items(), key=lambda x: x[1], reverse=True)

            report.append("\n🏷️ TOP SPENDING CATEGORIES")
            report.append("-" * 30)

            total_expenses = monthly_data.get('total_expenses', 0)

            for category, amount in sorted_categories[:5]:
                percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
                report.append(f"{category}: {format_currency(amount)} ({percentage:.2f}%)")

        report.append("\nGenerated: " + format_date(date.today()))
        report.append("=" * 50)
        
        return "\n".join(report)
    
    @staticmethod
    def generate_trend_report(days=30):
        """
        Generate a trend report for recent activity
        
        Args:
            days (int): Number of days to analyze
            
        Returns:
            str: Formatted trend report
        """
        print(f"📈 Generating {days}-Day Trend Report...")
        
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        mid_date = start_date + timedelta(days=days // 2)        
        
        report = []
        report.append("\n" + "=" * 50)
        report.append(f"📈 FINANCIAL TREND REPORT ({days} DAYS)")
        report.append("=" * 50)
        report.append(f"Period: {format_date(start_date)} to {format_date(end_date)}")
        report.append("")
        
        # TODO: Get transactions for date range
        transactions = Transaction.get_by_date_range(start_date, end_date)
        
        # TODO: Calculate trends
        # - Daily average spending
        # - Most active spending days
        # - Trend direction (spending increasing/decreasing)

        if not transactions:
            report.append("No transactions found.")
        else:
            total_spending = sum(t.amount for t in transactions if t.type == 'expense')
            total_income = sum(t.amount for t in transactions if t.type == 'income')

            daily_spending = defaultdict(float)
            daily_avg_spending = total_spending / days if days else 0

            report.append(f"Total Income: {format_currency(total_income)}")
            report.append(f"Total Expenses: {format_currency(total_spending)}")
            report.append(f"Daily Avg Spending: {format_currency(daily_avg_spending)}")

            for t in transactions:
                if t.type == 'expense':
                    daily_spending[t.transaction_date] += t.amount

            most_active_days = []
            max_spent = 0
            
            if daily_spending:
                max_spent = max(daily_spending.values())
                most_active_days = [d for d, amt in daily_spending.items() if amt == max_spent]

            report.append("\nMost Active Spending Day(s):")
            for d in most_active_days:
                report.append(f"- {format_date(d)} ({format_currency(max_spent)})")

            first_half = sum(t.amount for t in transactions
                if t.type == 'expense' and t.transaction_date < mid_date)

            second_half = sum(t.amount for t in transactions
                if t.type == 'expense' and t.transaction_date >= mid_date)

            if second_half > first_half:
                trend = "📈 Increasing"
            elif second_half < first_half:
                trend = "📉 Decreasing"
            else:
                trend = "➡️ Stable"

            report.append(f"\nTrend Direction: {trend}")

            report.append("\nGenerated: " + format_date(date.today()))
            report.append("=" * 50)
        
            return "\n".join(report)
    
    @staticmethod
    def generate_summary_dashboard():
        """
        Generate a comprehensive dashboard with key metrics
        
        Returns:
            str: Formatted dashboard
        """
        print("📊 Generating Financial Dashboard...")
        
        dashboard = []
        dashboard.append("\n" + "=" * 60)
        dashboard.append("📊 PERSONAL BUDGET TRACKER DASHBOARD")
        dashboard.append("=" * 60)
        
        # TODO: Get comprehensive data
        summary = TransactionService.get_transaction_summary()
        expense_categories = TransactionService.get_spending_by_category('expense')
        income_categories = TransactionService.get_spending_by_category('income')
        
        # TODO: Create dashboard sections:
        # 1. Current Balance Overview
        # 2. Recent Activity (last 7 days)
        # 3. Top Spending Categories
        # 4. Budget Health Indicators

        # Balance Overview
        dashboard.append("\n💰 BALANCE OVERVIEW")
        dashboard.append("-" * 30)
        dashboard.append(f"Income: {format_currency(summary.get('total_income', 0))}")
        dashboard.append(f"Expenses: {format_currency(summary.get('total_expenses', 0))}")
        dashboard.append(f"Net: {format_currency(summary.get('net_balance', 0))}")

        #Recent Activity (Last 7 days)
        dashboard.append("\n📅 RECENT ACTIVITY (Last 7 Days)")
        dashboard.append("-" * 30)
        end_date = date.today()
        start_date = end_date - timedelta(days=7)
        recent_transactions = Transaction.get_by_date_range(start_date, end_date)

        if recent_transactions:
            for t in recent_transactions[:5]:
                dashboard.append(
                    f"{format_date(t.transaction_date)} | {t.category_id} | {format_currency(t.amount)}"
            )
        else:
            dashboard.append("No recent transactions.")

        # Top Categories
        dashboard.append("\n🏷️ TOP SPENDING CATEGORIES")
        dashboard.append("-" * 30)

        if expense_categories:
            sorted_categories = sorted(expense_categories.items(), key=lambda x: x[1], reverse=True)
            for category, amount in sorted_categories[:5]:
                dashboard.append(f"{category}: {format_currency(amount)}")

        dashboard.append("\n📝 QUICK ACTIONS:")
        dashboard.append("   1. Add New Transaction")
        dashboard.append("   2. View Recent Transactions")
        dashboard.append("   3. Generate Detailed Reports")
        dashboard.append("   4. Manage Categories")
        
        dashboard.append("\nGenerated: " + format_date(date.today()))
        dashboard.append("=" * 60)
        
        return "\n".join(dashboard)
    
    @staticmethod
    def generate_budget_health_score():
        """
        Calculate and return a budget health score (0-100)
        
        Returns:
            dict: Health score and breakdown
        """
        # TODO: Implement budget health calculation
        # Consider factors like:
        # - Income vs expenses ratio
        # - Savings rate (if income > expenses)
        # - Spending consistency
        # - Emergency fund equivalent
        
        summary = TransactionService.get_transaction_summary()
        income = summary['total_income']
        expenses = summary['total_expenses']

        health_data = {
            'score': 0,  # 0-100
            'grade': 'F',  # A, B, C, D, F
            'factors': {
                'income_stability': 0,
                'expense_control': 0,
                'savings_rate': 0,
                'budget_balance': 0
            },
            'recommendations': []
        }
        
        # TODO: Calculate actual score based on financial data
       
        if income == 0:
            return health_data

        savings_rate = (income - expenses) / income

        # Scoring
        score = 0

        # Expense control
        if expenses <= income:
            score += 40

        # Savings rate
        if savings_rate > 0.2:
            score += 30
        elif savings_rate > 0:
            score += 15

        # Stability (simple proxy)
        score += 30

        health_data['score'] = min(score, 100)

        # Grade
        if score >= 85:
            health_data['grade'] = 'A'
        elif score >= 70:
            health_data['grade'] = 'B'
        elif score >= 50:
            health_data['grade'] = 'C'
        elif score >= 30:
            health_data['grade'] = 'D'
        else:
            health_data['grade'] = 'F'

        health_data['factors'] = {
            'income': income,
            'expenses': expenses,
            'savings_rate': savings_rate
        }

        if savings_rate < 0:
            health_data['recommendations'].append("Reduce expenses immediately")
        if savings_rate < 0.2:
            health_data['recommendations'].append("Increase savings rate")
        
        return health_data
    
    @staticmethod
    def export_report_to_file(report_content, filename):
        """
        Export report content to a text file
        
        Args:
            report_content (str): Report content
            filename (str): Output filename
            
        Returns:
            bool: True if successful
        """
        # TODO: Write report to file
        # Use context managers for file operations
        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(report_content)
            print(f"✅ Report exported to {filename}")
            return True
                        
        except Exception as e:
            print(f"❌ Error exporting report: {e}")
            return False

def main():
    """
    Test the ReportService
    """
    print("📈 Testing Report Service")
    print("=" * 30)
    
    # Test dashboard generation
    dashboard = ReportService.generate_summary_dashboard()
    print(dashboard)
    
    # Test balance report
    balance_report = ReportService.generate_balance_report()
    print(balance_report)
    
    print("\n💡 Complete the TODO sections to see full reports!")

if __name__ == "__main__":
    main()