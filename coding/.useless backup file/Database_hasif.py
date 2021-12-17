import mysql.connector
from datetime import datetime

"""
    Search Tag:
        INIT & UPDATE CONNECTION
        SEARCH DRIVER
        ADD DRIVER
        ADD ADMIN
        USED BY OTHER FUNCTION
        UNUSED
"""


class Database:
######### INIT & UPDATE CONNECTION #####################################################################################
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
########################################################################################################################
######### SEARCH DRIVER ################################################################################################

    def search_driver(self, search, search_by, search_filter):
        """
        No need to protect from SQL Injection as it only just search

        For Date, the output is not str, but date itself.
            Thus use, datetime.strftime(data[i][indexWithDate], '%d/%m/%Y')
        """
        search_filter = search_filter.lower()
        search = "%" + search + "%"
        student = None
        staff = None
        officer = None
        # Fetch User
        self.db.connect()
        if search_filter == 'all' or search_filter == 'student':
            temp = ""
            if search_by == "name":
                temp = "student." + search_by
            elif search_by == "plate":
                temp = "student.plateNum"
            elif search_by == "id":
                temp = "student.studentID"
            elif search_by == "brand":
                temp = "vehicle.vehBrand"
            elif search_by == "model":
                temp = "vehicle.vehModel"

            # print("Student: ", temp)
            sql = "SELECT * FROM plate_num_rec.student INNER JOIN plate_num_rec.vehicle " \
                  "ON student.plateNum=vehicle.plateNum WHERE " + temp + " LIKE '" + search + "';"
            # val = (temp, search)
            # self.cursor.execute("SELECT * FROM plate_num_rec.vehicle WHERE vehicle.plateNum like '%" + plate_num + "%'")
            self.cursor.execute(sql) # val
            result = self.cursor.fetchall()
            student = result
            # print("Student\n", student)

        if search_filter == 'all' or search_filter == 'staff':
            temp = ""
            if search_by == "name":
                temp = "staff." + search_by
            elif search_by == "plate":
                temp = "staff.plateNum"
            elif search_by == "id":
                temp = "staff.staffID"
            elif search_by == "brand":
                temp = "vehicle.vehBrand"
            elif search_by == "model":
                temp = "vehicle.vehModel"

            # print("Staff: ", temp)
            sql = "SELECT * FROM plate_num_rec.staff INNER JOIN plate_num_rec.vehicle " \
                  "ON staff.plateNum=vehicle.plateNum WHERE " + temp + " LIKE '" + search + "';"
            # val = (temp, search)
            # self.cursor.execute("SELECT * FROM plate_num_rec.vehicle WHERE vehicle.plateNum like '%" + plate_num + "%'")
            self.cursor.execute(sql)  # val
            result = self.cursor.fetchall()
            staff = result
            # print("Staff\n", staff)

        if search_filter == 'all' or search_filter == 'officer':
            temp = ""
            if search_by == "name":
                temp = "officer.officerName"
            elif search_by == "plate":
                temp = "officer.plateNum"
            elif search_by == "id":
                temp = "officer.officerID"
            elif search_by == "brand":
                temp = "vehicle.vehBrand"
            elif search_by == "model":
                temp = "vehicle.vehModel"

            # print("Officer: ", temp)
            sql = "SELECT officerID, officerName, rank, officer.plateNum, vehType, vehBrand, vehModel, roadTaxExpiry " \
                  "FROM plate_num_rec.officer INNER JOIN plate_num_rec.vehicle " \
                  "ON officer.plateNum=vehicle.plateNum WHERE " + temp + " LIKE '" + search + "';"
            # val = (temp, search)
            # self.cursor.execute("SELECT * FROM plate_num_rec.vehicle WHERE vehicle.plateNum like '%" + plate_num + "%'")
            self.cursor.execute(sql)  # val
            result = self.cursor.fetchall()
            officer = result
            # print("Officer\n", officer)

        """
        for car in car_list:
            print(car)
        """
        self.db.close()

        final_result = []
        # data = (role, id, name, year, hostel, vaccineStat, rankOfficer, plateNum, vehType, vehBrand, vehModel, roadTax)
        for each in student:
            temp = ('student', each[0], each[1], each[2], each[3], each[5], None, each[6], each[7], each[8],
                    each[9], each[10])
            final_result.append(temp)

        for each in staff:
            temp = ('staff', each[0], each[1], None, None, each[3], None, each[4], each[5], each[6], each[7], each[8])
            final_result.append(temp)

        for each in officer:
            temp = ('officer', each[0], each[1], None, None, None, each[2], each[3], each[4], each[5], each[6], each[7])
            final_result.append(temp)

        return final_result  # student, staff, officer

