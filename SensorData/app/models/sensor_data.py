# models/sensor_service.py
from dataclasses import dataclass
from typing import Optional

from .database import Database as db
import datetime


'''
SensorData {
  sensorDataId: ObjectId,
  timestamp: Timestamp, // indexed
  accelerometer: {
    x: Double,
    y: Double,
    z: Double
  },
  gyroscope: {
    x: Double,
    y: Double,
    z: Double
  },
  humidity: Number,
  temperature: Double,
  location: {
    type: "Point",
    coordinates: [Double, Double] // [longitude, latitude]
  },
  roadId: ObjectId // ref a Road Management Service
}
'''

#TODO valuta se aggiungere una find all, per processo di tuning da sensore
@dataclass
class SensorData:
    sensor_data_id: int
    accelerometer_x: float
    accelerometer_y: float
    accelerometer_z: float
    gyroscope_x: float
    gyroscope_y: float
    gyroscope_z: float
    timestamp: datetime.datetime
    gps_lat: Optional[float] = None
    gps_lon: Optional[float] = None

    def init_db(self):
        con = db.connect()
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS sensors_data
                          (
                              sensor_dataId INTEGER PRIMARY KEY AUTOINCREMENT,
                              acc_x REAL,
                              acc_y REAL,
                              acc_z REAL,
                              gyro_x REAL,
                              gyro_y REAL,
                              gyro_z REAL,
                              timestamp DATETIME,
                              gps_latitudine REAL,
                              gps_longitudine REAL
                          )
                       """)
        con.commit()
        con.close()

    @staticmethod
    def insert_sensor_data(sensor_data):
        con = db.connect()
        cursor = con.cursor()
        #qui sulle query usare i placeholder per evitare sql injection
        cursor.execute("""INSERT INTO sensors_data
                          (
                              sensor_dataId, 
                              acc_x, acc_y,acc_z,
                              gyro_x, gyro_y,gyro_z,
                              gps_lat, gps_lon
                          )
                          VALUES (?,?,?,?,?,?,?,?)
                           """,
                          (sensor_data.sensor_dataId,
                            sensor_data.accelerometer_x,
                            sensor_data.accelerometer_y,
                            sensor_data.accelerometer_z,
                            sensor_data.gyroscope_x,
                            sensor_data.gyroscope_y,
                            sensor_data.gyroscope_z,
                            sensor_data.gps_lat,
                            sensor_data.gps_lon
                          )
                       )
        row = cursor.lastrowid
        con.commit()
        con.close()
        return row


    @staticmethod
    def find_by_sensor_id(sensor_data_id):
        con = db.connect()
        cursor = con.cursor()
        cursor.execute("""SELECT * FROM sensors_data WHERE sensor_dataId = ?""",
                       (sensor_data_id))
        row = cursor.fetchone()
        con.commit()
        con.close()
        return row

    @staticmethod
    def update_sensor(sensor_data):
        con = db.connect()
        cursor = con.cursor()
        cursor.execute("""UPDATE sensors_data
                          SET accelerometer_x = ?,
                              accelerometer_y = ?,
                              accelerometer_z = ?,
                              gyroscope_x = ?,
                              gyroscope_y = ?,
                              gyroscope_z = ?,
                              gps_lat = ?,
                              gps_lon = ?
                          WHERE sensor_dataId = ?
                       """,
                       (
                        sensor_data.sensor_dataId,
                        sensor_data.accelerometer_x,
                        sensor_data.accelerometer_y,
                        sensor_data.accelerometer_z,
                        sensor_data.gyroscope_x,
                        sensor_data.gyroscope_y,
                        sensor_data.gyroscope_z,
                        sensor_data.gps_lat,
                        sensor_data.gps_lon
                        )
                       )
        affected_rows = cursor.rowcount
        con.commit()
        con.close()
        return affected_rows


    @staticmethod
    def delete_sensor(self, sensor_data_id):
        con = db.connect()
        cursor = con.cursor()
        cursor.execute("""DELETE FROM sensors_data WHERE sensor_data_id = ?""",(sensor_data_id,))

        con.commit()
        con.close()


    @classmethod
    def create_sensor(cls, sensor_data_id: str, accelerometer_x: float,accelerometer_y: float,accelerometer_z: float
                      , gyroscope_x: float,gyroscope_y: float,gyroscope_z: float,
                      gps_lat: float,gps_lon: float):
        """Factory method to create a new sensor"""
        return cls(sensor_data_id, accelerometer_x, accelerometer_y, accelerometer_z,
                   gyroscope_x,gyroscope_y,gyroscope_z,
                   gps_lat,gps_lon)


    def save(self):
        """Saves this sensor instance to the database"""
        id = self.find_by_sensor_id(self.senso_data_id)
        if id is None:
            self.insert_sensor(self) # CREATE
        else:
            self.update_sensor(self) # UPDATE

'''

@dataclass
class PredictionResult:
    road_condition: str
    confidence: float
    timestamp: str
    sensor_id: str

    '''


