from fastapi import APIRouter, Depends, status

from api.schemas.requests import (
    CreateCreditApplicationRequest,
)
from applications.credit_applications import (
    CreateCreditApplication,
    AttachBankSnapshot,
    ApproveCreditApplication,
    RejectCreditApplication,
    GetCreditApplication,
    ListCreditApplications,
)
from api.dependencies import (
    get_create_credit_application,
    get_attach_bank_snapshot,
    get_approve_credit_application,
    get_reject_credit_application,
    get_credit_application,
    get_list_credit_applications,
)

# ✅ Router definition (this was missing)
router = APIRouter()


from uuid import uuid4
from core.credit_applications import CreditApplication, Applicant, Document,DocumentType,Country
from core.credit_applications.value_objects import Money, Income

@router.post("/create-application", status_code=status.HTTP_201_CREATED)
def create_credit_application(
    request: CreateCreditApplicationRequest,
    use_case: CreateCreditApplication = Depends(get_create_credit_application),
):
    application = CreditApplication(
        id=str(uuid4()),
        country=Country(request.country),
        applicant=Applicant(
            full_name=request.full_name,
            document = Document(                
                document_type=request.document_type,
                value=request.document_value,
                country=Country(request.country),
            )
        ),
        requested_amount=Money(request.requested_amount,request.currency),
        monthly_income=Income(request.monthly_income,request.currency),
    )

    created = use_case.execute(application)

    return {
        "id": created.id,
        "status": created.status.value,
    }



@router.get("/{application_id}")
def get_credit_application(
    application_id: str,
    use_case: GetCreditApplication = Depends(get_credit_application),
):
    return use_case.execute(application_id)

@router.post("/{application_id}/bank-snapshot")
def attach_bank_snapshot(
    application_id: str,
    use_case: AttachBankSnapshot = Depends(get_attach_bank_snapshot),
):
    use_case.execute(application_id)
    return {"status": "bank_snapshot_attached"}

@router.post("/{application_id}/approve")
def approve_credit_application(
    application_id: str,
    use_case: ApproveCreditApplication = Depends(get_approve_credit_application),
):
    use_case.execute(application_id)
    return {"status": "approved"}

@router.post("/{application_id}/reject")
def reject_credit_application(
    application_id: str,
    use_case: RejectCreditApplication = Depends(get_reject_credit_application),
):
    use_case.execute(application_id)
    return {"status": "rejected"}

@router.get("/")
def list_credit_applications(
    country: str | None = None,
    status: str | None = None,
    use_case: ListCreditApplications = Depends(get_list_credit_applications),
):
    return use_case.execute(country=country, status=status)




