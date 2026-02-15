import pytest

from api.billing import process_stripe_event


@pytest.mark.asyncio
async def test_process_stripe_event_is_idempotent_by_event_id():
    event = {
        "id": "evt_test_idempotency_1",
        "type": "noop.event",
        "data": {"object": {}},
    }

    first = await process_stripe_event(event)
    second = await process_stripe_event(event)

    assert first is True
    assert second is False
