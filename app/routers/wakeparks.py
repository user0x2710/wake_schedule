from functools import lru_cache

from app.celery import celery_app
from app.tasks.get_timetable import request_shedule
from celery.result import GroupResult
from core.config import config
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import ORJSONResponse

router = APIRouter(
    prefix="/wakeparks",
    tags=["items"],
)


@lru_cache()
def get_items():
    return list(config.SHEDULE_ITEMS.keys())


@router.get("/", response_class=ORJSONResponse)
def items(items: list = Depends(get_items)):
    return items


@router.get("/{item_id}", response_class=ORJSONResponse, status_code=202)
def get_item(item_id: str):
    if item_id not in config.SHEDULE_ITEMS:
        raise HTTPException(status_code=404)
    task = request_shedule(item_id).apply_async()
    task.save()

    return {"task_id": task.id}


@router.get("/tasks/{task_id}", response_class=ORJSONResponse)
def get_status(task_id: str, response: Response):
    task_result = GroupResult.restore(task_id, app=celery_app)

    if task_result is None:
        raise HTTPException(status_code=404)
    if task_result.ready():
        result_data = task_result.get()
        return result_data

    response.status_code = 202
    return {"task_id": task_id}
