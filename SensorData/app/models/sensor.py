#model/sensor.py
import enum
from dataclasses import dataclass
from .database import Database as db

import datetime

'''
Sensor {
  sensorId: string,
  serial: Number,
  model: String,
  firmware: String,
  installationDate: Timestamp,
  lastCalibration: Timestamp,
  status: Enum["ACTIVE", "INACTIVE", "MAINTENANCE"]
}
'''

class Status(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    MAINTENANCE = "MAINTENANCE"




@dataclass
class Sensor:
    sensorId: str
    serial: int
    model: str
    status: Status

    '''Esegue le query di creazione'''

    @staticmethod
    def init_db():
        con = db.connect()
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS sensors
                          (
                              sensorId INTEGER PRIMARY KEY AUTOINCREMENT,
                              serial INTEGER, 
                              model TEXT,
                              status TEXT
                          )
                       """)
        con.commit()
        con.close()

    @staticmethod
    def insert_sensor(sensor):
        con = db.connect()
        cursor = con.cursor()
        print(f"Status type: {type(sensor.status)}")
        print(f"Status value: {sensor.status}")

        #verifica che sia una stringa
        status_value = str(sensor.status)
        if hasattr(sensor.status, 'value'):
            status_value = str(sensor.status.value)

        print(f"Final status_value: {status_value}")
        print(f"Final status_value type: {type(status_value)}")

        cursor.execute("""INSERT INTO sensors
                              ( serial, model, status)
                          VALUES ( ?, ?, ?)
                       """,
                       (
                        int(sensor.serial),
                        str(sensor.model),
                        status_value))
        row = cursor.lastrowid
        con.commit()
        con.close()
        return row

    @staticmethod
    def find_by_sensor_id(sensor_id):
        con = db.connect()
        cursor = con.cursor()
        cursor.execute("""SELECT * FROM sensors WHERE sensorId = ?""",
                       sensor_id)
        row =cursor.fetchone()
        con.commit()
        con.close()
        return row

    @staticmethod
    def find_all():
        con = db.connect()
        cursor = con.cursor()
        cursor.execute("""SELECT * FROM sensors""")
        row = cursor.fetchall()
        con.commit()
        con.close()
        return row

    @staticmethod
    def update_sensor(sensor):
        con = db.connect()
        cursor = con.cursor()
        cursor.execute("""UPDATE sensors
                          SET serial           = ?,
                              model            = ?,
                              status           = ?
                          WHERE sensorId = ?
                       """,
                       (sensor.serial,
                        sensor.model,
                        sensor.status.value,
                        sensor.sensorId)
                       )
        # questa restituisce delle tuple
        affected_rows = cursor.rowcount
        con.commit()
        con.close()
        return affected_rows

    @staticmethod
    def delete_sensor(sensorId):
        con = db.connect()
        cursor = con.cursor()
        cursor.execute("""DELETE FROM sensors WHERE sensorId = ?""",(sensorId))

        con.commit()
        con.close()


    @classmethod
    def create_sensor(cls, sensorId: str, serial: int, model: str,
                      status: Status = Status.ACTIVE):
        """Factory method to create a new sensor"""
        return cls(sensorId, serial, model, status)


    def save(self):
        """Saves this sensor instance to the database"""
        try:
            if self.sensorId:
                # Verifica se esiste già un sensore con questo ID
                existing = self.find_by_sensor_id(self.sensorId)
                if existing:
                    print("update")
                    return self.update_sensor(self)

            print("insert")
            return self.insert_sensor(self)

        except Exception as e:
            print(f"Errore durante il salvataggio: {str(e)}")
            raise


