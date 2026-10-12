import asyncio

from sqlmodel import SQLModel

from app.app import main
from app.database import database


if __name__ == "__main__":
    print("Initializing Database.")
    SQLModel.metadata.create_all(bind=database.engine)
    asyncio.run(main())