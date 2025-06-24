#model/sensor.py
import enum
from dataclasses import dataclass
import app.models.database as db
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
    installationDate: datetime
    lastCalibration: datetime
    status: Status

    '''Esegue le query di creazione'''
    def init_db(self):
        con = db.Database.connect()
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS sensors 
                          ( sensorId INTEGER PRIMARY KEY AUTOINCREMENT,
                            model TEXT,
                            serial INTEGER,
                            installationDate DATETIME,
                            lastCalibration DATETIME,
                            status TEXT
                            )
        """)
        con.commit()
        con.close()


    def insert_sensor(self, sensor):
        con = db.Database.connect()
        cursor = con.cursor()
        #qui sulle query usare i placeholder per evitare sql injection
        cursor.execute("""INSERT INTO sensors
                          (sensorId, serial, model, firmware, installationDate, lastCalibration, status)
                          VALUES (?, ?, ?, ?, ?, ?)
                       """,
                       (sensor.sensorId,
                        sensor.serial,
                        sensor.model,
                        sensor.installationDate,
                        sensor.lastCalibration,
                        sensor.status.value))
        con.commit()
        con.close()


    def findBySensorId(self, sensorId):
        con = db.Database.connect()
        cursor = con.cursor()
        cursor.execute("""SELECT * FROM sensors WHERE sensorId = ?""",
                       (sensorId))
        con.commit()
        con.close()

    def updateSensor(self, sensor):
        con = db.Database.connect()
        cursor = con.cursor()
        cursor.execute("""UPDATE sensors
                          SET serial           = ?,
                              model            = ?,
                              installationDate = ?,
                              lastCalibration  = ?,
                              status           = ?
                          WHERE sensorId = ?
                       """,
                       (sensor.serial,
                        sensor.model,
                        sensor.installationDate,
                        sensor.lastCalibration,
                        sensor.status.value,
                        sensor.sensorId)
                       )
        con.commit()
        con.close()
        return cursor.rowcount


    def deleteSensor(self, sensorId):
        con = db.Database.connect()
        cursor = con.cursor()
        cursor.execute("""DELETE FROM sensors WHERE sensorId = ?""",(sensorId))

        con.commit()
        con.close()


    @classmethod
    def create_sensor(cls, sensorId: str, serial: int, model: str,
                      installationDate: datetime, lastCalibration: datetime,
                      status: Status = Status.ACTIVE):
        """Factory method to create a new sensor"""
        return cls(sensorId, serial, model, installationDate, lastCalibration, status)


    def save(self):
        """Saves this sensor instance to the database"""
        id = self.findBySensorId(self.sensorId)
        if id is None:
            self.insert_sensor(self) # CREATE
        else:
            self.updateSensor(self) # UPDATE


