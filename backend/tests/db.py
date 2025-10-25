import sys
from os.path import abspath, dirname

# Adding backend directory to sys.path for imports
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User

# Connect to the database
engine = create_engine('postgresql://chimera_user:chimera_password@localhost:5433/chimera_db')

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a Session
session = Session()

# Test adding a user
new_user = User(email='testuser@example.com', password_hash='securehashedpassword')
session.add(new_user)
session.commit()

# Query the user to verify
user = session.query(User).filter_by(email='testuser@example.com').first()
print(user.email, user.created_at)

# Close the session
session.close()