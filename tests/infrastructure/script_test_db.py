from infrastructure.database.session import engine
from infrastructure.database.base import Base

from infrastructure.database.models import credit_application  

def main():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")


if __name__ == "__main__":
    main()
