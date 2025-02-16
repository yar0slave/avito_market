import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from app.main import app
from app import crud, models, schemas

client = TestClient(app)


@pytest.fixture
def mock_db():
    return Mock()


@pytest.fixture
def mock_user():
    return models.User(
        id=1,
        username="testuser",
        password_hash="hashed_password",
        coins=1000
    )


# Unit тесты
def test_create_user(mock_db, mock_user):
    with patch('app.crud.get_user', return_value=None):
        with patch('app.auth.get_password_hash', return_value="hashed_password"):
            mock_db.add = Mock()
            mock_db.commit = Mock()
            mock_db.refresh = Mock()

            user_data = schemas.UserCreate(username="testuser", password="testpass")
            user = crud.create_user(mock_db, user_data)

            mock_db.add.assert_called_once()
            mock_db.commit.assert_called_once()
            mock_db.refresh.assert_called_once()


def test_get_user(mock_db, mock_user):
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    user = crud.get_user(mock_db, "testuser")
    assert user.username == "testuser"


def test_send_coins(mock_db):
    transaction = models.Transaction(
        id=1,
        from_user_id=1,
        to_user_id=2,
        amount=100
    )

    mock_db.add = Mock()
    mock_db.commit = Mock()
    mock_db.refresh = Mock()

    result = crud.send_coins(mock_db, 1, 2, 100)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


@patch('app.main.get_db')
def test_merchandise_purchase_flow(mock_get_db, mock_db, mock_user):
    mock_get_db.return_value = mock_db

    with patch('app.auth.get_current_user', return_value=mock_user):
        with patch('app.crud.get_merchandise', return_value=models.Merchandise(id=1, name="t-shirt", price=80)):
            response = client.get(
                "/api/buy/t-shirt",
                headers={"Authorization": "Bearer test_token"}
            )
            assert response.status_code == 200


@patch('app.main.get_db')
def test_coin_transfer_flow(mock_get_db, mock_db, mock_user):
    mock_get_db.return_value = mock_db

    with patch('app.auth.get_current_user', return_value=mock_user):
        with patch('app.crud.get_user', return_value=models.User(id=2, username="receiver", coins=1000)):
            response = client.post(
                "/api/sendCoin",
                headers={"Authorization": "Bearer test_token"},
                json={"toUser": "receiver", "amount": 100}
            )
            assert response.status_code == 200


@patch('app.main.get_db')
def test_insufficient_funds(mock_get_db, mock_db, mock_user):
    mock_get_db.return_value = mock_db

    with patch('app.auth.get_current_user', return_value=mock_user):
        with patch('app.crud.get_user', return_value=models.User(id=2, username="receiver", coins=1000)):
            response = client.post(
                "/api/sendCoin",
                headers={"Authorization": "Bearer test_token"},
                json={"toUser": "receiver", "amount": 2000}
            )
            assert response.status_code == 400
            assert "Insufficient funds" in response.json()["detail"]