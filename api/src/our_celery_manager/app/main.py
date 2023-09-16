from pathlib import Path
from typing import Annotated

from sqlalchemy.orm import Session

from fastapi import FastAPI, Query, Request, Depends, Response
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from our_celery_manager.app.models.dtos.tasks import ListResult, ListResultRow

from our_celery_manager.app.models.task.TaskResult import TaskResultPage
from our_celery_manager.app.service.celery.results import result_page, clone_and_send_task, result_page_exp

from .service.celery.model import SearchField, SortField
from .settings import SettingsApiResponse, settings

from .startup_checks import pre_startup_check, pre_startup_db_migration

from .db import SessionLocal

import logging

pre_startup_check()
pre_startup_db_migration()

logging.basicConfig(level=logging.INFO, force=True)
logger = logging.getLogger(__name__)
logger.info("OK")

app = FastAPI(root_path=settings.root_path)

def get_db():
    """
    Ceates a database session.
    It aims at being used as a fastapi dependency. See: https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-dependency
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/info", response_model=SettingsApiResponse)
async def info():
    displayable_settings = settings.hiding_passwords()
    return SettingsApiResponse.from_settings(displayable_settings)


@app.get("/old/results/page", response_model=TaskResultPage)
async def task_result_page(
    request: Request,
    n: int = 0,
    size: int = 10,
    sort: Annotated[list[str], Query()] = [],
    search: Annotated[list[str], Query()] = [],
    session: Session = Depends(get_db),
):
    sorts = [SortField.from_api_str(s) for s in sort if s is not None and s != ""]
    searchs = [SearchField.from_api_str(s) for s in search if s is not None and s != ""]
    results = result_page(size, n, sorts, searchs, session)
    return results

@app.get("/results/page", response_model=ListResult)
async def task_result_page_exp(
    request: Request,
    n: int = 0,
    size: int = 10,
    sort: Annotated[list[str], Query()] = [],
    search: Annotated[list[str], Query()] = [],
    session: Session = Depends(get_db)
):
    sorts = [SortField.from_api_str(s) for s in sort if s is not None and s != ""]
    searchs = [SearchField.from_api_str(s) for s in search if s is not None and s != ""]
    r = result_page_exp(size, n, sorts, searchs, session)
    return r

@app.post("/clone_and_send/{id}")
async def clone_and_send(request: Request, id: str, session: Session = Depends(get_db)):
    """Clone la tâche et la renvoie sur le broker"""
    r = clone_and_send_task(id, session)
    return r


static_path = Path(__file__).parent / 'static'
app.mount("/", StaticFiles(directory=static_path, html=True), name="static")

@app.exception_handler(Exception)
def handle_exception(req, exception):
    logger.exception(exception, exc_info=exception, stack_info=True)
    return Response("ISE", status_code=500)