#!/usr/bin/env python3
"""
Script to populate the database with sample data for the 33-day consecration.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, DailyContent
from app.utils.security import get_password_hash
from app.models.user import User

def create_sample_users(db: Session):
    """Create sample users"""
    users_data = [
        {
            "name": "Juan Pérez",
            "email": "juan@example.com",
            "password_hash": get_password_hash("password123"),
            "current_day": 5
        },
        {
            "name": "María García",
            "email": "maria@example.com", 
            "password_hash": get_password_hash("password123"),
            "current_day": 12
        },
        {
            "name": "Carlos López",
            "email": "carlos@example.com",
            "password_hash": get_password_hash("password123"),
            "current_day": 1
        }
    ]
    
    for user_data in users_data:
        user = User(**user_data)
        db.add(user)
    
    db.commit()
    print("✅ Sample users created")

def create_daily_content(db: Session):
    """Create sample daily content for the 33-day consecration"""
    
    daily_content = [
        {
            "day": 1,
            "title": "Día 1: Introducción a la Consagración",
            "description": "Hoy comenzamos nuestra jornada de 33 días hacia la consagración total a María. Este primer día nos introduce en el significado profundo de la consagración y nos prepara para este camino espiritual.",
            "video_url": "https://www.youtube.com/watch?v=example1",
            "rosary_video_url": "https://www.youtube.com/watch?v=rosary1",
            "meditation_pdf_url": "/pdfs/meditation_day_1.pdf",
            "mysteries": "Gozosos",
            "quote": "La devoción a María es el camino más seguro y fácil para llegar a Jesús."
        },
        {
            "day": 2,
            "title": "Día 2: La Humildad de María",
            "description": "Reflexionamos sobre la humildad de María, virtud fundamental que debemos imitar en nuestro camino hacia la consagración total.",
            "video_url": "https://www.youtube.com/watch?v=example2",
            "rosary_video_url": "https://www.youtube.com/watch?v=rosary2",
            "meditation_pdf_url": "/pdfs/meditation_day_2.pdf",
            "mysteries": "Gozosos",
            "quote": "María es la obra maestra de la humildad. En ella vemos la perfección de esta virtud."
        },
        {
            "day": 3,
            "title": "Día 3: La Fe de María",
            "description": "Contemplamos la fe inquebrantable de María, que nos enseña a confiar completamente en Dios en todos los momentos de nuestra vida.",
            "video_url": "https://www.youtube.com/watch?v=example3",
            "rosary_video_url": "https://www.youtube.com/watch?v=rosary3",
            "meditation_pdf_url": "/pdfs/meditation_day_3.pdf",
            "mysteries": "Gozosos",
            "quote": "Bienaventurada eres, María, porque has creído."
        },
        {
            "day": 4,
            "title": "Día 4: La Esperanza en María",
            "description": "Aprendemos a poner nuestra esperanza en María, que es la puerta del cielo y nuestro refugio seguro.",
            "video_url": "https://www.youtube.com/watch?v=example4",
            "rosary_video_url": "https://www.youtube.com/watch?v=rosary4",
            "meditation_pdf_url": "/pdfs/meditation_day_4.pdf",
            "mysteries": "Gozosos",
            "quote": "María es la puerta del cielo, el camino más seguro para llegar a Dios."
        },
        {
            "day": 5,
            "title": "Día 5: El Amor a María",
            "description": "Cultivamos el amor filial hacia María, reconociendo en ella a nuestra Madre celestial que nos ama con amor maternal.",
            "video_url": "https://www.youtube.com/watch?v=example5",
            "rosary_video_url": "https://www.youtube.com/watch?v=rosary5",
            "meditation_pdf_url": "/pdfs/meditation_day_5.pdf",
            "mysteries": "Gozosos",
            "quote": "Ama a María y ella te amará. Ama a María y tendrás a Jesús."
        }
    ]
    
    # Add more days (6-33) with similar structure
    for day in range(6, 34):
        daily_content.append({
            "day": day,
            "title": f"Día {day}: Continuando la Jornada",
            "description": f"En este día {day} de nuestra jornada de consagración, continuamos profundizando en nuestra relación con María y preparándonos para la consagración total.",
            "video_url": f"https://www.youtube.com/watch?v=example{day}",
            "rosary_video_url": f"https://www.youtube.com/watch?v=rosary{day}",
            "meditation_pdf_url": f"/pdfs/meditation_day_{day}.pdf",
            "mysteries": "Gozosos" if day % 5 == 1 else "Dolorosos" if day % 5 == 2 else "Gloriosos" if day % 5 == 3 else "Luminosos" if day % 5 == 4 else "Gozosos",
            "quote": f"La consagración total a María es el secreto de la santidad. Día {day} de nuestra jornada espiritual."
        })
    
    for content_data in daily_content:
        content = DailyContent(**content_data)
        db.add(content)
    
    db.commit()
    print(f"✅ Created {len(daily_content)} days of content")

def main():
    """Main function to populate the database"""
    print("🚀 Starting database population...")
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Get database session
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_content = db.query(DailyContent).first()
        if existing_content:
            print("⚠️  Database already contains data. Skipping population.")
            return
        
        # Create sample data
        create_sample_users(db)
        create_daily_content(db)
        
        print("✅ Database population completed successfully!")
        
    except Exception as e:
        print(f"❌ Error populating database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main() 