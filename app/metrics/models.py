from uuid import uuid4
from sqlalchemy import Column, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

# Entity class for metric_sample table
class MetricSample(Base):
    __tablename__ = "metric_samples"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    hardware_id = Column(
        UUID(as_uuid=True),
        ForeignKey("machines.hardware_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    recorded_at = Column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        server_default=func.now(),
    )

    gpu_util = Column(Float, nullable=True)
    cpu_util = Column(Float, nullable=True)
    mem_used_gb = Column(Float, nullable=True)
    net_rx_mb = Column(Float, nullable=True)
    net_tx_mb = Column(Float, nullable=True)

    machine = relationship("Machine", back_populates="metric_samples")
