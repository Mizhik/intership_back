import pytest
from unittest.mock import AsyncMock
from uuid import uuid4
from app.services.user import UserService, ErrorNotFound
from app.repository.users import UserRepository
from app.dtos.user import UserSchema, UserUpdate


@pytest.fixture
def mock_user_repository():
    user_repository = AsyncMock(spec=UserRepository)
    return user_repository


@pytest.fixture
def user_service(mock_user_repository):
    return UserService(db=AsyncMock(), repository=mock_user_repository)


@pytest.mark.asyncio
async def test_get_all_users(user_service, mock_user_repository):
    mock_user_repository.get_many.return_value = [
        {"id": str(uuid4()), "username": "testuser"}
    ]
    users = await user_service.get_all_users(0, 100)
    assert isinstance(users, list)


@pytest.mark.asyncio
async def test_get_one_user(user_service, mock_user_repository):
    user_id = uuid4()
    mock_user_repository.get_one.return_value = {
        "id": str(user_id),
        "username": "testuser",
    }
    user = await user_service.get_one_user(user_id)
    assert user["id"] == str(user_id)


@pytest.mark.asyncio
async def test_create_user(user_service, mock_user_repository):
    user_data = UserSchema(username="newuser", email="example@gmail.com", password="password")
    mock_user_repository.create.return_value = {
        "id": str(uuid4()),
        "username": "newuser",
        "email": "example@gmail.com",
        "password": "password",
    }
    user = await user_service.create_user(user_data)
    assert "id" in user
    assert user_data.username == user["username"]
    assert user_data.email == user["email"]
    assert user_data.password != user["password"]


@pytest.mark.asyncio
async def test_update_user(user_service, mock_user_repository):
    user_id = uuid4()
    user_update_data = UserUpdate(username="updateduser")
    mock_user_repository.update.return_value = {
        "id": str(user_id),
        "username": "updateduser",
    }
    user = await user_service.update_user(user_id, user_update_data)
    assert user["username"] == "updateduser"


@pytest.mark.asyncio
async def test_delete_user(user_service, mock_user_repository):
    user_id = uuid4()
    mock_user_repository.delete_res.return_value = {
        "id": str(user_id),
        "username": "testuser",
    }
    user = await user_service.delete_user(user_id)
    assert user["id"] == str(user_id)


@pytest.mark.asyncio
async def test_get_one_user_not_found(user_service, mock_user_repository):
    user_id = uuid4()
    mock_user_repository.get_one.return_value = None
    with pytest.raises(ErrorNotFound):
        await user_service.get_one_user(user_id)
