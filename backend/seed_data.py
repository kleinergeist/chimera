import os
import sys
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, DiagnosticSession, DiscoveredAccount, UserBucket, AccountAssignment

# Database configuration
DB_USER = os.getenv('POSTGRES_USER', 'chimera_user')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'chimera_password')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5433')
DB_NAME = os.getenv('POSTGRES_DB', 'chimera_db')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def seed_data_for_existing_users():
    """Generate sample data for existing users"""
    
    # Get all existing users
    users = session.query(User).all()
    
    if not users:
        print("No users found in database. Please sign up first.")
        return
    
    print(f"Found {len(users)} user(s). Generating sample data...\n")
    
    for user in users:
        print(f"Generating data for user: {user.email} (ID: {user.id})")
        
        # Create diagnostic sessions
        session1 = DiagnosticSession(
            user_id=user.id,
            status='completed',
            created_at=datetime.utcnow() - timedelta(days=10),
            completed_at=datetime.utcnow() - timedelta(days=9)
        )
        session.add(session1)
        
        session2 = DiagnosticSession(
            user_id=user.id,
            status='in_progress',
            created_at=datetime.utcnow() - timedelta(days=2)
        )
        session.add(session2)
        
        session3 = DiagnosticSession(
            user_id=user.id,
            status='completed',
            created_at=datetime.utcnow() - timedelta(days=30),
            completed_at=datetime.utcnow() - timedelta(days=29)
        )
        session.add(session3)
        
        session.commit()
        
        # Create discovered accounts for session1
        accounts_data = [
            {
                'account_name': 'john.doe',
                'email': 'john.doe@gmail.com',
                'platform': 'Gmail',
                'metadata': '{"account_type": "personal", "activity": "high"}'
            },
            {
                'account_name': 'johndoe123',
                'email': 'john@twitter.com',
                'platform': 'Twitter',
                'metadata': '{"followers": 1250, "verified": false}'
            },
            {
                'account_name': 'John Doe',
                'email': 'jdoe@company.com',
                'platform': 'LinkedIn',
                'metadata': '{"connections": 500, "industry": "Technology"}'
            },
            {
                'account_name': 'john_doe_photos',
                'email': 'john.d@instagram.com',
                'platform': 'Instagram',
                'metadata': '{"posts": 234, "followers": 890}'
            },
            {
                'account_name': 'JDoe',
                'email': 'john@github.com',
                'platform': 'GitHub',
                'metadata': '{"repos": 45, "stars": 120}'
            }
        ]
        
        accounts = []
        for acc_data in accounts_data:
            account = DiscoveredAccount(
                session_id=session1.id,
                account_name=acc_data['account_name'],
                email=acc_data['email'],
                platform=acc_data['platform'],
                account_metadata=acc_data['metadata'],
                created_at=datetime.utcnow() - timedelta(days=9)
            )
            session.add(account)
            accounts.append(account)
        
        session.commit()
        
        # Create user buckets
        bucket1 = UserBucket(
            user_id=user.id,
            bucket_name='Personal',
            description='Personal social media and email accounts',
            created_at=datetime.utcnow() - timedelta(days=8)
        )
        session.add(bucket1)
        
        bucket2 = UserBucket(
            user_id=user.id,
            bucket_name='Professional',
            description='Work-related and professional networking accounts',
            created_at=datetime.utcnow() - timedelta(days=8)
        )
        session.add(bucket2)
        
        bucket3 = UserBucket(
            user_id=user.id,
            bucket_name='Development',
            description='Coding and development platforms',
            created_at=datetime.utcnow() - timedelta(days=7)
        )
        session.add(bucket3)
        
        session.commit()
        
        # Create account assignments
        assignments = [
            (accounts[0], bucket1, 'Primary email account', 'Keep active', 'Personal'),
            (accounts[1], bucket1, 'Social media - entertainment', 'Review privacy settings', 'Personal'),
            (accounts[2], bucket2, 'Professional networking', 'Update profile regularly', 'Professional'),
            (accounts[3], bucket1, 'Photo sharing', 'Archive old posts', 'Personal'),
            (accounts[4], bucket3, 'Code repository', 'Update projects', 'Development')
        ]
        
        for account, bucket, notes, user_notes, category in assignments:
            assignment = AccountAssignment(
                account_id=account.id,
                bucket_id=bucket.id,
                notes=notes,
                user_notes=user_notes,
                suggested_category=category,
                created_at=datetime.utcnow() - timedelta(days=6)
            )
            session.add(assignment)
        
        session.commit()
        
        print(f"  ✓ Created 3 diagnostic sessions")
        print(f"  ✓ Created 5 discovered accounts")
        print(f"  ✓ Created 3 user buckets")
        print(f"  ✓ Created 5 account assignments\n")
    
    print("Sample data generation complete!")

if __name__ == "__main__":
    try:
        seed_data_for_existing_users()
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()

