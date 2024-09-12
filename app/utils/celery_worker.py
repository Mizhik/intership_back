import asyncio
from datetime import timedelta, datetime
from sqlalchemy import func, select
from app.database.db import sessionmanager
from app.entity.models import User, Result, Quiz, Notification
from celery.schedules import crontab
from celery import Celery
from app.core.settings import config

celery_app = Celery(
    main="tasks",
    broker=config.CELERY_BROKER_URL,
    backend=config.CELERY_BACKEND_URL,
)

celery_app.conf.update(
    broker_connection_retry_on_startup=True,
    beat_schedule={
        "run-every-day-at-midnight": {
            "task": "app.utils.celery_worker.run_user_quiz_check",
            "schedule": crontab(minute=0, hour=0),
        }
    },
)


@celery_app.task(autoretry_for=(Exception,), retry_backoff=True)
def run_user_quiz_check():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_user_quiz_check_async())


async def run_user_quiz_check_async():
    async with sessionmanager.session() as session:
        users = await session.execute(select(User))
        users = users.scalars().all()
        now = datetime.now()

        for user in users:
            subquery = (
                select(
                    Result.quiz_id, func.max(Result.create_at).label("latest_attempt")
                )
                .where(Result.user_id == user.id)
                .group_by(Result.quiz_id)
                .subquery()
            )

            quiz_results = await session.execute(
                select(Result).join(
                    subquery,
                    (Result.quiz_id == subquery.c.quiz_id)
                    & (Result.create_at == subquery.c.latest_attempt),
                )
            )
            quiz_results = quiz_results.scalars().all()

            for quiz_result in quiz_results:
                quiz = await session.get(Quiz, quiz_result.quiz_id)

                if now - quiz_result.create_at > timedelta(hours=24):
                    notification_message = f"It's time to take the quiz '{quiz.title}'!"
                    notification = Notification(
                        user_id=user.id, text=notification_message
                    )
                    session.add(notification)
                    await session.commit()
