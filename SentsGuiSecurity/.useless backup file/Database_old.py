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
            self.cursor.execute("SELECT * FROM plate_num_rec.staff where staffID = %s", (staff_id, ))
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
            self.cursor.execute("SELECT user.username, user.password FROM plate_num_rec.user where user.username = '" +
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

        """
        # rangeloop = [1, 2, 3, 4, 5]
        staff_array = []
        if staff_list:
            nom = 0
            nom2 = 0
            for staff in staff_list:
                for i in range(0, 5):
                    staff_temp = staff
                    nom += 1
                staff_array.append(staff_temp)
                nom += 1
            # print("Test new array = ",staff_array)
            return staff_array
        else:
            print("Username does not Exist")
            return
        """

    def edit_user(self, id, value, mode):
        status = ""
        mode_name = ""
        sql = ""
        val = ""
        val_bef = ""

        # Fetch User
        status = ""
        self.cursor.execute("SELECT * FROM plate_num_rec.user where user.id = '" + str(id) + "'")
        result = self.cursor.fetchall()

        if result:
            if mode == 1:
                mode_name = "Username"
                val_bef = result[0][1]
                value = value.lower()
            elif mode == 2:
                mode_name = "Password"
            elif mode == 3:
                mode_name = "Privilege"
                val_bef = result[0][3]
            elif mode == 4:
                mode_name = "Name"
                val_bef = result[0][4]
                value = value.lower()

            try:
                sql = "UPDATE plate_num_rec.user SET user." + mode_name.lower() + " = %s WHERE user.id = %s;"
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

    def remove_user(self, id):
        status = ""
        # Fetch User
        try:
            self.cursor.execute("SELECT * FROM plate_num_rec.user where id = '" + str(id) + "'")
            result = self.cursor.fetchall()
            staff = result

            username = staff[0][1]
            privilege = staff[0][3]
            name = staff[0][4]
        except:
            status = "User ID " + str(id) + " Does Not Exist"

        # Remove User
        try:
            self.cursor.execute("DELETE FROM plate_num_rec.user WHERE id = '" + str(id) + "'")

            self.db.commit()
            status = "User Successfully Removed: \n\tID\t\t\t: " + str(id) + \
                     "\n\tName\t\t: " + name + \
                     "\n\tUsername\t: " + username + \
                     "\n\tPrivilege\t: " + privilege
        except:
            if status == "":
                status = "User Failed to Remove: \n\tID\t\t\t: " + str(id) + \
                         "\n\tName\t\t: " + name + \
                         "\n\tUsername\t: " + username + \
                         "\n\tPrivilege\t: " + privilege

        print(status)

    def insert_vehicle(self, plate_num, veh_type, veh_brand, veh_model, road_tax_exp):
        # Example
        # sql = "INSERT INTO plate_num_rec.user (id, username, password, privilege, name) VALUES (%s, %s, %s, %s, %s)"
        # val = ('1', 'abu', 'abu', 'admin', 'abu')
        # Insert New User

        self.db.connect()

        plate_num = plate_num.upper()
        veh_type = veh_type.lower()
        veh_brand = veh_brand.lower()
        veh_model = veh_model.lower()
        road_tax_exp = road_tax_exp.lower()

        status = None
        try:
            sql = "INSERT INTO plate_num_rec.vehicle " \
                  "(plateNum, vehType, vehBrand, vehModel, roadTaxExpiry) VALUES (%s, %s, %s, %s, %s)"
            val = (plate_num, veh_type, veh_brand, veh_model, road_tax_exp)
            self.cursor.execute(sql, val)

            self.db.commit()

            status = "Vehicle Successfully Added: \n\tPlate Number:" + plate_num + \
                     "\n\tVeh Type\t: " + veh_type + \
                     "\n\tVeh Brand\t: " + veh_brand + \
                     "\n\tVeh Model\t: " + veh_model + \
                     "\n\tRoad Tax\t: " + road_tax_exp
        except:
            status = "Vehicle Failed to Add: \n\tPlate Number: " + plate_num + \
                     "\n\tVeh Type\t: " + veh_type + \
                     "\n\tVeh Brand\t: " + veh_brand + \
                     "\n\tVeh Model\t: " + veh_model + \
                     "\n\tRoad Tax\t: " + road_tax_exp

        print(status)

        self.db.close()

    def select_vehicle(self, plate_num):
        plate_num = plate_num.upper()
        # Fetch User
        self.cursor.execute("SELECT * FROM plate_num_rec.vehicle WHERE car_owner.plateNum like '%" + plate_num + "%'")
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
        self.cursor.execute("SELECT * FROM plate_num_rec.car_owner where car_owner.plateNum = '" + plate_num + "'")
        result = self.cursor.fetchall()

        if result:
            if mode == 1:
                mode_name = "Name"
                db_name = "ownerName"
                val_bef = result[0][1]
                value = value.lower()
            elif mode == 2:
                mode_name = "Status"
                db_name = "ownerStatus"
                val_bef = result[0][2]
            elif mode == 3:
                mode_name = "ID"
                db_name = "statusId"
                val_bef = result[0][3]
                value = value.upper()
            elif mode == 4:
                mode_name = "Car Brand"
                db_name = "carBrand"
                val_bef = result[0][4]
                value = value.lower()
            elif mode == 5:
                mode_name = "Car Model"
                db_name = "carModel"
                val_bef = result[0][5]
                value = value.lower()

            try:
                sql = "UPDATE plate_num_rec.car_owner SET car_owner." + db_name + " = %s WHERE car_owner.plateNum = %s;"
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
            self.cursor.execute("SELECT * FROM plate_num_rec.car_owner where plateNum = '" + plate_num + "'")
            result = self.cursor.fetchall()
            car = result

            name = car[0][1]
            owner_status = car[0][2]
            id = car[0][3]
            car_brand = car[0][4]
            car_model = car[0][5]
        except:
            status = "Plate Number " + plate_num + " Does Not Exist"

        # Remove User
        try:
            self.cursor.execute("DELETE FROM plate_num_rec.car_owner WHERE plateNum = '" + plate_num + "'")

            self.db.commit()
            status = "Car OWner Successfully Removed: \n\tPlate Number: " + plate_num + \
                     "\n\tName\t\t: " + name + \
                     "\n\tStatus\t\t: " + owner_status + \
                     "\n\tID\t\t\t: " + id + \
                     "\n\tCar Brand\t: " + car_brand + \
                     "\n\tCar Brand\t: " + car_model
        except:
            if status == "":
                status = "Car OWner Failed to Remove: \n\tPlate Number: " + plate_num + \
                         "\n\tName\t\t: " + name + \
                         "\n\tStatus\t\t: " + owner_status + \
                         "\n\tID\t\t\t: " + id + \
                         "\n\tCar Brand\t: " + car_brand + \
                         "\n\tCar Brand\t: " + car_model

        print(status)

    def insert_staff(self, staff_id, name, vaccination_stats,
                       plate_num, veh_type, veh_brand, veh_model, road_tax):
        self.db.connect()

        staff_id = staff_id.lower()
        name = name.lower()
        plate_num = plate_num.lower()
        vaccination_stats = vaccination_stats.lower()

        status = None
        try:
            sql = "INSERT INTO plate_num_rec.staff " \
                  "(staffID, name, plateNum, vaccinationStatus) VALUES (%s, %s, %s, %s)"
            val = (staff_id, name, plate_num, vaccination_stats)
            self.cursor.execute(sql, val)

            self.db.commit()

            status = "Staff Successfully Added: \n\tStaff ID\t\t:" + staff_id + \
                     "\n\tName\t\t\t: " + name + \
                     "\n\tPlate Number\t: " + plate_num + \
                     "\n\tVaccine Stat\t: " + vaccination_stats
            print(status)
        except:
            status = "Staff Failed to Add: \n\tStaff ID\t\t:" + staff_id + \
                     "\n\tName\t\t\t: " + name + \
                     "\n\tPlate Number\t: " + plate_num + \
                     "\n\tVaccine Stat\t: " + vaccination_stats
            print(status)
            self.db.close()
            return

        self.db.close()
        self.insert_vehicle(plate_num, veh_type, veh_brand, veh_model, road_tax)

    def insert_student(self, student_id, name, year, hostel_status, vaccination_stats,
                       plate_num, veh_type, veh_brand, veh_model, road_tax):
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
        self.insert_vehicle(plate_num, veh_type, veh_brand, veh_model, road_tax)

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
# db.insert_vehicle('CAB1234', 'Bike', 'Yamaha', 'Y15', '2022-12-15')
# db.insert_student('B999999999', 'ABC', 2, 'Campus', '2 Dose', 'CAB1234', 'Bike', 'Yamaha', 'Y15', '2022-12-15')
# db.insert_staff('123456789', 'CBA', '2 Dose', 'CBA1234', 'Car', 'Proton', 'Saga', '2022-12-15')
# db.insert_admin('123456789', '123', '123')
# db.insert_officer('1234', 'abc', '123', '123', 'abc')
# db.insert_officer('4321', 'cba', '123', '123', 'cba', 'AAA1111', 'Bike', 'Yamaha', 'R15', '2022-12-15')
