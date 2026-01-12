from datetime import datetime,timezone
from core.credit_applications.events import CreditApplicationValidated, CoreEvent

def test_event_has_id_and_timestamp():
    event = CreditApplicationValidated(
        id=CoreEvent.new_event_id(),
        occurred_at=datetime.now(timezone.utc),
        application_id="app-1",
    )

    assert event.id is not None
    assert event.occurred_at is not None
