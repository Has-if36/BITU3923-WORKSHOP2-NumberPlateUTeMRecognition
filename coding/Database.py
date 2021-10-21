import mysql.connector


class Database:
    def __init__(self):
        try:
            self.db = mysql.connector.connect(
                ### default ###
                host = "localhost",
                user = "root"
            )
            self.connection = True
            self.cursor = self.db.cursor()
            self.connection_result()
        except:
            self.connection = False
            print("Failed to Connect")

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

    def connection_result(self):
        status = str(self.db)
        status = status.split(" object at ")[0].replace("<", "")
        if status == "mysql.connector.connection_cext.CMySQLConnection":
            print("Successfully Connect")
        else:
            print("Failed to Connect")

    # All value for these parameters must be in String
    def insert_user(self, username, password, privilege, name):
        # Example
        # sql = "INSERT INTO plate_num_rec.user (id, username, password, privilege, name) VALUES (%s, %s, %s, %s, %s)"
        # val = ('1', 'abu', 'abu', 'admin', 'abu')

        username = username.lower()
        name = name.lower()

        # Fetch User
        status = ""
        self.cursor.execute("SELECT * FROM plate_num_rec.user")
        result = self.cursor.fetchall()
        id_list = result

        # Scan User & Increment ID
        id = 0
        for i in range(0, len(id_list)):
            id = i + 1
            if (i + 1) != id_list[i][0]:
                break
            if username == id_list[i][1]:
                status = "User Failed to Add: This Username has already exist"

        if len(id_list) == id:
            id = id + 1

        if status == "User Failed to Add: This Username has already exist":
            pass
        else:
            # Insert New User
            try:
                sql = "INSERT INTO plate_num_rec.user (id, username, password, privilege, name) " \
                      "VALUES (%s, %s, %s, %s, %s)"
                val = (id, username, password, privilege, name)
                self.cursor.execute(sql, val)

                self.db.commit()

                status = "User Successfully Added: \n\tID\t\t\t: " + str(id) + \
                         "\n\tName\t\t: " + name + \
                         "\n\tUsername\t: " + username + \
                         "\n\tPrivilege\t: " + privilege
            except:
                status = "User Failed to Add: \n\tID " + str(id) + \
                         "\n\tName\t: " + name + \
                         "\n\tUsername\t: " + username + \
                         "\n\tPrivilege\t: " + privilege

        print(status)

    def select_user(self):
        # Fetch User
        self.cursor.execute("SELECT * FROM plate_num_rec.user")
        result = self.cursor.fetchall()
        staff_list = result

        for staff in staff_list:
            print(staff)

    def select_user(self, username):
        username = username.lower()

        # Fetch User
        self.cursor.execute("SELECT * FROM plate_num_rec.user where user.username = '" + username + "'")
        result = self.cursor.fetchall()
        staff_list = result

        if staff_list:
            for staff in staff_list:
                print(staff)
            return staff_list[0]
        else:
            print("Username does not Exist")
            return

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

    def insert_car_owner(self, plate_num, owner_name, owner_status, id, car_brand, car_model):
        # Example
        # sql = "INSERT INTO plate_num_rec.user (id, username, password, privilege, name) VALUES (%s, %s, %s, %s, %s)"
        # val = ('1', 'abu', 'abu', 'admin', 'abu')
        # Insert New User

        plate_num = plate_num.upper()
        owner_name = owner_name.lower()
        id = id.upper()
        car_brand = car_brand.lower()
        car_model = car_model.lower()

        status = None
        try:
            sql = "INSERT INTO plate_num_rec.car_owner " \
                  "(plateNum, ownerName, ownerStatus, statusId, carBrand, carModel) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (plate_num, owner_name, owner_status, id, car_brand, car_model)
            self.cursor.execute(sql, val)

            self.db.commit()

            status = "Car Owner Successfully Added: \n\tPlate Number:" + plate_num + \
                     "\n\tName\t\t: " + owner_name + \
                     "\n\tStatus\t\t: " + owner_status + \
                     "\n\tID\t\t\t: " + id + \
                     "\n\tCar Brand\t: " + car_brand + \
                     "\n\tCar Model\t: " + car_model
        except:
            status = "Car Owner Failed to Add: \n\tPlate Number: " + plate_num + \
                     "\n\tName\t\t: " + owner_name + \
                     "\n\tStatus\t\t: " + owner_status + \
                     "\n\tID\t\t\t: " + id + \
                     "\n\tCar Brand\t: " + car_brand + \
                     "\n\tCar Model\t: " + car_model

        print(status)

    def select_car_owner(self, plate_num):
        plate_num = plate_num.upper()
        # Fetch User
        self.cursor.execute("SELECT * FROM plate_num_rec.car_owner WHERE car_owner.plateNum = '" + plate_num + "'")
        result = self.cursor.fetchall()
        car_list = result

        for car in car_list:
            print(car)

    def edit_car_owner(self, plate_num, value, mode):
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

    def remove_car_owner(self, plate_num):
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


db = Database("localhost", "pnrAdmin", "pnrAdmin")
# db.insert_user('abu', 'bakar', 'admin', 'ali')
# db.select_user("ali")
# db.edit_user(2, "ali", 4)
# db.remove_user(2)
# db.insert_car_owner('ABC1234', 'chin', 'student', 'b1234', 'cheng', 'hanji')
# db.select_car_owner("ABC1234")
# db.edit_car_owner("ABC1234", "Chin", 1)
# db.remove_car_owner("ABC1234")
