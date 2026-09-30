class BatchRepository:

    def __init__(self, database):
        self.database = database

    def create_batch(
        self,
        batch_code,
        model_name,
        created_at
    ):

        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            INSERT INTO batches (
                batch_code,
                model_name,
                created_at,
                current_sequence,
                status
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                batch_code,
                model_name,
                created_at,
                1,
                "ACTIVE"
            )
        )

        self.database.connection.commit()

    def get_active_batch(self):

        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                batch_code,
                model_name,
                created_at,
                current_sequence,
                status
            FROM batches
            WHERE status = 'ACTIVE'
            ORDER BY id DESC
            LIMIT 1
            """
        )

        return cursor.fetchone()

    def update_sequence(
        self,
        batch_id,
        sequence_number
    ):

        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            UPDATE batches
            SET current_sequence = ?
            WHERE id = ?
            """,
            (
                sequence_number,
                batch_id
            )
        )

        self.database.connection.commit()

    def close_batch(self, batch_id):

        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            UPDATE batches
            SET status = 'CLOSED'
            WHERE id = ?
            """,
            (batch_id,)
        )

        self.database.connection.commit()