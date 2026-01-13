from datetime import datetime, timezone
from uuid import uuid4

from core.credit_applications.events import CreditApplicationValidated


def test_event_has_id_and_timestamp():
    event = CreditApplicationValidated(
        id=str(uuid4()),
        occurred_at=datetime.now(timezone.utc),
        application_id="app-1",
    )

    assert event.id
    assert isinstance(event.id, str)
    assert event.occurred_at
    assert isinstance(event.occurred_at, datetime)
