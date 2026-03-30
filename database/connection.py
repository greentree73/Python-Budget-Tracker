#!/usr/bin/env python3
"""
Database Connection Module
Handles PostgreSQL database connections and basic operations

TODO: Complete the database connection and query functions
"""

import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseConnection:
    """
    Manages database connections and provides query methods
    """
    
    def __init__(self):
        """
        Initialize database connection parameters from environment variables
        """
        # TODO: Set up database connection parameters
        # Hint: Use os.getenv() to get environment variables
        # You'll need: DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT
        
        self.host = os.getenv("DB_HOST", "localhost")  # TODO: Get from environment
        self.database = os.getenv("DB_NAME", "budget_tracker")  # TODO: Get from environment  
        self.user = os.getenv("DB_USER", "postgres")  # TODO: Get from environment
        self.password = os.getenv("DB_PASSWORD", "root")  # TODO: Get from environment
        self.port = os.getenv("DB_PORT", 5432)  # TODO: Get from environment (default: 5432)
        
        self.connection = None
    
    def connect(self):
        """
        Establish connection to the PostgreSQL database
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # TODO: Create database connection using psycopg.connect()
            # Use the connection parameters from __init__
            # Set cursor_factory=RealDictCursor for dictionary-like results
            self.connection = psycopg.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port,
                row_factory=dict_row
            )
            print("�� Database connection established successfully")
            return True
        except Exception as e:
            print(f"�� Database connection failed: {e}")
            return False
         
    def disconnect(self):
        """
        Close the database connection
        """
        # TODO: Close the connection if it exists
        # Check if self.connection exists and close it
        if self.connection:
            self.connection.close()
            print("�� Database connection closed successfully")
    
    def execute_query(self, query, params=None):
        """
        Execute a SQL query and return results
        
        Args:
            query (str): SQL query to execute
            params (tuple, optional): Query parameters
            
        Returns:
            list: Query results as list of dictionaries
        """
        try:
            # TODO: Execute query using cursor
            # 1. Create cursor from self.connection
            # 2. Execute query with optional parameters
            # 3. Fetch and return results
            # 4. Close cursor
         
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
            
                # If SELECT query → fetch results
                if cursor.description:
                    return cursor.fetchall()
                            
        except Exception as e:
            print(f"❌ Query execution failed: {e}")
            return []
    
    def execute_update(self, query, params=None):
        """
        Execute an INSERT, UPDATE, or DELETE query
        
        Args:
            query (str): SQL query to execute
            params (tuple, optional): Query parameters
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # TODO: Execute update query
            # 1. Create cursor
            # 2. Execute query with parameters  
            # 3. Commit the transaction
            # 4. Close cursor
            # 5. Return True if successful
             
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                return True
            
        except Exception as e:
            print(f"❌ Update query failed: {e}")
            # TODO: Rollback the transaction on error
            self.connection.rollback()
            return False
    
    def test_connection(self):
        """
        Test database connection and print status
        """
        print("🔍 Testing database connection...")
        
        if self.connect():
            # Test with a simple query
            result = self.execute_query("SELECT version()")
            if result:
                print(f"✅ Database connection successful!")
                print(f"📊 PostgreSQL version: {result[0]['version'][:50]}...")
                
                # Test if our tables exist
                tables_query = """
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
                """
                tables = self.execute_query(tables_query)
                if tables:
                    print(f"📋 Found {len(tables)} tables: {', '.join([t['table_name'] for t in tables])}")
                else:
                    print("⚠️  No tables found. Run schema.sql to create tables.")
                
                self.disconnect()
                return True
            else:
                print("❌ Connection established but query failed")
                self.disconnect()
                return False
        else:
            print("❌ Could not connect to database")
            print("💡 Make sure PostgreSQL is running and .env file is configured")
            return False

def main():
    """
    Test the database connection
    """
    print("🗄️  Budget Tracker Database Connection Test")
    print("=" * 50)
    
    db = DatabaseConnection()
    db.test_connection()
    
    print("\n💡 Next steps:")
    print("   1. If connection failed, check your .env file and PostgreSQL setup")
    print("   2. Run schema.sql to create database tables")
    print("   3. Run seed_data.sql to add sample data")
    print("   4. Start building your budget tracker application!")

if __name__ == "__main__":
    main()