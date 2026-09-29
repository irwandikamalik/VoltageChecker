from app.database.database import Database


class OperatorRepository:

    def __init__(self, database):

        self.database = database

    def add_operator(self, operator_id, name):
        cursor = self.database.connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO operators (operator_id, name)
                VALUES (?, ?)
                """,
                (operator_id, name)
            )

            self.database.connection.commit()

            return True
 
        except Exception as error:
 
            print("Gagal menambahkan operator", error)

            return False

    def is_valid_operator(self, operator_id):
        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM operators
            WHERE operator_id = ?
            """,
            (operator_id,)
        )

        result = cursor.fetchone()

        return result is not None

    def get_operator(self, operator_id):
        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            SELECT operator_id, name
            FROM operators
            WHERE operator_id = ?
            """,
            (operator_id,)
        )

        result = cursor.fetchone()

        if result is  None:
            return None

        return {
            "operator_id" : result[0],
            "name" : result[1]
        }

    def get_all_operators(self):
        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            SELECT id, operator_id, name
            FROM operators
            ORDER by id
            """
        )

        return cursor.fetchall()

    def delete_operator(self, operator_id):
        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            DELETE FROM operators
            WHERE operator_id = ?
            """,
            (operator_id,)
        )