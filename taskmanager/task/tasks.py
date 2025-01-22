from celery import shared_task


@shared_task
def send_event_end(task_id: int, user_id: int):
    print("Sending email end")