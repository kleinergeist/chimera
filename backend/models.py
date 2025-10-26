from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    clerk_id = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class DiagnosticSession(Base):
    __tablename__ = 'diagnostic_sessions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    user = relationship('User', back_populates='diagnostic_sessions')

class DiscoveredAccount(Base):
    __tablename__ = 'discovered_accounts'
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('diagnostic_sessions.id'))
    account_name = Column(String, nullable=False)
    email = Column(String)
    platform = Column(String, nullable=False)
    account_metadata = Column(Text)  # Renamed from metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    session = relationship('DiagnosticSession', back_populates='discovered_accounts')

class CompromisedCredential(Base):
    __tablename__ = 'compromised_credentials'
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('diagnostic_sessions.id'))
    account_name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    password = Column(String, nullable=True)
    source = Column(String, nullable=True)  # where it was found (tool/source/platform)
    metadata = Column(Text)  # raw JSON or extra info
    created_at = Column(DateTime, default=datetime.utcnow)
    session = relationship('DiagnosticSession', back_populates='compromised_credentials')

class UserBucket(Base):
    __tablename__ = 'user_buckets'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    bucket_name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship('User', back_populates='user_buckets')

class AccountAssignment(Base):
    __tablename__ = 'account_assignments'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('discovered_accounts.id'))
    bucket_id = Column(Integer, ForeignKey('user_buckets.id'))
    notes = Column(Text)
    user_notes = Column(Text)
    suggested_category = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    account = relationship('DiscoveredAccount', back_populates='account_assignments')
    bucket = relationship('UserBucket', back_populates='account_assignments')

User.diagnostic_sessions = relationship('DiagnosticSession', order_by=DiagnosticSession.id, back_populates='user')
DiagnosticSession.discovered_accounts = relationship('DiscoveredAccount', order_by=DiscoveredAccount.id, back_populates='session')
DiagnosticSession.compromised_credentials = relationship('CompromisedCredential', order_by='CompromisedCredential.id', back_populates='session')
User.user_buckets = relationship('UserBucket', order_by=UserBucket.id, back_populates='user')
DiscoveredAccount.account_assignments = relationship('AccountAssignment', order_by=AccountAssignment.id, back_populates='account')
UserBucket.account_assignments = relationship('AccountAssignment', order_by=AccountAssignment.id, back_populates='bucket')
