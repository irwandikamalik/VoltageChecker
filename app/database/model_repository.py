class ModelRepository:

    def __init__(self, database):
        self.database = database


    def add_model(
        self,
        model_name,
        voltage_lower,
        voltage_upper,
        current_lower,
        current_upper
    ):

        cursor = self.database.connection.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO models (
                    model_name,
                    voltage_lower,
                    voltage_upper,
                    current_lower,
                    current_upper
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    model_name,
                    voltage_lower,
                    voltage_upper,
                    current_lower,
                    current_upper
                )
            )

            self.database.connection.commit()

            return True

        except Exception as error:

            print(
                "Gagal menambahkan model:",
                error
            )

            return False


    def get_model(self, model_name):

        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            SELECT
                model_name,
                voltage_lower,
                voltage_upper,
                current_lower,
                current_upper
            FROM models
            WHERE model_name = ?
            """,
            (model_name,)
        )

        result = cursor.fetchone()

        if result is None:
            return None

        return {
            "model_name": result[0],
            "voltage_lower": result[1],
            "voltage_upper": result[2],
            "current_lower": result[3],
            "current_upper": result[4]
        }


    def get_all_models(self):

        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                model_name,
                voltage_lower,
                voltage_upper,
                current_lower,
                current_upper
            FROM models
            ORDER BY id
            """
        )

        return cursor.fetchall()


    def delete_model(self, model_name):

        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            DELETE FROM models
            WHERE model_name = ?
            """,
            (model_name,)
        )

        self.database.connection.commit()

        return cursor.rowcount > 0

    def update_model(
        self,
        model_name,
        voltage_lower,
        voltage_upper,
        current_lower,
        current_upper
    ):

        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            UPDATE models
            SET
                voltage_lower = ?,
                voltage_upper = ?,
                current_lower = ?,
                current_upper = ?
            WHERE model_name = ?
            """,
            (
                voltage_lower,
                voltage_upper,
                current_lower,
                current_upper,
                model_name
            )
        )

        self.database.connection.commit()

        return cursor.rowcount > 0