#!/usr/bin/env python3
"""
Script to load daily content from JSON file into the database.
"""

import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, DailyContent

def load_daily_content():
    """Load daily content from JSON file into database"""
    
    # Get the path to the JSON file
    json_file_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
        "daily_content.json"
    )
    
    # Check if JSON file exists
    if not os.path.exists(json_file_path):
        print(f"❌ JSON file not found at: {json_file_path}")
        return False
    
    try:
        # Read JSON file
        with open(json_file_path, 'r', encoding='utf-8') as file:
            content_data = json.load(file)
        
        print(f"✅ Loaded {len(content_data)} days of content from JSON file")
        
        # Create database session
        db = SessionLocal()
        
        try:
            # Check if content already exists
            existing_content = db.query(DailyContent).first()
            if existing_content:
                print("⚠️  Database already contains daily content. Skipping load.")
                return True
            
            # Insert content into database
            for day_data in content_data:
                content = DailyContent(**day_data)
                db.add(content)
            
            db.commit()
            print(f"✅ Successfully loaded {len(content_data)} days of content into database")
            return True
            
        except Exception as e:
            print(f"❌ Error loading content into database: {e}")
            db.rollback()
            return False
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Error reading JSON file: {e}")
        return False

def main():
    """Main function to load daily content"""
    print("🚀 Loading daily content from JSON file...")
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Load content
    success = load_daily_content()
    
    if success:
        print("✅ Daily content loading completed successfully!")
    else:
        print("❌ Failed to load daily content")

if __name__ == "__main__":
    main() 