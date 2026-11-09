import os
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from dotenv import load_dotenv

# Load connection string from backend/.env
load_dotenv()

Base = declarative_base()



class User(Base):
  __tablename__ = "users"

  user_id = Column(Integer, primary_key=True)
  email = Column(String(255), unique=True, nullable=False)
  password_hash = Column(String(255), nullable=False)
  role = Column(String(20), default="customer")
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

  # Relationship to user orders
  orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")

  def to_dict(self):
    return {
        "user_id": self.user_id,
        "email": self.email,
        "role": self.role,
        "created_at": (
            self.created_at.isoformat() if self.created_at else None
        ),
    }


class CD(Base):
  __tablename__ = "cds"

  cd_id = Column(Integer, primary_key=True)
  title = Column(String(255), nullable=False)
  artist = Column(String(255), nullable=False)
  genre = Column(String(50))
  release_year = Column(Integer)
  price = Column(Float, nullable=False)
  stock_quantity = Column(Integer, default=0)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

  order_items = relationship("OrderItem", back_populates="cd")

  def to_dict(self):
    return {
        "cd_id": self.cd_id,
        "title": self.title,
        "artist": self.artist,
        "genre": self.genre,
        "release_year": self.release_year,
        "price": self.price,
        "stock_quantity": self.stock_quantity,
        "created_at": (
            self.created_at.isoformat() if self.created_at else None
        ),
    }


class Order(Base):
  __tablename__ = "orders"

  order_id = Column(Integer, primary_key=True)
  user_id = Column(
      Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
  )
  total_amount = Column(Float, nullable=False)
  status = Column(String(50), default="pending")
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

  user = relationship("User", back_populates="orders")
  items = relationship(
      "OrderItem", back_populates="order", cascade="all, delete-orphan"
  )

  def to_dict(self):
    return {
        "order_id": self.order_id,
        "user_id": self.user_id,
        "total_amount": self.total_amount,
        "status": self.status,
        "created_at": (
            self.created_at.isoformat() if self.created_at else None
        ),
        "items": [item.to_dict() for item in self.items],
    }

class OrderItem(Base):
  __tablename__ = "order_items"

  item_id = Column(Integer, primary_key=True)
  order_id = Column(
      Integer, ForeignKey("orders.order_id", ondelete="CASCADE"), nullable=False
  )
  cd_id = Column(
      Integer, ForeignKey("cds.cd_id", ondelete="RESTRICT"), nullable=False
  )
  quantity = Column(Integer, nullable=False)
  unit_price = Column(Float, nullable=False)

  order = relationship("Order", back_populates="items")
  cd = relationship("CD", back_populates="order_items")

  def to_dict(self):
    return {
        "item_id": self.item_id,
        "order_id": self.order_id,
        "cd_id": self.cd_id,
        "quantity": self.quantity,
        "unit_price": self.unit_price,
    }

def get_sql_engine(db_url=None):
  url = db_url or os.getenv("NEON_SQL_URL")
  if not url:
    raise ValueError(
        "NEON_SQL_URL is missing from environment variables (.env)."
    )
  return create_engine(url)


def get_sql_session(db_url=None):
  """Creates and returns a new SQLAlchemy session."""
  engine = get_sql_engine(db_url)
  Session = sessionmaker(bind=engine)
  return Session()


def init_db(db_url=None):
  """Creates all SQL tables in Neon PostgreSQL if they do not exist yet."""
  engine = get_sql_engine(db_url)
  Base.metadata.create_all(engine)
  print("SQL Database tables verified/created successfully!")