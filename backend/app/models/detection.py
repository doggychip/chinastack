from sqlalchemy import Column, Text, Float, ForeignKey, UniqueConstraint, text
from app.database import Base


class SiteDetection(Base):
    __tablename__ = "site_detections"

    id = Column(Text, primary_key=True, server_default=text("(lower(hex(randomblob(8))))"))
    site_id = Column(Text, ForeignKey("sites.id"), nullable=False)
    tech_id = Column(Text, ForeignKey("technologies.id"), nullable=False)
    version = Column(Text)
    confidence = Column(Float, default=1.0)
    evidence = Column(Text)
    first_detected_at = Column(Text, server_default=text("(datetime('now'))"))
    last_detected_at = Column(Text, server_default=text("(datetime('now'))"))

    __table_args__ = (UniqueConstraint("site_id", "tech_id"),)
