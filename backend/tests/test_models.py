import sys
from os.path import abspath, dirname
from datetime import datetime

# Adding backend directory to sys.path for imports
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, DiagnosticSession, DiscoveredAccount, UserBucket, AccountAssignment

# Connect to the database
engine = create_engine('postgresql://chimera_user:chimera_password@localhost:5433/chimera_db')

# Create all tables
Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

def test_user_model():
    """Test User model creation and retrieval"""
    session = Session()
    
    try:
        # Create a new user with Clerk ID
        new_user = User(
            clerk_id='clerk_test_user_123456',
            email='testuser@example.com'
        )
        session.add(new_user)
        session.commit()
        
        # Query the user
        user = session.query(User).filter_by(email='testuser@example.com').first()
        assert user is not None
        assert user.email == 'testuser@example.com'
        assert user.clerk_id == 'clerk_test_user_123456'
        assert user.created_at is not None
        
        print(f"✓ User created successfully: {user.email}, ID: {user.id}, Clerk ID: {user.clerk_id}")
        return user
    except Exception as e:
        session.rollback()
        print(f"✗ User test failed: {e}")
        raise
    finally:
        session.close()

def test_diagnostic_session_model(user_id):
    """Test DiagnosticSession model creation and retrieval"""
    session = Session()
    
    try:
        # Create a diagnostic session
        new_session = DiagnosticSession(
            user_id=user_id,
            status='in_progress',
            created_at=datetime.utcnow()
        )
        session.add(new_session)
        session.commit()
        
        # Query the session
        diag_session = session.query(DiagnosticSession).filter_by(user_id=user_id).first()
        assert diag_session is not None
        assert diag_session.status == 'in_progress'
        assert diag_session.user_id == user_id
        
        print(f"✓ DiagnosticSession created successfully: ID {diag_session.id}, Status: {diag_session.status}")
        return diag_session
    except Exception as e:
        session.rollback()
        print(f"✗ DiagnosticSession test failed: {e}")
        raise
    finally:
        session.close()

def test_discovered_account_model(session_id):
    """Test DiscoveredAccount model creation and retrieval"""
    session = Session()
    
    try:
        # Create a discovered account
        new_account = DiscoveredAccount(
            session_id=session_id,
            account_name='john_doe',
            email='john@example.com',
            platform='Twitter',
            account_metadata='{"followers": 1000, "verified": false}'
        )
        session.add(new_account)
        session.commit()
        
        # Query the account
        account = session.query(DiscoveredAccount).filter_by(session_id=session_id).first()
        assert account is not None
        assert account.account_name == 'john_doe'
        assert account.platform == 'Twitter'
        assert account.email == 'john@example.com'
        
        print(f"✓ DiscoveredAccount created successfully: {account.account_name} on {account.platform}")
        return account
    except Exception as e:
        session.rollback()
        print(f"✗ DiscoveredAccount test failed: {e}")
        raise
    finally:
        session.close()

def test_user_bucket_model(user_id):
    """Test UserBucket model creation and retrieval"""
    session = Session()
    
    try:
        # Create a user bucket
        new_bucket = UserBucket(
            user_id=user_id,
            bucket_name='Social Media',
            description='All social media accounts'
        )
        session.add(new_bucket)
        session.commit()
        
        # Query the bucket
        bucket = session.query(UserBucket).filter_by(user_id=user_id).first()
        assert bucket is not None
        assert bucket.bucket_name == 'Social Media'
        assert bucket.description == 'All social media accounts'
        
        print(f"✓ UserBucket created successfully: {bucket.bucket_name}")
        return bucket
    except Exception as e:
        session.rollback()
        print(f"✗ UserBucket test failed: {e}")
        raise
    finally:
        session.close()

def test_account_assignment_model(account_id, bucket_id):
    """Test AccountAssignment model creation and retrieval"""
    session = Session()
    
    try:
        # Create an account assignment
        new_assignment = AccountAssignment(
            account_id=account_id,
            bucket_id=bucket_id,
            notes='Auto-categorized',
            user_notes='Keep this account active',
            suggested_category='Personal'
        )
        session.add(new_assignment)
        session.commit()
        
        # Query the assignment
        assignment = session.query(AccountAssignment).filter_by(account_id=account_id).first()
        assert assignment is not None
        assert assignment.suggested_category == 'Personal'
        assert assignment.notes == 'Auto-categorized'
        
        print(f"✓ AccountAssignment created successfully: Account {assignment.account_id} -> Bucket {assignment.bucket_id}")
        return assignment
    except Exception as e:
        session.rollback()
        print(f"✗ AccountAssignment test failed: {e}")
        raise
    finally:
        session.close()

def test_relationships():
    """Test relationships between models"""
    session = Session()
    
    try:
        # Query user with relationships
        user = session.query(User).filter_by(email='testuser@example.com').first()
        
        # Test User -> DiagnosticSession relationship
        assert len(user.diagnostic_sessions) > 0
        print(f"✓ User has {len(user.diagnostic_sessions)} diagnostic session(s)")
        
        # Test User -> UserBucket relationship
        assert len(user.user_buckets) > 0
        print(f"✓ User has {len(user.user_buckets)} bucket(s)")
        
        # Test DiagnosticSession -> DiscoveredAccount relationship
        diag_session = user.diagnostic_sessions[0]
        assert len(diag_session.discovered_accounts) > 0
        print(f"✓ DiagnosticSession has {len(diag_session.discovered_accounts)} discovered account(s)")
        
        # Test DiscoveredAccount -> AccountAssignment relationship
        account = diag_session.discovered_accounts[0]
        assert len(account.account_assignments) > 0
        print(f"✓ DiscoveredAccount has {len(account.account_assignments)} assignment(s)")
        
        # Test UserBucket -> AccountAssignment relationship
        bucket = user.user_buckets[0]
        assert len(bucket.account_assignments) > 0
        print(f"✓ UserBucket has {len(bucket.account_assignments)} assignment(s)")
        
        print("✓ All relationships working correctly!")
    except Exception as e:
        print(f"✗ Relationship test failed: {e}")
        raise
    finally:
        session.close()

def cleanup_test_data():
    """Clean up test data"""
    session = Session()
    
    try:
        # Delete in reverse order of foreign key dependencies
        session.query(AccountAssignment).delete()
        session.query(DiscoveredAccount).delete()
        session.query(UserBucket).delete()
        session.query(DiagnosticSession).delete()
        session.query(User).filter_by(email='testuser@example.com').delete()
        session.commit()
        print("✓ Test data cleaned up successfully")
    except Exception as e:
        session.rollback()
        print(f"✗ Cleanup failed: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Running Model Tests")
    print("=" * 60)
    
    try:
        # Run tests
        user = test_user_model()
        diag_session = test_diagnostic_session_model(user.id)
        account = test_discovered_account_model(diag_session.id)
        bucket = test_user_bucket_model(user.id)
        assignment = test_account_assignment_model(account.id, bucket.id)
        
        # Test relationships
        test_relationships()
        
        print("\n" + "=" * 60)
        print("All Tests Passed! ✓")
        print("=" * 60)
        
        # Cleanup
        cleanup_test_data()
        
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"Tests Failed: {e}")
        print("=" * 60)
        cleanup_test_data()