########################################################################################################################
######### ADD DRIVER ###################################################################################################

    def insert_staff(self, staff_id, name, vaccination_stats, plate_num, veh_type, veh_brand, veh_model, road_tax):
        self.db.connect()

        staff_id = staff_id.upper()
        name = name.upper()
        plate_num = plate_num.upper()
        vaccination_stats = vaccination_stats

        staff = None
        vehicle = None
        try:  # Fetch User
            status = ""
            self.cursor.execute("SELECT * FROM plate_num_rec.vehicle where plateNum = %s", (plate_num,))
            result = self.cursor.fetchall()
            vehicle = result
        except:
            print("Failed to Fetch Plate Number")

        try:  # Fetch User
            status = ""
            self.cursor.execute("SELECT * FROM plate_num_rec.staff where staffID = %s", (staff_id,))
            result = self.cursor.fetchall()
            staff = result
        except:
            print("Failed to Fetch Student")

        status = None
        if not vehicle:
            road_tax = datetime.strptime(road_tax, '%d/%m/%Y').strftime('%Y-%m-%d')
            if not staff:
                try:
                    sql = "INSERT INTO plate_num_rec.staff " \
                          "(staffID, name, plateNum, vaccinationStatus) VALUES (%s, %s, %s, %s)"
                    val = (staff_id, name, plate_num, vaccination_stats)
                    self.cursor.execute(sql, val)

                    self.db.commit()

                    status = "Staff Successfully Added: \n\tStaff ID\t\t:" + staff_id + \
                             "\n\tName\t: " + name + \
                             "\n\tPlate Number\t: " + plate_num + \
                             "\n\tVaccine Stat\t: " + vaccination_stats
                    print(status)
                except:
                    status = "Staff Failed to Add: \n\tStaff ID\t\t:" + staff_id + \
                             "\n\tName\t: " + name + \
                             "\n\tPlate Number\t: " + plate_num + \
                             "\n\tVaccine Stat\t: " + vaccination_stats
                    print(status)
                    self.db.close()
                    return "Failed...", "Staff Failed to Add"

                self.db.close()
                self.insert_vehicle(plate_num, veh_type, veh_brand, veh_model, road_tax)
                return "Success!", "Staff Successfully Add"
            else:
                if staff[0][2] == "" or not staff[0][2]:
                    try:
                        # sql = "INSERT INTO plate_num_rec.staff " \
                        #       "(staffID, name, plateNum, vaccinationStatus) VALUES (%s, %s, %s, %s)"
                        sql = "UPDATE plate_num_rec.staff SET name = %s, plateNum = %s, " \
                              "vaccinationStatus = %s WHERE staffID = %s;"
                        val = (name, plate_num, vaccination_stats, staff_id)
                        self.cursor.execute(sql, val)

                        self.db.commit()

                        status = "Staff Successfully Updated: \n\tStaff ID\t\t:" + staff_id + \
                                 "\n\tName\t: " + name + \
                                 "\n\tPlate Number\t: " + plate_num + \
                                 "\n\tVaccine Stat\t: " + vaccination_stats
                        print(status)
                    except:
                        status = "Staff Failed to Update: \n\tStaff ID\t\t:" + staff_id + \
                                 "\n\tName\t: " + name + \
                                 "\n\tPlate Number\t: " + plate_num + \
                                 "\n\tVaccine Stat\t: " + vaccination_stats
                        print(status)
                        self.db.close()
                        return "Failed...", "Staff Failed to Add"

                    self.db.close()
                    self.insert_vehicle(plate_num, veh_type, veh_brand, veh_model, road_tax)
                    return "Success!", "Staff Successfully Add"
                else:
                    return "Failed...", "This Staff has already Exist"
        else:
            return "Failed...", "This Plate Number has already Exist"

    def insert_student(self, student_id, name, year, hostel_status, vaccination_stats,
                       plate_num, veh_type, veh_brand, veh_model, road_tax):
        self.db.connect()

        student = None
        vehicle = None
        try:  # Fetch User
            status = ""
            self.cursor.execute("SELECT * FROM plate_num_rec.vehicle where plateNum = %s", (plate_num,))
            result = self.cursor.fetchall()
            vehicle = result
        except:
            print("Failed to Fetch Plate Number")

        try:  # Fetch User
            status = ""
            self.cursor.execute("SELECT * FROM plate_num_rec.student where studentID = %s", (student_id,))
            result = self.cursor.fetchall()
            student = result
        except:
            print("Failed to Fetch Student")

        student_id = student_id.upper()
        name = name.upper()
        hostel_status = hostel_status
        plate_num = plate_num.upper()
        vaccination_stats = vaccination_stats

        if not vehicle:
            if not student:
                road_tax = datetime.strptime(road_tax, '%d/%m/%Y').strftime('%Y-%m-%d')

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
                    return "Failed...", "Student Failed to Add"

                self.db.close()
                self.insert_vehicle(plate_num, veh_type, veh_brand, veh_model, road_tax)
                return "Success!", "Student Successfully Add"
            else:
                return "Failed...", "This Student has already Exist"
        else:
            return "Failed...", "This Plate Number has already Exist"

    def insert_officer(self, officer_id, name, username=None, password=None, rank=None,
                       plate_num=None, veh_type=None, veh_brand=None, veh_model=None, road_tax=None):
        self.db.connect()

        officer_id = officer_id.upper()
        name = name.upper()
        rank = rank

        officer = None
        vehicle = None
        try:  # Fetch User
            status = ""
            self.cursor.execute("SELECT * FROM plate_num_rec.vehicle where plateNum = %s", (plate_num,))
            result = self.cursor.fetchall()
            vehicle = result
        except:
            print("Failed to Fetch Plate Number")
        try:  # Fetch User
            status = ""
            self.cursor.execute("SELECT * FROM plate_num_rec.officer where officer.officerID = %s", (officer_id,))
            result = self.cursor.fetchall()
            officer = result
        except:
            print("Failed to Fetch")

        if plate_num:
            ###### ADD OFFICER (DRIVER) #####
            status = None
            if not vehicle:
                road_tax = datetime.strptime(road_tax, '%d/%m/%Y').strftime('%Y-%m-%d')
                if not officer:
                    try:
                        sql = "INSERT INTO plate_num_rec.officer " \
                              "(officerID, officerName, plateNum) VALUES (%s, %s, %s)"
                        val = (officer_id, name, plate_num)
                        self.cursor.execute(sql, val)

                        self.db.commit()

                        status = "Officer Successfully Added: \n\tOfficer ID\t\t:" + officer_id + \
                                 "\n\tName\t: " + name + \
                                 "\n\tPlate Number\t: " + plate_num
                        print(status)
                    except:
                        status = "Officer Failed to Add: \n\tOfficer ID\t\t:" + officer_id + \
                                 "\n\tName\t: " + name + \
                                 "\n\tPlate Number\t: " + plate_num
                        print(status)
                        self.db.close()
                        return "Failed...", "Officer Failed to Add"

                    self.db.close()
                    self.insert_vehicle(plate_num, veh_type, veh_brand, veh_model, road_tax)
                    return "Success!", "Officer Successfully Add"
                else:
                    print(officer)
                    if officer[0][5] == "" or not officer[0][5]:
                        try:
                            # sql = "INSERT INTO plate_num_rec.officer " \
                            #       "(officerID, name, plateNum, vaccinationStatus) VALUES (%s, %s, %s, %s)"
                            sql = "UPDATE plate_num_rec.officer SET officerName = %s, plateNum = %s " \
                                  "WHERE officerID = %s;"
                            val = (name, plate_num, officer_id)
                            self.cursor.execute(sql, val)

                            self.db.commit()

                            status = "Officer Successfully Updated: \n\tOfficer ID\t\t:" + officer_id + \
                                     "\n\tName\t: " + name + \
                                     "\n\tPlate Number\t: " + plate_num
                            print(status)
                        except:
                            status = "Officer Failed to Update: \n\tOfficer ID\t\t:" + officer_id + \
                                     "\n\tName\t: " + name + \
                                     "\n\tPlate Number\t: " + plate_num
                            print(status)
                            self.db.close()
                            return "Failed...", "Officer Failed to Add"

                        self.db.close()
                        self.insert_vehicle(plate_num, veh_type, veh_brand, veh_model, road_tax)
                        return "Success!", "Officer Successfully Add"
                    else:
                        return "Failed...", "This Officer has already Exist"
            else:
                return "Failed...", "This Plate Number has already Exist"
        else:
            ###### ADD OFFICER (ADMIN) #####
            if officer:
                print(officer)
                status = None
                print("Officer Exist")
                try:
                    sql = "UPDATE plate_num_rec.officer SET officer.officerName = %s, " \
                          "officer.password = %s WHERE officer.officerID = %s;"
                    val = (name, password, officer_id)
                    self.cursor.execute(sql, val)
                    self.db.commit()

                    print("Successfully Update Officer")
                    self.db.close()
                    return "Success!", "Officer Successfully Added!"
                except:
                    status = "Admin Failed to Add: \n\tStaff ID\t:" + officer_id
                    self.db.close()
                    print(status)
                    return "Failed...", "Officer Failed to Add..."
            else:
                status = None
                print("Officer Does Not Exist")
                try:
                    sql = "INSERT INTO plate_num_rec.officer " \
                          "(officerID, officerName, password) VALUES (%s, %s, %s)"
                    val = (officer_id, name, password)
                    self.cursor.execute(sql, val)
                    self.db.commit()

                    status = "Officer Successfully Added: \n\tOfficer ID\t:" + officer_id
                    print(status)
                    self.db.close()
                    return "Success!", "Officer Successfully Added!"
                except:
                    status = "Officer Failed to Add: \n\tOfficer ID\t: " + officer_id
                    self.db.close()
                    print(status)
                    return "Failed...", "Officer Failed to Add..."

