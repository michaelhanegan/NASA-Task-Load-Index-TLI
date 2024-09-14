from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    assessments = relationship("Assessment", back_populates="user")

class Assessment(Base):
    __tablename__ = 'assessments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, nullable=False)
    mental_demand = Column(Float)
    physical_demand = Column(Float)
    temporal_demand = Column(Float)
    performance = Column(Float)
    effort = Column(Float)
    frustration = Column(Float)
    overall_score = Column(Float)
    user = relationship("User", back_populates="assessments")

engine = create_engine('sqlite:///nasa_tlx.db')
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
