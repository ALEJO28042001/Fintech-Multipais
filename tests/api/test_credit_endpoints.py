import pytest
from fastapi.testclient import TestClient

from api.main import create_app
from core.credit_applications.enums import ApplicationStatus, Country


@pytest.fixture
def client():
    """
    Creates a fresh app instance per test session.
    Uses in-memory repositories (API-first stage).
    """
    app = create_app()
    return TestClient(app)


def _create_application(client, payload_override=None):
    payload = {
        "country": "SP",
        "full_name": "Juan Pérez",
        "document_value": "12345678Z",
        "document_type": "DNI",
        "requested_amount": 5000,
        "monthly_income": 2000,
        "currency": "EUR",
    }

    if payload_override:
        payload.update(payload_override)

    response = client.post(
        "/credit-applications/create-application",
        json=payload,
    )

    assert response.status_code == 201
    return response.json()["id"]


# ---------------------------------------------------------------------
# CREATE
# ---------------------------------------------------------------------

def test_create_credit_application(client):
    app_id = _create_application(client)
    assert isinstance(app_id, str)


# ---------------------------------------------------------------------
# GET BY ID
# ---------------------------------------------------------------------

def test_get_credit_application(client):
    app_id = _create_application(
        client,
        {
            "country": "PT",
            "full_name": "Ana Silva",
            "document_value": "123456789",
            "document_type": "NIF",
        },
    )

    response = client.get(f"/credit-applications/{app_id}")
    assert response.status_code == 200
    body = response.json()

    assert body["id"] == app_id
    assert body["country"] == "PT"
    assert "status" in body


# # ---------------------------------------------------------------------
# # LIST (FILTER BY COUNTRY)
# # ---------------------------------------------------------------------

def test_list_credit_applications_filtered_by_country(client):
    _create_application(
        client,
        {
            "country": "SP",
            "full_name": "Carlos Ruiz",
            "document_value": "87654321X",
            "requested_amount": 30000,
            "document_type": "DNI",
        },
    )

    _create_application(
        client,
        {
            "country": "PT",
            "full_name": "Maria Costa",
            "document_value": "987654322",
            "document_type": "NIF",
        },
    )

    response = client.get("/credit-applications?country=SP")

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) >= 1
    assert all(item["country"] == Country.SP for item in body)


def test_list_credit_applications_filtered_by_status(client):
    _create_application(
        client,
        {
            "country": "SP",
            "full_name": "Carlos Ruiz",
            "document_value": "87654321X",
            "requested_amount": 30000,
            "document_type": "DNI",
        },
    )

    _create_application(
        client,
        {
            "country": "PT",
            "full_name": "Maria Costa",
            "document_value": "987654322",
            "document_type": "NIF",
        },
    )

    response = client.get("/credit-applications?status=VALIDATED")

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) >= 1
    assert all(item["status"] == "VALIDATED" for item in body)
    
# # # ---------------------------------------------------------------------
# # # APPROVE
# # # ---------------------------------------------------------------------

def test_approve_credit_application(client):
    app_id = _create_application(
        client,
        {
            "full_name": "Laura Gómez",
            "document_value": "11223344A",
            "document_type": "DNI",
        },
    )

    # Attach bank snapshot (required before approval)
    snapshot_response = client.post(
        f"/credit-applications/{app_id}/bank-snapshot"
    )
    assert snapshot_response.status_code == 200

    response = client.get(f"/credit-applications/{app_id}")
    # # Approve
    response = client.post(f"/credit-applications/{app_id}/approve")

    assert response.status_code == 200
    assert response.json()["status"] == "approved"

    # Verify state
    get_response = client.get(f"/credit-applications/{app_id}")
    assert get_response.json()["status"] == ApplicationStatus.APPROVED



# # # ---------------------------------------------------------------------
# # # REJECT
# # # ---------------------------------------------------------------------

def test_reject_credit_application(client):
    app_id = _create_application(
        client,
        {
            "country": "PT",
            "full_name": "Rui Fernandes",
            "document_value": "987654322",
            "document_type": "NIF",
            "requested_amount": 1000,  # force rejection by PT policy
            "monthly_income": 1000,
        },
    )

    response = client.post(f"/credit-applications/{app_id}/reject")
    assert response.status_code == 200
    assert response.json()["status"] == "rejected"

    # # Verify state
    get_response = client.get(f"/credit-applications/{app_id}")
    assert get_response.json()["status"] == ApplicationStatus.REJECTED
    print(get_response.json())

