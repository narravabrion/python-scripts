import psycopg2
import csv
from twilio.rest import Client


class DataEntry:
    def __init__(self, filepath):
        self.filepath = filepath

    def sendSMS(self, message):
        account_sid = '<account_sid>'
        auth_token = '<auth_token>'
        client = Client(account_sid, auth_token)

        try:
            message = client.messages \
            .create(
                body=message,
                from_='<twilio_number>',
                to='<phone_number>'
            )

            print(message.sid)
        except Exception as error:
            print(error)


    def connectDB(self):
        try:
            with psycopg2.connect(
                dbname="<dbname>",
                user="<username>",
                password="<password>",
                host="<host>",
                port="<port>"
            ) as conn:
                print("Database connected")
                return conn
        except (psycopg2.DatabaseError) as error:
            print(error)

    def read_file(self):
        try:
            with open(self.filepath, 'r') as file:
                csv_data = csv.reader(file)
                next(csv_data)
                return list(csv_data)
        except FileNotFoundError as error:
            print(error)

    def insertData(self):
        csv_data = self.read_file()
        data_length = len(csv_data)
        message = f"seccessfully inserted {data_length} records into the database"
        try:
            
            with self.connectDB() as conn:
                with conn.cursor() as cur:
                    for row in csv_data:
                        cur.execute(
                            "INSERT INTO scores (entry_no, first_name, second_name, score) VALUES (%s, %s, %s, %s)", row
                        )
                        conn.commit()
                    print("Data inserted successfully")
                    self.sendSMS(message)
        except psycopg2.DatabaseError as error:
            print(error)


if __name__ == "__main__":
    data = DataEntry("data.csv")
    data.insertData()

