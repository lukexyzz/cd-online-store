from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from config import Config

# Create SQLAlchemy engine & session factory
engine = create_engine(Config.DATABASE_URL, echo=False, future=True)
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base()


class CD(Base):
    """SQLAlchemy ORM model stub for a Compact Disc (CD) catalog item."""

    __tablename__ = "cds"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    artist = Column(String(150), nullable=False)
    genre = Column(String(80), nullable=True)
    price = Column(Float, nullable=False, default=9.99)
    stock = Column(Integer, nullable=False, default=10)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "genre": self.genre,
            "price": self.price,
            "stock": self.stock,
        }


def init_sql_db():
    """Initialize SQL database tables."""
    Base.metadata.create_all(bind=engine)

