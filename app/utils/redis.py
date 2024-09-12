import json
from fastapi import HTTPException
from fastapi.responses import FileResponse
import json
import csv
import tempfile
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
    async def get_data_by_pattern(pattern: str):
        redis = await get_redis_client()
        data = []
        keys = await redis.keys(pattern)
        for key in keys:
            value = await redis.get(key)
            if value:
                data.append(json.loads(value))
        await redis.close()
        return data

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

    @staticmethod
    async def export_redis_data(query: str, file_format: str):
        data = await Redis.get_data_by_pattern(query)
        if file_format == "json":
            temp_json_file = tempfile.NamedTemporaryFile(
                delete=False, mode="w", suffix=".json"
            )
            json.dump(data, temp_json_file, indent=2)
            temp_json_file.close()

            return FileResponse(
                path=temp_json_file.name,
                filename="quiz_results.json",
                media_type="multipart/form-data",
            )

        elif file_format == "csv":
            with tempfile.NamedTemporaryFile(
                delete=False, mode="w", suffix=".csv"
            ) as temp_csv_file:
                fieldnames = [
                    "user_id",
                    "company_name",
                    "quiz_name",
                    "question",
                    "answer",
                    "is_true",
                ]
                writer = csv.DictWriter(temp_csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for item in data:
                    user_id = item["user_id"]
                    company_name = item["company_name"]
                    quiz_name = item["quiz_name"]
                    answers = item["answers"]
                    for question_data in answers:
                        writer.writerow(
                            {
                                "user_id": user_id,
                                "company_name": company_name,
                                "quiz_name": quiz_name,
                                "question": question_data["question"],
                                "answer": ", ".join(question_data["answer"]),
                                "is_true": question_data["is_correct"],
                            }
                        )
            return FileResponse(
                temp_csv_file.name,
                filename="quiz_results.csv",
                media_type="multipart/form-data",
            )
