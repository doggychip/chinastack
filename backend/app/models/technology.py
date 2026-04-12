from sqlalchemy import Column, Text, text
from app.database import Base


class Technology(Base):
    __tablename__ = "technologies"

    id = Column(Text, primary_key=True, server_default=text("(lower(hex(randomblob(8))))"))
    name = Column(Text, nullable=False, unique=True)
    slug = Column(Text, nullable=False, unique=True)
    category = Column(Text, nullable=False)
    subcategory = Column(Text)
    website = Column(Text)
    description = Column(Text)
    icon_url = Column(Text)
    created_at = Column(Text, server_default=text("(datetime('now'))"))
