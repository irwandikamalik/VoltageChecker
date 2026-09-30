from app.database.database import Database
from app.database.model_repository import ModelRepository


database = Database()
database.create_tables()

model_repository = ModelRepository(database)


# =====================================
# Tambahkan MODEL-A
# =====================================

success = model_repository.add_model(
    "MODEL-A",
    23.00,
    25.00,
    0.100,
    0.200
)

print("Tambah MODEL-A:", success)


# =====================================
# Ambil MODEL-A
# =====================================

model = model_repository.get_model(
    "MODEL-A"
)

print("\nData MODEL-A:")

print(model)


# =====================================
# Tampilkan semua model
# =====================================

models = model_repository.get_all_models()

print("\nSemua model:")

for model in models:

    print(model)