########################################################################################################################
######### ADD ADMIN ####################################################################################################

    # All value for these parameters must be in String
    def insert_admin(self, name, staff_id, username=None, password=None):
        # Example
        # sql = "INSERT INTO plate_num_rec.user (id, username, password, privilege, name) VALUES (%s, %s, %s, %s, %s)"
        # val = ('1', 'abu', 'abu', 'admin', 'abu')

        self.db.connect()

        staff_id = staff_id.upper()

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
            print("Staff Exist")
            try:
                sql = "UPDATE plate_num_rec.staff SET staff.name = %s WHERE staff.staffID = %s;"
                val = (name, staff_id)
                self.cursor.execute(sql, val)
                self.db.commit()

                print("Successfully Update Staff")

                sql = "INSERT INTO plate_num_rec.admin " \
                      "(staffID, password) VALUES (%s, %s)"
                val = (staff_id, password)
                self.cursor.execute(sql, val)
                self.db.commit()

                status = "Admin Successfully Added: \n\tStaff ID\t: " + staff_id
                print(status)
                self.db.close()
                return "Success!", "Admin Successfully Added!"
            except:
                status = "Admin Failed to Add: \n\tStaff ID\t:" + staff_id
                self.db.close()
                print(status)
                return "Failed...", "Admin Failed to Add..."
        else:
            status = None
            print("Staff Does Not Exist")
            try:
                sql = "INSERT INTO plate_num_rec.staff " \
                      "(staffID, name) VALUES (%s, %s)"
                val = (staff_id, name)
                self.cursor.execute(sql, val)
                self.db.commit()

                print("Successfully Add Staff")

                sql = "INSERT INTO plate_num_rec.admin " \
                      "(staffID, password) VALUES (%s, %s)"
                val = (staff_id, password)
                self.cursor.execute(sql, val)
                self.db.commit()

                status = "Admin Successfully Added: \n\tStaff ID\t:" + staff_id
                print(status)
                self.db.close()
                return "Success!", "Admin Successfully Added!"
            except:
                status = "Admin Failed to Add: \n\tStaff ID\t: " + staff_id
                self.db.close()
                print(status)
                return "Failed...", "Admin Failed to Add..."

