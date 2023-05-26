from PyQt5.QtSql import QSqlQuery

class Database:

    def insert_camera(placeInRoadId, active, lanesNum):
        sql = QSqlQuery()
        sql.prepare("INSERT INTO Camera (placeInRoadId, active, lanesNum) VALUES (?, ?, ?)")
        sql.addBindValue(placeInRoadId)
        sql.addBindValue(active)
        sql.addBindValue(lanesNum)
        sql.exec_()

    def insert_city(cityName):
        sql = QSqlQuery()
        sql.prepare("INSERT INTO City (cityName) VALUES (?)")
        sql.addBindValue(cityName)
        sql.exec_()

    def insert_day_of_week(dayName):
        sql = QSqlQuery()
        sql.prepare("INSERT INTO DayOfWeek (dayName) VALUES (?)")
        sql.addBindValue(dayName)
        sql.exec_()

    def insert_lane(cameraId, laneInd, point_1_id, point_2_id, point_3_id, point_4_id):
        sql = QSqlQuery()
        sql.prepare("INSERT INTO Lane (cameraId, laneInd, point_1_id, point_2_id, point_3_id, point_4_id) VALUES (?, ?, ?, ?, ?, ?)")
        sql.addBindValue(cameraId)
        sql.addBindValue(laneInd)
        sql.addBindValue(point_1_id)
        sql.addBindValue(point_2_id)
        sql.addBindValue(point_3_id)
        sql.addBindValue(point_4_id)
        sql.exec_()

    def insert_place_in_road(streetId, roadKm, trafficLights, crossroads, closestBuilding):
        sql = QSqlQuery()
        sql.prepare("INSERT INTO PlaceInRoad (streetId, roadKm, trafficLights, crossroads, closestBuilding) VALUES (?, ?, ?, ?, ?)")
        sql.addBindValue(streetId)
        sql.addBindValue(roadKm)
        sql.addBindValue(trafficLights)
        sql.addBindValue(crossroads)
        sql.addBindValue(closestBuilding)
        sql.exec_()

    def insert_point(x, y):
        sql = QSqlQuery()
        sql.prepare("INSERT INTO Point (x, y) VALUES (?, ?)")
        sql.addBindValue(x)
        sql.addBindValue(y)
        sql.exec_()

    def insert_statistics(laneId, dayOfWeekId, time, tlcr, intensity):
        sql = QSqlQuery()
        sql.prepare("INSERT INTO Statistics (laneId, dayOfWeekId, time, tlcr, intensity) VALUES (?, ?, ?, ?, ?)")
        sql.addBindValue(laneId)
        sql.addBindValue(dayOfWeekId)
        sql.addBindValue(time)
        sql.addBindValue(tlcr)
        sql.addBindValue(intensity)
        sql.exec_()

    def insert_street(cityId, streetName):
        sql = QSqlQuery()
        sql.prepare("INSERT INTO Street (cityId, streetName) VALUES (?, ?)")
        sql.addBindValue(cityId)
        sql.addBindValue(streetName)
        sql.exec_()

    def get_or_create_point(coords):
        sql = QSqlQuery()
        sql.prepare("SELECT id FROM Point WHERE x = ? AND y = ?")
        sql.addBindValue(coords[0])
        sql.addBindValue(coords[1])
        sql.exec_()

        if sql.next():
            # Точка вже існує, повертаємо її id
            pointId = sql.value(0)
        else:
            # Створюємо нову точку
            sql.prepare("INSERT INTO Point(x, y) VALUES(?, ?)")
            sql.addBindValue(coords[0])
            sql.addBindValue(coords[1])
            sql.exec_()
            pointId = sql.lastInsertId()
            Database.__db.commit()

        return pointId