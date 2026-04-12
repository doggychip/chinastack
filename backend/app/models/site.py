from sqlalchemy import Column, Text, Integer, text
from app.database import Base


class Site(Base):
    __tablename__ = "sites"

    id = Column(Text, primary_key=True, server_default=text("(lower(hex(randomblob(8))))"))
    domain = Column(Text, nullable=False, unique=True)
    url = Column(Text, nullable=False)
    title = Column(Text)
    meta_description = Column(Text)
    icp_number = Column(Text)
    icp_entity = Column(Text)
    server_header = Column(Text)
    status_code = Column(Integer)
    response_time_ms = Column(Integer)
    last_scanned_at = Column(Text)
    scan_count = Column(Integer, default=1)
    html_size_bytes = Column(Integer)
    tech_count = Column(Integer, default=0)
    created_at = Column(Text, server_default=text("(datetime('now'))"))
    updated_at = Column(Text, server_default=text("(datetime('now'))"))
