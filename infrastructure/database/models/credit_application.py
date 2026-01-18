from sqlalchemy import (
    String,
    Numeric,
    DateTime,
    JSON,
)
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, UTC

from infrastructure.database.base import Base


class CreditApplicationModel(Base):
    __tablename__ = "credit_applications"

    id: Mapped[str] = mapped_column(String, primary_key=True)

    country: Mapped[str] = mapped_column(String(2), nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)

    full_name: Mapped[str] = mapped_column(String, nullable=False)
    document_type: Mapped[str] = mapped_column(String, nullable=False)
    document_value: Mapped[str] = mapped_column(String, nullable=False)

    requested_amount: Mapped[float] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )
    currency: Mapped[str] = mapped_column(String(3), nullable=False)

    monthly_income: Mapped[float] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    bank_snapshot: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )
