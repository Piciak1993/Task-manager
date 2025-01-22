from typing import List, Optional
from fastapi import HTTPException, status
import models, stream, tasks


async def create_task(request, database) -> models.Task:
    new_task = models.Task(title=request.title,
        description=request.description,
        start_time=request.start_time,
        end_time=request.end_time,
        hours_to_complete=request.hours_to_complete,
        user_id=request.user_id
    )

    database.add(new_task)
    database.commit()
    database.refresh(new_task)
    tasks.send_event_end.delay(new_task.user_id, new_task.id)
    event_data = stream.generate_event_data(user_id=new_task.user_id, task_id=new_task.id, action='created')
    stream.send_event(event_data)

    return new_task


async def update_task(request, database, task_id: int) -> models.Task:

    task = database.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = request.title
    task.description = request.description
    task.start_time = request.start_time
    task.end_time = request.end_time
    task.hours_to_complete = request.hours_to_complete
    task.user_id = request.user_id



    database.commit()
    database.refresh(task)

    event_data = stream.generate_event_data(user_id=request.user_id, task_id=task_id, action='update')
    stream.send_event(event_data)

    return task


async def get_tasks(database) -> List[models.Task]:
    tasks = database.query(models.Task).all()
    return tasks


async def get_task_by_id(task_id, database) -> Optional[models.Task]:
    task_info = database.query(models.Task).get(task_id)
    if not task_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found !")
    return task_info