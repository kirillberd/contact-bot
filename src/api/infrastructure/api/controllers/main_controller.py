from fastapi import APIRouter, Depends, Query, HTTPException, Path
from fastapi.responses import JSONResponse
from infrastructure.container import Container
from fastapi.concurrency import run_in_threadpool
from dependency_injector.wiring import inject, Provide
from infrastructure.repositories.contact_repository import IContactRepository
from domain.contact import Contact
from loguru import logger
from typing import List, Optional

router = APIRouter(prefix="/api")


@router.post("/insert-contact")
@inject
async def insert_contact(
    contact: Contact,
    contact_repository: IContactRepository = Depends(
        Provide[Container.contact_repository]
    ),
):

    try:
        await run_in_threadpool(contact_repository.add, contact)
        return JSONResponse(
            status_code=200, content={"detail": "Contact added successfully"}
        )
    except Exception as e:
        logger.error(f"Error adding contact: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error while inserting contacts"
        )


@router.get("/contacts")
@inject
async def get_contacts(
    tags: Optional[List[str]] = Query(None, description="Filter by tags (any match)"),
    region: Optional[str] = Query(None, description="Filter by exact region match"),
    contact_repository: IContactRepository = Depends(
        Provide[Container.contact_repository]
    ),
):
    try:
        contacts = await run_in_threadpool(
            contact_repository.get, tags=tags, region=region
        )
        return contacts
    except Exception as e:
        logger.error(f"Error fetching contacts: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error while fetching contacts"
        )


@router.put("/contacts/{id}")
@inject
async def update_contact(
    id: int,
    contact: Contact,
    contact_repository: IContactRepository = Depends(
        Provide[Container.contact_repository]
    ),
):

    try:
        await run_in_threadpool(contact_repository.update, contact, id)
        return JSONResponse(
            status_code=200, content={"detail": "Contact updated successfully"}
        )
    except Exception as e:
        logger.error(f"Error updating contacts: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error while updating contact"
        )

@router.delete("/contacts/{id}")
@inject
async def delete_contact(
    id: int,
    contact_repository: IContactRepository = Depends(
        Provide[Container.contact_repository]
    )
):
    try:
        await run_in_threadpool(contact_repository.delete, id)
        return JSONResponse(
            status_code=200, content={"detail": "Contact deleted successfully"}
        )
    except Exception as e:
        logger.error(f"Error deleting contact: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error while deleting contact"
        )

