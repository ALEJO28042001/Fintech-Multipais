from enum import Enum

class Country(str, Enum):
    """
    Supported countries for credit applications.
    """
    PT = "PT"
    IT = "IT"
    ES = "ES"
    MX = "MX"
    BR = "BR"
    CO = "CO"

class Currency(str, Enum):
    EUR = "EUR"
    USD = "USD"
    COP = "COP"
    MXN = "MXN"
    BRL = "BRL"

class DocumentType(str, Enum):
    """
    Supported document types across all countries.
    Country-specific validation is done via policies.
    """
    CC = "CC"     # Colombia
    CF = "CF"     # Italy  
    CPF = "CPF"     # Brazil
    CURP = "CURP"   # Mexico
    DNI = "DNI"   # Spain
    NIF = "NIF"   # Portugal

class ApplicationStatus(str, Enum):
    """
    Lifecycle states of a credit application.
    """
    CREATED = "CREATED"
    VALIDATED = "VALIDATED"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

