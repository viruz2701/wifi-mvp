from fastapi import APIRouter
from app.tasks import example_task

router = APIRouter()

@router.get("/test-celery")
def test_celery():
    task = example_task.delay("Hello from FastAPI")
    return {"task_id": task.id}