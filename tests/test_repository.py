import sqlite3

from app.database.database import Database
from app.database.operator_repository import OperatorRepository
from app.database.model_repository import ModelRepository
from app.database.batch_repository import BatchRepository

def create_database(tmp_path):

    db_path = tmp_path / "test.db"

    database = Database(
        db_path=str(db_path)
    )

    database.create_tables()

    return database

def test_add_operator(tmp_path):

    database = create_database(tmp_path)

    repository = OperatorRepository(database)

    result = repository.add_operator(
        "OP100",
        "Test Operator"
    )

    assert result is True

    operator = repository.get_operator(
        "OP100"
    )

    assert operator["operator_id"] == "OP100"
    assert operator["name"] == "Test Operator"

    database.close()

def test_operator_not_found(tmp_path):

    database = create_database(tmp_path)

    repository = OperatorRepository(database)

    result = repository.get_operator(
        "OP999"
    )

    assert result is None

    database.close()

def test_is_valid_operator(tmp_path):

    database = create_database(tmp_path)

    repository = OperatorRepository(database)

    repository.add_operator(
        "OP100",
        "Test Operator"
    )

    assert repository.is_valid_operator(
        "OP100"
    ) is True

    assert repository.is_valid_operator(
        "OP999"
    ) is False

    database.close()

def test_add_model(tmp_path):

    database = create_database(tmp_path)

    repository = ModelRepository(database)

    result = repository.add_model(
        model_name="MODEL-TEST",
        voltage_lower=23.0,
        voltage_upper=25.0,
        current_lower=0.100,
        current_upper=0.200
    )

    assert result is True

    model = repository.get_model(
        "MODEL-TEST"
    )

    assert model["model_name"] == "MODEL-TEST"
    assert model["voltage_lower"] == 23.0
    assert model["voltage_upper"] == 25.0
    assert model["current_lower"] == 0.100
    assert model["current_upper"] == 0.200

    database.close()

def test_create_and_get_active_batch(tmp_path):

    database = create_database(tmp_path)

    repository = BatchRepository(database)

    repository.create_batch(
        batch_code="MDF261001120000",
        model_name="MODEL-TEST",
        created_at="2026-10-01 12:00:00"
    )

    batch = repository.get_active_batch()

    assert batch is not None

    assert batch[1] == "MDF261001120000"
    assert batch[2] == "MODEL-TEST"
    assert batch[4] == 1
    assert batch[5] == "ACTIVE"

    database.close()

def test_update_batch_sequence(tmp_path):

    database = create_database(tmp_path)

    repository = BatchRepository(database)

    repository.create_batch(
        batch_code="MDF261001120000",
        model_name="MODEL-TEST",
        created_at="2026-10-01 12:00:00"
    )

    batch = repository.get_active_batch()

    batch_id = batch[0]

    repository.update_sequence(
        batch_id=batch_id,
        sequence_number=25
    )

    updated_batch = repository.get_active_batch()

    assert updated_batch[4] == 25

    database.close()