########################################################################################################################
######### USED BY OTHER FUNCTION #######################################################################################

    def insert_vehicle(self, platenum, veh_type, veh_brand, veh_model, roadtaxexp):
        # Example
        # sql = "INSERT INTO plate_num_rec.vehicle (id, username, password, privilege, name) VALUES (%s, %s, %s, %s, %s)"
        # val = ('1', 'abu', 'abu', 'admin', 'abu')
        # Insert New User

        self.db.connect()

        platenum = platenum.upper()
        veh_brand = veh_brand.upper()
        veh_model = veh_model.upper()
        roadtaxexp = roadtaxexp

        status = None
        try:
            sql = "INSERT INTO plate_num_rec.vehicle " \
                  "(plateNum, vehType, vehBrand, vehModel, roadTaxExpiry) VALUES (%s, %s, %s, %s, %s)"
            val = (platenum, veh_type, veh_brand, veh_model, roadtaxexp)
            self.cursor.execute(sql, val)

            self.db.commit()

            status = "Vehicle Successfully Added: \n\tPlate Number:" + platenum + \
                     "\n\tPlate Number\t: " + platenum + \
                     "\n\tVeh Type\t: " + veh_type + \
                     "\n\tCar Brand\t: " + veh_brand + \
                     "\n\tCar Model\t: " + veh_model + \
                     "\n\tRoad Tax Expiry\t: " + roadtaxexp
        except:
            status = "Vehicle Failed to Add: \n\tPlate Number: " + platenum + \
                     "\n\tPlate Number\t: " + platenum + \
                     "\n\tVeh Type\t: " + veh_type + \
                     "\n\tVeh Brand\t: " + veh_brand + \
                     "\n\tveh Model\t: " + veh_model + \
                     "\n\tRoad Tax Expiry\t: " + roadtaxexp

        print(status)

        self.db.close()

