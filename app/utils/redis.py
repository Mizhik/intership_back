import json
from fastapi import HTTPException

from app.entity.models import Result
from app.database.redis_connector import get_redis_client


class Redis:

    @staticmethod
    async def save_data_to_redis_db(key, value):
        redis = await get_redis_client()
        await redis.set(key, value)
        await redis.expire(key, 48 * 3600)
        await redis.close()

    @staticmethod
    async def get_data_from_redis_db(key):
        redis = await get_redis_client()
        result = await redis.get(key)
        await redis.close()
        return result

    @staticmethod
    async def delete_data_from_redis_db(key):
        redis = await get_redis_client()
        await redis.delete(key)
        await redis.close()

    @staticmethod
    async def save_results_to_redis(quiz_results: Result, answers_input: list[dict]):
        try:
            detailed_answers = []
            for answer in answers_input:
                detailed_answers.append(
                    {
                        "question": str(answer["question"]),
                        "answer": [aid.title for aid in answer["answer"]],
                        "is_correct": answer["is_correct"],
                    }
                )

            quiz_result_data = {
                "user_id": str(quiz_results.user_id),
                "quiz_name": quiz_results.quiz.title,
                "company_name": str(quiz_results.quiz.company.name),
                "answers": detailed_answers,
            }

            key = f"{quiz_results.user_id}:{quiz_results.quiz_id}:{quiz_results.quiz.company_id}"
            await Redis.save_data_to_redis_db(
                key,
                json.dumps(quiz_result_data),
            )
        except Exception as e:
            raise HTTPException(
                status_code=409, detail=f"Can't save data to redis: {str(e)}"
            )
