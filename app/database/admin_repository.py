class AdminRepository:

    def __init__(self, database):
        self.database = database

    def add_admin(self, username, password):

        cursor = self.database.connection.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO admin (
                    username,
                    password
                )
                VALUES (?, ?)
                """,
                (
                    username,
                    password
                )
            )

            self.database.connection.commit()

            return True

        except Exception as error:

            print(
                "Gagal menambahkan admin:",
                error
            )

            return False

    def validate_admin(self, username, password):

        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM admin
            WHERE username = ?
            AND password = ?
            """,
            (
                username,
                password
            )
        )

        result = cursor.fetchone()

        return result is not None

    def get_all_admins(self):

        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            SELECT id, username
            FROM admin
            ORDER BY id
            """
        )

        return cursor.fetchall()