########################################################################################################################
######### UNUSED #######################################################################################################

    def login_user(self, staff_id, password):
        # Username is Unique ID
        staff_list = None
        try:
            self.db.reconnect()

            # Fetch User
            self.cursor.execute(
                "SELECT admin.username, admin.password FROM plate_num_rec.admin where admin.staffID = '" +
                staff_id + "'")
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
            print("Staff ID does not Exist")
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
                value = value.upper()
            elif mode == 2:
                mode_name = "name"
            elif mode == 3:
                mode_name = "year"
                val_bef = result[0][3]
            elif mode == 4:
                mode_name = "hostelStatus"
                val_bef = result[0][4]
                value = value
            elif mode == 5:
                mode_name = "plateNum"
                val_bef = result[0][5]
                value = value.upper()
            elif mode == 6:
                mode_name = "vaccinationStatus"
                val_bef = result[0][6]
                value = value

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
                value = value.upper()
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
                value = value

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
                     "\n\tCar Brand\t: " + carbrand
        except:
            if status == "":
                status = "Vehicle Failed to Remove: \n\tPlate Number: " + plate_num + \
                         "\n\tPlate Number\t: " + plate_num + \
                         "\n\tName\t: " + name + \
                         "\n\tCar Brand\t: " + carbrand

        print(status)

########################################################################################################################


# db = Database()
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
    Latest Version
"""
# db.search_driver('a', 'plate', 'all')
# db.insert_vehicle('CAB1234', 'Anqib', 'Pijot', '2022-12-15')
# db.insert_student('B999999999', 'ABC', 2, 'Campus', '2 Dose', 'CAB1234', 'Yamaha', '2022-12-15')
# db.insert_staff('B23456789', 'CBA', "Lecturer", "CBA1234", "2 dose", "Proton", "2022-12-15")
# db.insert_admin('abc', '123456789', '123', '123')
# db.insert_officer('1234', 'abc', '123', '123', 'abc')
# db.insert_officer('4321', 'cba', '123', '123', 'cba', 'AAA1111', 'Bike', 'Yamaha', 'R15', '2022-12-15')
