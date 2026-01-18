from sqlalchemy.orm import Session

from core.credit_applications.repository import CreditApplicationRepository
from core.credit_applications import CreditApplication, Applicant,Document
from core.credit_applications.enums import Country, ApplicationStatus
from core.credit_applications.value_objects import Money, Income

from datetime import datetime
from core.credit_applications import CreditApplication, BankSnapshot

from infrastructure.database.session import get_session
from infrastructure.database.models.credit_application import CreditApplicationModel


class PostgresCreditApplicationRepository(
    CreditApplicationRepository
):
    def __init__(self, session: Session | None = None):
        self.session = session or get_session()

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------
    def save(self, application: CreditApplication) -> None:
        model = (
            self.session.get(CreditApplicationModel, application.id)
            or CreditApplicationModel(id=application.id)
        )

        model.country = application.country.value
        model.status = application.status.value

        model.full_name = application.applicant.full_name
        model.document_type = application.applicant.document.document_type
        model.document_value = application.applicant.document.value

        model.requested_amount = application.requested_amount.amount
        model.currency = application.requested_amount.currency
        model.monthly_income = application.monthly_income.monthly_amount

        model.created_at = application.created_at
        model.bank_snapshot = self._serialize_snapshot(
            application.bank_snapshot
        )
        self.session.add(model)
        self.session.commit()

    # ------------------------------------------------------------------
    # Get by ID
    # ------------------------------------------------------------------
    def get(self, application_id: str) -> CreditApplication | None:
        model = self.session.get(
            CreditApplicationModel,
            application_id,
        )
        return self._to_domain(model) if model else None

    # ------------------------------------------------------------------
    # List
    # ------------------------------------------------------------------
    def list(
        self,
        country: Country | None = None,
        status: ApplicationStatus | None = None,
    ) -> list[CreditApplication]:
        query = self.session.query(CreditApplicationModel)

        if country:
            query = query.filter(
                CreditApplicationModel.country == country
            )

        if status:
            query = query.filter(
                CreditApplicationModel.status == status
            )

        return [self._to_domain(m) for m in query.all()]


    # ------------------------------------------------------------------
    # Mapper (private)
    # ------------------------------------------------------------------
    def _to_domain(
        self,
        model: CreditApplicationModel,
    ) -> CreditApplication:
        application = CreditApplication(
            id=model.id,
            country=Country(model.country),
            applicant=Applicant(
                full_name=model.full_name,
                document = Document(
                    document_type=model.document_type,
                    value=model.document_value,
                    country=Country(model.country)
                    )
                
            ),
            requested_amount=Money(
                model.requested_amount,
                model.currency,
            ),
            monthly_income=Income(model.monthly_income,model.currency),
        )

        application.status = ApplicationStatus(model.status)

        application.bank_snapshot = self._deserialize_snapshot(
            model.bank_snapshot
        )
        application.created_at = model.created_at

        return application

    def _serialize_snapshot(
        self, snapshot: BankSnapshot | None
    ) -> dict | None:
        if snapshot is None:
            return None

        return {
            "provider": snapshot.provider,
            "payload": snapshot.payload,
            "fetched_at": snapshot.fetched_at.isoformat(),
        }

    def _deserialize_snapshot(
        self, data: dict | None
    ) -> BankSnapshot | None:
        if data is None:
            return None

        return BankSnapshot(
            provider=data["provider"],
            payload=data["payload"],
            fetched_at=datetime.fromisoformat(data["fetched_at"]),
        )
