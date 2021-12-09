import mysql.connector


class Database:
    def __init__(self, host=None, user=None, password=None):
        self.db = None
        if not host:
            self.host = "localhost"
        else:
            self.host = host
        if not user:
            self.user = "root"
        else:
            self.user = user
        if not password:
            self.password = None
        else:
            self.password = password

        try:
            if not self.password:
                self.db = mysql.connector.connect(
                    host=self.host,
                    user=self.user
                )
            else:
                self.db = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password
                )
            self.db.connect()
            self.cursor = self.db.cursor()
            status = str(self.db)
            print("Successfully Connect: ", status)

            self.db.close()
        except:
            status = str(self.db)
            print("Failed to Connect: ", status)

    """
    def __init__(self, host, user, password):
        try:
            self.db = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )
            self.connection = True
            self.cursor = self.db.cursor()
            self.connection_result()
        except:
            self.connection = False
            print("Failed to Connect")
    """

    def update_connection(self, host=None, user=None, password=None):
        try:
            self.db.close()
            self.db = None
        except:
            self.db = None

        if not host:
            self.host = "localhost"
        else:
            self.host = host
        if not user:
            self.user = "root"
        else:
            self.user = user
        if not password:
            self.password = None
        else:
            self.password = password

        try:
            if not self.password:
                self.db = mysql.connector.connect(
                    host=self.host,
                    user=self.user
                )
            else:
                self.db = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password
                )
            self.db.connect()
            self.cursor = self.db.cursor()
            status = str(self.db)
            print("Successfully Connect: ", status)
            self.db.close()
            return True
        except:
            status = str(self.db)
            print("Failed to Connect: ", status)
            return False

    """
    def connection_result(self):
        status = str(self.db)
        status = status.split(" object at ")[0].replace("<", "")
        if status == "mysql.connector.connection_cext.CMySQLConnection":
            print("Successfully Connect")
        else:
            print("Failed to Connect: ", status)
    """

    # All value for these parameters must be in String
    def insert_admin(self, staff_id, username, password):
        # Example
        # sql = "INSERT INTO plate_num_rec.user (id, username, password, privilege, name) VALUES (%s, %s, %s, %s, %s)"
        # val = ('1', 'abu', 'abu', 'admin', 'abu')

        self.db.connect()

        staff_id = staff_id.lower()
        username = username.lower()

        staff = None
        try:  # Fetch User
            status = ""
            self.cursor.execute("SELECT * FROM plate_num_rec.staff where staffID = %s", (staff_id,))
            result = self.cursor.fetchall()
            staff = result
        except:
            print("Failed to Fetch")

        if staff:
            status = None
            try:
                sql = "INSERT INTO plate_num_rec.admin " \
                      "(staffID, username, password) VALUES (%s, %s, %s)"
                val = (staff_id, username, password)
                self.cursor.execute(sql, val)

                self.db.commit()

                status = "Admin Successfully Added: \n\tStaff ID\t:" + staff_id + \
                         "\n\tUsername\t: " + username
            except:
                status = "Admin Failed to Add: \n\tStaff ID\t:" + staff_id + \
                         "\n\tUsername\t: " + username

            print(status)
        else:
            print("This Staff ID does not Exist. Unable to Insert New Admin")

        self.db.close()

    def login_user(self, username, password):
        # Username is Unique ID
        staff_list = None
        try:
            self.db.reconnect()

            username = username.lower()

            # Fetch User
            self.cursor.execute(
                "SELECT admin.username, admin.password FROM plate_num_rec.admin where admin.username = '" +
                username + "'")
            result = self.cursor.fetchall()
            staff_list = result
        except:
            msg = "Failed to Connect"
            return False, msg

        if staff_list:
            for staff in staff_list:
                print(staff)
            return staff_list[0]
        else:
            print("Username does not Exist")
            return

    """
    def select_user(self):
        # Fetch User
        self.cursor.execute("SELECT * FROM plate_num_rec.user")
        result = self.cursor.fetchall()
        staff_list = result

        for staff in staff_list:
            print(staff)
    """

    def select_user(self, username):
        username = username.lower()

        # Fetch User
        self.cursor.execute("SELECT * FROM plate_num_rec.user where user.username like '%" + username + "%'")
        result = self.cursor.fetchall()
        staff_list = result

        if staff_list:
            # for staff in staff_list:
            #     print(staff)
            return staff_list
        else:
            print("Username does not Exist")
            return

    def edit_student(self, id, value, mode):
        status = ""
        mode_name = ""
        sql = ""
        val = ""
        val_bef = ""

        # Fetch User
        status = ""
        self.cursor.execute("SELECT * FROM plate_num_rec.student where student.studentID = '" + str(id) + "'")
        result = self.cursor.fetchall()

        if result:
            if mode == 1:
                mode_name = "studentID"
                val_bef = result[0][1]
                value = value.lower()
            elif mode == 2:
                mode_name = "name"
            elif mode == 3:
                mode_name = "year"
                val_bef = result[0][3]
            elif mode == 4:
                mode_name = "hostelStatus"
                val_bef = result[0][4]
                value = value.lower()
            elif mode == 5:
                mode_name = "plateNum"
                val_bef = result[0][5]
                value = value.lower()
            elif mode == 6:
                mode_name = "vaccinationStatus"
                val_bef = result[0][6]
                value = value.lower()

            try:
                sql = "UPDATE plate_num_rec.student SET student." + mode_name.lower() + " = %s WHERE student.studentID = %s;"
                val = (value, id)
                self.cursor.execute(sql, val)

                self.db.commit()

                if mode != 2:
                    status = "User Successfully Edit: \n\tChanges has made:\n\t\t" + \
                             mode_name + "\t: " + val_bef + " -> " + value
                else:
                    status = "User Successfully Edit: \n\tChanges has made: Password"
            except:
                if mode != 2:
                    status = "User Failed to Edit: \n\tChanges to make:\n\t\t" + \
                             mode_name + "\t: " + val_bef + " -/> " + value
                else:
                    status = "User Successfully Edit: \n\tChanges has made: Password"
        else:
            status = "ID does not Exist"

        print(status)

    def remove_student(self, id):
        status = ""
        # Fetch User
        try:
            self.cursor.execute("SELECT * FROM plate_num_rec.student where studentID = '" + str(id) + "'")
            result = self.cursor.fetchall()
            student = result

            studentid = student[0][1]
            name = student[0][2]
            year = student[0][3]
            hostelstatus = student[0][4]
            platenum = student[0][5]
            vacstatus = student[0][6]

        except:
            status = "Student ID " + str(id) + " Does Not Exist"

        # Remove User
        try:
            self.cursor.execute("DELETE FROM plate_num_rec.student WHERE studentID = '" + str(id) + "'")

            self.db.commit()
            status = "User Successfully Removed: \n\tID\t\t\t: " + str(id) + \
                     "\n\tStudentID\t\t: " + studentid + \
                     "\n\tName\t: " + name + \
                     "\n\tYear\t: " + year + \
                     "\n\tHostel Status\t: " + hostelstatus + \
                     "\n\tPlate Num\t: " + platenum + \
                     "\n\tVax Status\t: " + vacstatus

        except:
            if status == "":
                status = "User Failed to Remove: \n\tID\t\t\t: " + str(id) + \
                         "\n\tStudentID\t\t: " + studentid + \
                         "\n\tName\t: " + name + \
                         "\n\tYear\t: " + year + \
                         "\n\tHostel Status\t: " + hostelstatus + \
                         "\n\tPlate Num\t: " + platenum + \
                         "\n\tVax Staus\t: " + vacstatus

        print(status)

    def insert_vehicle(self, platenum, name, carbrand, roadtaxexp):
        # Example
        # sql = "INSERT INTO plate_num_rec.vehicle (id, username, password, privilege, name) VALUES (%s, %s, %s, %s, %s)"
        # val = ('1', 'abu', 'abu', 'admin', 'abu')
        # Insert New User

        self.db.connect()

        platenum = platenum.upper()
        name = name.lower()
        carbrand = carbrand.lower()
        roadtaxexp = roadtaxexp.lower()

        status = None
        try:
            sql = "INSERT INTO plate_num_rec.vehicle " \
                  "(plateNum, name, carBrand, roadTaxExpiry) VALUES (%s, %s, %s, %s)"
            val = (platenum, name, carbrand, roadtaxexp)
            self.cursor.execute(sql, val)

            self.db.commit()

            status = "Vehicle Successfully Added: \n\tPlate Number:" + platenum + \
                     "\n\tPlate Number\t: " + platenum + \
                     "\n\tName\t: " + name + \
                     "\n\tCar Brand\t: " + carbrand + \
                     "\n\tRoad Tax Expiry\t: " + roadtaxexp
        except:
            status = "Vehicle Failed to Add: \n\tPlate Number: " + platenum + \
                     "\n\tPlate Number\t: " + platenum + \
                     "\n\tName\t: " + name + \
                     "\n\tCar Brand\t: " + carbrand + \
                     "\n\tRoad Tax Expiry\t: " + roadtaxexp

        print(status)

        self.db.close()

    def select_vehicle(self, plate_num):
        plate_num = plate_num.upper()
        # Fetch User
        self.cursor.execute("SELECT * FROM plate_num_rec.vehicle WHERE vehicle.plateNum like '%" + plate_num + "%'")
        result = self.cursor.fetchall()
        car_list = result

        for car in car_list:
            print(car)

        return car_list

    def edit_vehicle(self, plate_num, value, mode):
        status = ""
        mode_name = ""
        db_name = ""
        sql = ""
        val = ""
        val_bef = ""

        # Fetch User
        status = ""
        self.cursor.execute("SELECT * FROM plate_num_rec.vehicle where vehicle.plateNum = '" + plate_num + "'")
        result = self.cursor.fetchall()

        if result:
            if mode == 1:
                mode_name = "Plate Number"
                db_name = "plateNum"
                val_bef = result[0][1]
                value = value.lower()
            elif mode == 2:
                mode_name = "Name"
                db_name = "name"
                val_bef = result[0][2]
            elif mode == 3:
                mode_name = "Car Brand"
                db_name = "carBrand"
                val_bef = result[0][3]
                value = value.upper()
            elif mode == 4:
                mode_name = "Road Tax Expiry"
                db_name = "roadTaxExpiry"
                val_bef = result[0][4]
                value = value.lower()

            try:
                sql = "UPDATE plate_num_rec.vehicle SET vehicle." + db_name + " = %s WHERE vehicle.plateNum = %s;"
                val = (value, plate_num)
                self.cursor.execute(sql, val)

                self.db.commit()

                status = "User Successfully Edit: \n\tChanges has made:\n\t\t" + \
                         mode_name + "\t: " + val_bef + " -> " + value
            except:
                status = "User Failed to Edit: \n\tChanges to make:\n\t\t" + \
                         mode_name + "\t: " + val_bef + " -/> " + value
        else:
            status = "Plate Number does not Exist"

        print(status)

    def remove_vehicle(self, plate_num):
        plate_num = plate_num.upper()

        status = ""
        # Fetch User
        try:
            self.cursor.execute("SELECT * FROM plate_num_rec.vehicle where plateNum = '" + plate_num + "'")
            result = self.cursor.fetchall()
            car = result

            plate_num = car[0][1]
            name = car[0][2]
            carbrand = car[0][3]
            roadtaxexpiry = car[0][4]

        except:
            status = "Plate Number " + plate_num + " Does Not Exist"

        # Remove User
        try:
            self.cursor.execute("DELETE FROM plate_num_rec.vehicle WHERE plateNum = '" + plate_num + "'")

            self.db.commit()
            status = "Vehicle Successfully Removed: \n\tPlate Number: " + plate_num + \
                     "\n\tPlate Number\t: " + plate_num + \
                     "\n\tName\t: " + name + \
                     "\n\tCar Brand\t: " + carbrand + \
                     "\n\tRoad Tax Expiry\t: " + roadtaxexp
        except:
            if status == "":
                status = "VehicleFailed to Remove: \n\tPlate Number: " + plate_num + \
                         "\n\tPlate Number\t: " + plate_num + \
                         "\n\tName\t: " + name + \
                         "\n\tCar Brand\t: " + carbrand + \
                         "\n\tRoad Tax Expiry\t: " + roadtaxexp

        print(status)

    def insert_staff(self, staff_id, name, stats, plate_num, vaccination_stats, veh_brand, road_tax):
        self.db.connect()

        staff_id = staff_id.lower()
        name = name.lower()
        stats = stats.lower()
        plate_num = plate_num.lower()
        vaccination_stats = vaccination_stats.lower()

        status = None
        try:
            sql = "INSERT INTO plate_num_rec.staff " \
                  "(staffID, name, status, plateNum, vaccinationStatus) VALUES (%s, %s, %s, %s, %s)"
            val = (staff_id, name, stats, plate_num, vaccination_stats)
            self.cursor.execute(sql, val)

            self.db.commit()

            status = "Staff Successfully Added: \n\tStaff ID\t\t:" + str(staff_id) + \
                     "\n\tStaff ID\t\t\t: " + staff_id + \
                     "\n\tName\t: " + name + \
                     "\n\tStatus\t: " + stats + \
                     "\n\tPlate Number\t: " + plate_num + \
                     "\n\tVaccine Stat\t: " + vaccination_stats
            print(status)
        except:
            status = "Staff Failed to Add: \n\tStaff ID\t\t:" + staff_id + \
                     "\n\tStaff ID\t\t\t: " + staff_id + \
                     "\n\tName\t: " + name + \
                     "\n\tStatus\t: " + stats + \
                     "\n\tPlate Number\t: " + plate_num + \
                     "\n\tVaccine Stat\t: " + vaccination_stats
            print(status)
            self.db.close()
            return

        self.db.close()
        self.insert_vehicle(plate_num, name, veh_brand, road_tax)

    def insert_student(self, student_id, name, year, hostel_status, vaccination_stats,
                       plate_num, veh_brand, road_tax):
        self.db.connect()

        student_id = student_id.lower()
        name = name.lower()
        hostel_status = hostel_status.lower()
        plate_num = plate_num.lower()
        vaccination_stats = vaccination_stats.lower()

        status = None
        try:
            sql = "INSERT INTO plate_num_rec.student " \
                  "(studentID, name, year, hostelStatus, plateNum, vaccinationStatus) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (student_id, name, year, hostel_status, plate_num, vaccination_stats)
            self.cursor.execute(sql, val)

            self.db.commit()

            status = "Student Successfully Added: \n\tStudent ID\t\t:" + student_id + \
                     "\n\tName\t\t\t: " + name + \
                     "\n\tYear\t\t\t: " + str(year) + \
                     "\n\tHostel Stat\t\t: " + hostel_status + \
                     "\n\tPlate Number\t: " + plate_num + \
                     "\n\tVaccine Stat\t: " + vaccination_stats
            print(status)
        except:
            status = "Student Failed to Add: \n\tStudent ID\t:" + student_id + \
                     "\n\tName\t\t\t: " + name + \
                     "\n\tYear\t\t\t: " + str(year) + \
                     "\n\tHostel Stat\t\t: " + hostel_status + \
                     "\n\tPlate Number\t: " + plate_num + \
                     "\n\tVaccine Stat\t: " + vaccination_stats
            print(status)
            self.db.close()
            return

        self.db.close()
        self.insert_vehicle(plate_num, name, veh_brand, road_tax)

    def insert_officer(self, officer_id, name, username, password, rank,
                       plate_num=None, veh_type=None, veh_brand=None, veh_model=None, road_tax=None):
        self.db.connect()

        officer_id = officer_id.lower()
        name = name.lower()
        username = username.lower()
        rank = rank.lower()
        if plate_num:
            plate_num = plate_num.lower()

        status = None
        try:
            sql = None
            val = None

            if plate_num:
                sql = "INSERT INTO plate_num_rec.officer " \
                      "(officerID, officerName, username, password, rank, plateNum) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (officer_id, name, username, password, rank, plate_num)
            else:
                sql = "INSERT INTO plate_num_rec.officer " \
                      "(officerID, officerName, username, password, rank) VALUES (%s, %s, %s, %s, %s)"
                val = (officer_id, name, username, password, rank)

            self.cursor.execute(sql, val)
            self.db.commit()

            status = "Officer Successfully Added: \n\tOfficer ID\t\t:" + officer_id + \
                     "\n\tName\t\t\t: " + name + \
                     "\n\tUsername\t\t: " + username + \
                     "\n\tRank\t\t\t: " + rank
            if plate_num:
                status = status + "\n\tPlate Number\t: " + plate_num
            print(status)
        except:
            status = "Officer Failed to Add: \n\tOfficer ID\t\t:" + officer_id + \
                     "\n\tName\t\t\t: " + name + \
                     "\n\tUsername\t\t: " + username + \
                     "\n\tRank\t\t\t: " + rank
            if plate_num:
                status = status + "\n\tPlate Number\t: " + plate_num
            print(status)
            self.db.close()
            return

        self.db.close()
        if plate_num:
            self.insert_vehicle(plate_num, veh_type, veh_brand, veh_model, road_tax)


db = Database()
# for i in range(0,1000):
#     db.update_connection()
# db.connect()

"""
    Older Version
"""
# db.insert_user('bulat 3', 'bakar', 'admin', 'ali')
# db.select_user("ali")
# db.edit_user(2, "ali", 4)
# db.remove_user(2)
# db.insert_car_owner('ABC1234', 'chin', 'student', 'b1234', 'cheng', 'hanji')
# db.select_car_owner("ABC1234")
# db.edit_car_owner("ABC1234", "Chin", 1)
# db.remove_car_owner("ABC1234")

"""
    Latest Update
"""
db.insert_vehicle('CAB1234', 'Anqib', 'Pijot', '2022-12-15')
# db.insert_student('B999999999', 'ABC', 2, 'Campus', '2 Dose', 'CAB1234', 'Yamaha', '2022-12-15')
# db.insert_staff('B23456789', 'CBA', "Lecturer", "CBA1234", "2 dose", "Proton", "2022-12-15")
# db.insert_admin('123456789', '123', '123')
# db.insert_officer('1234', 'abc', '123', '123', 'abc')
# db.insert_officer('4321', 'cba', '123', '123', 'cba', 'AAA1111', 'Bike', 'Yamaha', 'R15', '2022-12-15')
