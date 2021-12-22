import os
import shutil
import ftplib
import zipfile
import mysql.connector
from datetime import datetime

"""
    Search Tag:
        INIT & UPDATE CONNECTION
        SEARCH DRIVER
        SEARCH ADMIN
        ADD DRIVER
        ADD ADMIN
        USED BY OTHER FUNCTION
        OTHERS
        UNUSED
"""


class MySQL:
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

    def connect_sql(self):
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
        print(search_filter)
        # Fetch User
        self.connect_sql()
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
            self.cursor.execute(sql)  # val
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
        if student:
            for each in student:
                temp = ('student', each[0], each[1], each[2], each[3], each[5], None, each[6], each[7], each[8],
                        each[9], each[10])
                final_result.append(temp)

        if staff:
            for each in staff:
                temp = ('staff', each[0], each[1], None, None, each[3], None, each[4], each[5], each[6], each[7], each[8])
                final_result.append(temp)

        if officer:
            for each in officer:
                temp = ('officer', each[0], each[1], None, None, None, each[2], each[3], each[4], each[5], each[6], each[7])
                final_result.append(temp)

        return final_result  # student, staff, officer

    ########################################################################################################################
    ######### SEARCH ADMIN #################################################################################################

    def search_admin(self, search, search_by, search_filter):
        """
            No need to protect from SQL Injection as it only just search
        """
        search_filter = search_filter.lower()
        search = "%" + search + "%"
        student = None
        staff = None
        officer = None
        # Fetch User
        self.connect_sql()
        self.db.connect()
        if search_filter == 'all' or search_filter == 'staff':
            temp = ""
            if search_by == "name":
                temp = "staff." + search_by
            elif search_by == "id":
                temp = "staff.staffID"

            # print("Staff: ", temp)
            sql = "SELECT staff.staffID, staff.name FROM plate_num_rec.staff INNER JOIN " \
                  "(SELECT admin.staffID FROM plate_num_rec.admin) AS b " \
                  "ON staff.staffID=b.staffID WHERE " + temp + " LIKE '" + search + "';"
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
            elif search_by == "id":
                temp = "officer.officerID"

            # print("Officer: ", temp)
            sql = "SELECT officerID, officerName FROM plate_num_rec.officer WHERE " \
                  + temp + " LIKE '" + search + "' and officer.password IS NOT NULL;"
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
        # data = (role, staffID, name)
        for each in staff:
            temp = ('staff', each[0], each[1])
            final_result.append(temp)

        for each in officer:
            temp = ('officer', each[0], each[1])
            final_result.append(temp)


        return final_result  # student, staff, officer

    ########################################################################################################################
    ######### ADD DRIVER ###################################################################################################

    def insert_staff(self, staff_id, name, vaccination_stats, plate_num, veh_type, veh_brand, veh_model, road_tax):
        self.connect_sql()
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
                    self.db.close()
                    return "Failed...", "This Staff has already Exist"
        else:
            self.db.close()
            return "Failed...", "This Plate Number has already Exist"

    def insert_student(self, student_id, name, year, hostel_status, vaccination_stats,
                       plate_num, veh_type, veh_brand, veh_model, road_tax):
        self.connect_sql()
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
                          "(studentID, name, year, hostelStatus, plateNum, vaccinationStatus) " \
                          "VALUES (%s, %s, %s, %s, %s, %s)"
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
                self.db.close()
                return "Failed...", "This Student has already Exist"
        else:
            self.db.close()
            return "Failed...", "This Plate Number has already Exist"

    def insert_officer(self, officer_id, name, username=None, password=None, rank=None,
                       plate_num=None, veh_type=None, veh_brand=None, veh_model=None, road_tax=None):
        self.connect_sql()
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
                              "(officerID, officerName, rank, plateNum) VALUES (%s, %s, %s, %s)"
                        val = (officer_id, name, rank, plate_num)
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
                    if officer[0][4] == "" or not officer[0][4]:
                        try:
                            # sql = "INSERT INTO plate_num_rec.officer " \
                            #       "(officerID, name, plateNum, vaccinationStatus) VALUES (%s, %s, %s, %s)"
                            sql = "UPDATE plate_num_rec.officer SET officerName = %s, rank = %s, plateNum = %s " \
                                  "WHERE officerID = %s;"
                            val = (name, rank, plate_num, officer_id)
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

        self.connect_sql()
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
                      "(staffID, name, password) VALUES (%s, %s, %s)"
                val = (staff_id, name, password)
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
                      "(staffID, name, password) VALUES (%s, %s, %s)"
                val = (staff_id, name, password)
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

        self.connect_sql()
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

    def remove_vehicle(self, plate_num):
        plate_num = plate_num.upper()

        status = ""
        vehicle = None
        # Fetch User
        try:
            sql = "SELECT * FROM plate_num_rec.vehicle where plateNum = %s"
            val = (plate_num,)
            self.cursor.execute(sql, val)
            result = self.cursor.fetchall()
            vehicle = result
        except Exception as e:
            msg = 'Error Searching Vehicle: ' + str(e)
            print(msg)
            self.db.close()
            return False, msg

        # Remove Vehicle
        if vehicle:
            try:
                sql = "DELETE FROM plate_num_rec.vehicle WHERE plateNum = %s"
                val = (plate_num,)
                self.cursor.execute(sql, val)

                self.db.commit()
                status = "Vehicle Successfully Removed: \n\tPlate Number: " + plate_num
                print(status)
                self.db.close()
                return True, 'Successfully Removed'
            except Exception as e:
                if status == "":
                    status = "Vehicle Failed to Remove: \n\tPlate Number: " + plate_num
                print(status)
                msg = 'Error Removing Vehicle: ' + str(e)
                print(msg)
                self.db.close()
                return False, msg
        else:
            self.db.close()
            return False, 'Vehicle Plate does not Exist'

    ########################################################################################################################
    ######### OTHERS #######################################################################################################

    def login_user(self, staff_id, password):
        # Username is Unique ID
        self.connect_sql()
        staff_list = None
        try:
            self.db.connect()

            # Fetch User
            sql = "SELECT admin.staffID FROM plate_num_rec.admin where admin.staffID LIKE %s"
            val = (staff_id, )
            self.cursor.execute(sql, val)
            result = self.cursor.fetchall()
            staff_list = result
        except Exception as e:
            msg = 'Error: ' + str(e)
            self.db.close()
            return False, msg

        if not staff_list:
            self.db.close()
            return False, "Unrecognised Staff ID"

        try:
            # Fetch User
            sql = "SELECT admin.staffID FROM plate_num_rec.admin where " \
                  "admin.staffID LIKE %s AND " \
                  "admin.password COLLATE latin1_general_cs LIKE %s"
            val = (staff_id, password)
            self.cursor.execute(sql, val)
            result = self.cursor.fetchall()
            staff_list = result
        except Exception as e:
            msg = 'Error: ' + str(e)
            return False, msg

        if staff_list:
            self.db.close()
            return True, ''
        else:
            self.db.close()
            print("Staff ID does not Exist")
            return False, 'Incorrect Password'

    def login_officer(self, officer_id, password):
        # Username is Unique ID
        self.connect_sql()
        officer_list = None
        try:
            self.db.connect()

            # Fetch User
            sql = "SELECT officerID FROM plate_num_rec.officer where officerID LIKE %s"
            val = (officer_id, )
            self.cursor.execute(sql, val)
            result = self.cursor.fetchall()
            officer_list = result
        except Exception as e:
            msg = 'Error: ' + str(e)
            return False, msg

        if not officer_list:
            self.db.close()
            return False, "Unrecognised Officer ID"

        try:
            # Fetch User
            sql = "SELECT officerID FROM plate_num_rec.officer where " \
                  "officerID LIKE %s AND " \
                  "password COLLATE latin1_general_cs LIKE %s"
            val = (officer_id, password)
            self.cursor.execute(sql, val)
            result = self.cursor.fetchall()
            officer_list = result
        except Exception as e:
            msg = 'Error: ' + str(e)
            return False, msg

        if officer_list:
            self.db.close()
            return True, ''
        else:
            self.db.close()
            print("Officer ID does not Exist")
            return False, 'Incorrect Password'

    def remove_driver(self, data):
        """
        Pram for Data Structure:
            Student:
                [driver[0], driver[1].upper(), name, role, driver_id, year, hostel, vac_stat, plate_num,
                             veh_type, veh_brand, veh_model, road_tax,
                             driver_img_tk, driver_img_label, dw_result, driver_img, edit_btn, remove_btn]
            Staff:
                [driver[0], driver[1].upper(), name, role, driver_id, vac_stat, plate_num, veh_type,
                             veh_brand, veh_model, road_tax,
                             driver_img_tk, driver_img_label, dw_result, driver_img, edit_btn, remove_btn]
            Officer:
                [driver[0], driver[1].upper(), name, role, driver_id, rank, plate_num, veh_type, veh_brand,
                             veh_model, road_tax,
                             driver_img_tk, driver_img_label, dw_result, driver_img, edit_btn, remove_btn]
        """

        status = ""
        self.connect_sql()
        self.db.connect()

        # Fetch Driver
        student = None
        try:
            sql = "SELECT * FROM plate_num_rec." + data[0] + " where " + data[1] + " = %s;"
            val = (data[2], )
            self.cursor.execute(sql, val)
            result = self.cursor.fetchall()
        except Exception as e:
            msg = 'Error Searching ' + data[0] + ': ' + str(e)
            print(msg)
            self.db.close()
            return False, msg

        has_pass = None
        if data[0] == 'officer':
            try:
                sql = "SELECT * FROM plate_num_rec." + data[0] + " where " + data[1] + " = %s and password IS NOT NULL;"
                val = (data[2],)
                self.cursor.execute(sql, val)
                has_pass = self.cursor.fetchall()
            except Exception as e:
                msg = 'Error Searching ' + data[1] + ': ' + str(e)
                print(msg)
                self.db.close()
                return False, msg

        # Remove Driver
        if result:
            try:
                sql = ''
                val = None
                if data[0] == 'student':
                    sql = "DELETE FROM plate_num_rec." + data[0] + " where " + data[1] + " = %s;"
                    val = (data[2], )
                elif data[0] == 'staff':
                    # sql = "DELETE FROM plate_num_rec." + data[0] + " where " + data[1] + " = %s;"
                    sql = "UPDATE plate_num_rec.staff  SET  plateNum = NULL, vaccinationStatus = NULL " \
                          "WHERE " + data[1] + " = %s;"
                    val = (data[2], )
                elif data[0] == 'officer' and has_pass:
                    # sql = "DELETE FROM plate_num_rec." + data[0] + " where " + data[1] + " = %s;"
                    sql = "UPDATE plate_num_rec.officer  SET  plateNum = NULL, rank = NULL " \
                          "WHERE " + data[1] + " = %s;"
                    val = (data[2], )
                elif data[0] == 'officer' and not has_pass:
                    sql = "DELETE FROM plate_num_rec.officer where " + data[1] + " = %s;"
                    val = (data[2],)
                self.cursor.execute(sql, val)

                self.db.commit()
                status = "User Successfully Removed: \n\t" + data[1] + "\t\t: " + data[2]

                stats, msg = self.remove_vehicle(data[3])

                self.db.close()
                if stats:
                    return True, 'Successfully Remove Driver'
                else:
                    return stats, msg

            except Exception as e:
                if status == "":
                    status = "User Failed to Remove: \n\t" + data[1] + "\t\t: " + data[2]
                print(status)
                msg = 'Error Remove ' + data[0] + ': ' + str(e)
                print(msg)
                self.db.close()
                return False, msg
        else:
            self.db.close()
            return False, "Driver Not Found"

    def edit_driver(self, driver_id, role, data_type, value):
        role = role.lower()
        driver_id = driver_id.upper()
        db_attribute = {
            'Name': 'name',
            'Year': 'year',
            'Hostel': 'hostelStatus',
            'Vaccination Status': 'vaccinationStatus',
            'Rank': 'rank',
            'Plate Number': 'plateNum',
            'Vehicle Type': 'vehType',
            'Vehicle Brand': 'vehBrand',
            'Vehicle Model': 'vehModel',
            'Road Tax': 'roadTaxExpiry'
        }
        type_db = db_attribute[data_type]
        id_type = ''

        if role == 'student':
            id_type = 'studentID'
        elif role == 'staff':
            id_type = 'staffID'
        elif role == 'officer':
            id_type = 'officerID'
            if type_db == 'name':
                type_db = 'officerName'

        self.connect_sql()
        self.db.connect()
        # Fetch User
        status = ""
        try:
            sql = "SELECT " + id_type + ", plateNum FROM plate_num_rec." + role + \
                  " where " + id_type + " = %s and plateNum IS NOT NULL"
            val = (driver_id,)
            self.cursor.execute(sql, val)
            result = self.cursor.fetchall()

        except Exception as e:
            msg = 'Error: ' + str(e)
            print(msg)
            self.db.close()
            return False, msg

        if result:
            try:
                if type_db == 'plateNum' or type_db == 'vehType' or type_db == 'vehBrand' or type_db == 'vehModel' or \
                        type_db == 'roadTaxExpiry':
                    sql = "UPDATE plate_num_rec.vehicle SET " + type_db + " = %s WHERE plateNum = %s;"
                    val = (value, result[0][1])
                else:
                    sql = "UPDATE plate_num_rec." + role + " SET " + type_db + " = %s WHERE " + id_type + " = %s;"
                    val = (value, driver_id)
                self.cursor.execute(sql, val)
                self.db.commit()

                if type_db == 'plateNum':
                    sql = "UPDATE plate_num_rec." + role + " SET " + type_db + " = %s WHERE " + id_type + " = %s;"
                    val = (value, driver_id)
                    self.cursor.execute(sql, val)
                    self.db.commit()

                self.db.close()
                return True, 'Successfully Edit Driver'
            except Exception as e:
                msg = 'Error: ' + str(e)
                print(msg)
                self.db.close()
                return False, msg
        else:
            self.db.close()
            return False, 'Driver Has No Vehicle'

    def remove_admin(self, data):
        """
        Pram for Data Structure:
            Staff:
                [staff, staffID, name, edit_btn, remove_btn]
            Officer:
                [officer, OfficerID, name, edit_btn, remove_btn]
        """
        # status = ""
        # role_type = ''
        # role = data[0]
        # if role == 'staff':
        #     role = 'admin'
        #     role_type = 'staffID'
        # elif role == 'officer':
        #     role_type = 'officerID'


        self.connect_sql()
        self.db.connect()

        # Fetch User
        student = None
        try:
            sql = "SELECT * FROM plate_num_rec." + data[0] + " where " + data[1] + " = %s;"
            val = (data[2], )
            self.cursor.execute(sql, val)
            result = self.cursor.fetchall()
        except Exception as e:
            msg = 'Error Searching ' + data[1] + ': ' + str(e)
            print(msg)
            self.db.close()
            return False, msg

        has_plate = None
        if data[0] == 'officer':
            try:
                sql = "SELECT * FROM plate_num_rec." + data[0] + " where " + data[1] + " = %s and plateNum IS NOT NULL;"
                val = (data[2],)
                self.cursor.execute(sql, val)
                has_plate = self.cursor.fetchall()
            except Exception as e:
                msg = 'Error Searching ' + data[1] + ': ' + str(e)
                print(msg)
                self.db.close()
                return False, msg

        # Remove User
        print(result)
        if result:
            try:
                sql = ''
                val = None
                if data[0] == 'admin':
                    # sql = "DELETE FROM plate_num_rec." + data[0] + " where " + data[1] + " = %s;"
                    sql = "DELETE FROM plate_num_rec." + data[0] + " where " + data[1] + " = %s;"
                    val = (data[2], )
                elif data[0] == 'officer' and has_plate:
                    # sql = "DELETE FROM plate_num_rec." + data[0] + " where " + data[1] + " = %s;"
                    sql = "UPDATE plate_num_rec." + data[0] + "  SET  password = NULL WHERE " + data[1] + " = %s;"
                    val = (data[2], )
                elif data[0] == 'officer' and not has_plate:
                    sql = "DELETE FROM plate_num_rec." + data[0] + " where " + data[1] + " = %s;"
                    val = (data[2],)
                self.cursor.execute(sql, val)

                self.db.commit()
                self.db.close()
                status = "User Successfully Removed: \n\t" + data[1] + "\t\t: " + data[2]

                return True, 'Successfully Remove User'

            except Exception as e:
                if status == "":
                    status = "User Failed to Remove: \n\t" + data[1] + "\t\t: " + data[2]
                print(status)
                msg = 'Error Remove ' + data[0] + ': ' + str(e)
                print(msg)
                self.db.close()
                return False, msg
        else:
            self.db.close()
            return False, "User Not Found"

    def edit_admin_personal(self, admin_id, role, data_type, value):
        role_msg = role
        role = role.lower()
        admin_id = admin_id.upper()
        db_attribute = {
            'Name': 'name',
            'Password': 'password'
        }
        type_db = db_attribute[data_type]
        id_type = ''

        if role == 'staff':
            id_type = 'staffID'
            role = 'admin'
        elif role == 'officer':
            id_type = 'officerID'
            if type_db == 'name':
                type_db = 'officerName'

        self.connect_sql()
        self.db.connect()
        # Fetch User
        status = ""
        try:
            sql = "SELECT " + id_type + " FROM plate_num_rec." + role + \
                  " where " + id_type + " = %s"
            val = (admin_id,)
            self.cursor.execute(sql, val)
            result = self.cursor.fetchall()

        except Exception as e:
            msg = 'Error: ' + str(e)
            print(msg)
            self.db.close()
            return False, msg

        if result:
            try:
                sql = "UPDATE plate_num_rec." + role + " SET " + type_db + " = %s WHERE " + id_type + " = %s;"
                val = (value, admin_id)
                self.cursor.execute(sql, val)
                self.db.commit()

                if role == 'admin' and type_db == 'name':
                    sql = "UPDATE plate_num_rec.staff SET " + type_db + " = %s WHERE " + id_type + " = %s;"
                    val = (value, admin_id)
                    self.cursor.execute(sql, val)
                    self.db.commit()

                self.db.close()
                return True, 'Successfully Edit ' + role_msg
            except Exception as e:
                msg = 'Error: ' + str(e)
                print(msg)
                self.db.close()
                return False, msg
        else:
            return False, 'This ID is not ' + role_msg

    def edit_admin(self, data):
        role = data[0].lower()
        id_type = data[1]
        type_db = data[2]
        admin_id = data[3].upper()
        value = data[4]

        if type_db != 'password':
            value = value.upper()

        self.connect_sql()
        self.db.connect()
        # Fetch User
        status = ""
        try:
            sql = "SELECT " + id_type + " FROM plate_num_rec." + role + \
                  " where " + id_type + " = %s"
            val = (admin_id,)
            self.cursor.execute(sql, val)
            result = self.cursor.fetchall()

        except Exception as e:
            msg = 'Error: ' + str(e)
            print(msg)
            self.db.close()
            return False, msg

        if result:
            try:
                sql = "UPDATE plate_num_rec." + role + " SET " + type_db + " = %s WHERE " + id_type + " = %s;"
                val = (value, admin_id)
                self.cursor.execute(sql, val)
                self.db.commit()

                if type_db == 'name' and role == 'admin':
                    sql = "UPDATE plate_num_rec.staff SET " + type_db + " = %s WHERE " + id_type + " = %s;"
                    val = (value, admin_id)
                    self.cursor.execute(sql, val)
                    self.db.commit()

                self.db.close()
                return True, 'Successfully Edit Admin'
            except Exception as e:
                msg = 'Error: ' + str(e)
                print(msg)
                self.db.close()
                return 'Failed', None, ''
        else:
            self.db.close()
            return False, 'This ID is not Admin/Officer'

    def find_driver(self, plate_num):
        self.connect_sql()
        self.db.connect()

        try:
            sql = "SELECT studentID, name, plateNum FROM plate_num_rec.student where plateNum = %s"
            val = (plate_num,)
            self.cursor.execute(sql, val)
            student = self.cursor.fetchall()

            sql = "SELECT staffID, name, plateNum FROM plate_num_rec.staff where plateNum = %s"
            val = (plate_num,)
            self.cursor.execute(sql, val)
            staff = self.cursor.fetchall()

            sql = "SELECT officerID, officerName, plateNum FROM plate_num_rec.officer where plateNum = %s"
            val = (plate_num,)
            self.cursor.execute(sql, val)
            officer = self.cursor.fetchall()
        except Exception as e:
            msg = 'Error: ' + str(e)
            print(msg)
            self.db.close()
            return False, msg, ''

        self.db.close()
        if student:
            return 'Found Plate Number', student, 'Student'
        elif staff:
            return 'Found Plate Number', staff, 'Staff'
        elif officer:
            return 'Found Plate Number', officer, 'Officer'
        else:
            return 'Unrecognised Plate Number', None, ''

    def insert_log_driver(self, plate_num, recognition, type_ent='', gate=''):
        self.connect_sql()
        self.db.connect()
        try:
            # sql = "SELECT studentID, name, plateNum FROM plate_num_rec.student where plateNum = %s"
            sql = "INSERT INTO plate_num_rec.entry_log (plateNum, recognition, type, gate) VALUES (%s, %s, %s, %s)"
            val = (plate_num, recognition, type_ent, gate)
            self.cursor.execute(sql, val)
            self.db.commit()

            self.db.close()
            return True, 'Suceesfully Insert to Log'
        except Exception as e:
            msg = 'Error: ' + str(e)
            print(msg)
            self.db.close()
            return False, msg

    def get_log(self, date):
        self.connect_sql()
        self.db.connect()
        try:
            sql = "SELECT time, plateNum, recognition, gate FROM plate_num_rec.entry_log where " \
                  "date = %s AND type = 'enter' ORDER BY time DESC"
            val = (date, )
            self.cursor.execute(sql, val)
            enter = self.cursor.fetchall()

            sql = "SELECT time, plateNum, recognition, gate FROM plate_num_rec.entry_log where " \
                  "date = %s AND type = 'exit' ORDER BY time DESC"
            val = (date,)
            self.cursor.execute(sql, val)
            exit = self.cursor.fetchall()

            return enter, exit
        except Exception as e:
            msg = 'Error: ' + str(e)
            print(msg)
            return None, None

    ########################################################################################################################
    ######### UNUSED #######################################################################################################

    """
    def select_user(self):
        # Fetch User
        self.cursor.execute("SELECT * FROM plate_num_rec.user")
        result = self.cursor.fetchall()
        staff_list = result

        for staff in staff_list:
            print(staff)
    """

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


########################################################################################################################

class Filezilla:
    def __init__(self, host="localhost", user="pnradmin", password="pnradmin"):
        self.host = host
        self.user = user
        self.password = password
        self.ftp = None
        try:
            self.ftp = ftplib.FTP(self.host)
            print("Successfully Connect: ", self.ftp)
            self.ftp.login(self.user, self.password)
            self.ftp.close()
        except BaseException as err:
            print("Error: ", err)

    def update_connection(self, host=None, user=None, password=None):
        if not host:
            self.host = "localhost"
        else:
            self.host = host
        if not user:
            self.user = "pnradmin"
        else:
            self.user = user
        if not password:
            self.password = "pnradmin"
        else:
            self.password = password

        try:
            self.ftp = ftplib.FTP(self.host)
            print("Successfully Connect: ", self.ftp)
            self.ftp.login(self.user, self.password)
            self.ftp.close()
            return True
        except BaseException as err:
            print("Error: ", err)
            return False

    # To upload files to server
    def up_to_server(self, imgpath, imgfile, driver_id, mode):
        try:
            self.ftp = ftplib.FTP(self.host)
            self.ftp.login(self.user, self.password)

            if mode == 1:
                self.ftp.cwd("/driver")  # Folder path
            elif mode == 2:
                self.ftp.cwd("/plate_number")  # Folder path
            elif mode == 3:
                self.ftp.cwd("/webcam")  # Folder path

            with open(os.path.join(imgpath, imgfile), "rb") as file:
                # Command for Uploading the file "STOR filename"
                self.ftp.storbinary(f"STOR {imgfile}", file)

            # Change file name into studentid/staffid
            for f in self.ftp.nlst():
                if driver_id in f:
                    self.ftp.delete(driver_id)
                if imgfile in f:
                    self.ftp.rename(imgfile, driver_id.upper() + os.path.splitext(imgfile)[1])

            # os.remove(imgfile)  # Delete file from local/client side
            self.ftp.dir()

            file.close()
            self.ftp.quit()
            return True
        except BaseException as err:
            print("Error: ", err)
            return False

    # To download files from server
    def dw_from_server(self, imgpath, id_driver, mode):
        try:
            self.ftp = ftplib.FTP(self.host)
            self.ftp.login(self.user, self.password)

            if mode == 1:
                self.ftp.cwd("/driver")  # Folder path
            elif mode == 2:
                self.ftp.cwd("/plate_number")  # Folder path
            elif mode == 3:
                self.ftp.cwd("/webcam")  # Folder path

            filelist = []
            self.ftp.retrlines('LIST', filelist.append)
            print(filelist)

            f = 0

            filename = ''
            for f in filelist:
                if id_driver in f:
                    filename = id_driver + os.path.splitext(f)[1]
                    print(filename)
                    with open(filename, "wb") as file:
                        # Command for Uploading the file "STOR filename"
                        self.ftp.retrbinary(f"RETR {filename}", file.write)
                        f = 1

                    self.ftp.dir()
                    file.close()
                    print("SUCCESSFULLY TRANSFERRED")

            source = os.path.join('./', filename)
            dest = os.path.join(imgpath, filename)
            shutil.move(source, dest)

            if f == 0:
                print("FILE DOES NOT EXIST")
                return False, ''

            self.ftp.quit()
            return True, filename
        except BaseException as err:
            print("Error: ", err)
            return False, ''

    def rem_from_server(self, id_driver):
        DRIVER = 'driver'
        PLATE = 'plate_number'

        try:
            self.ftp = ftplib.FTP(self.host)
            self.ftp.login(self.user, self.password)

            self.ftp.cwd("/driver")
            filelist = []
            self.ftp.retrlines('LIST', filelist.append)
            print(filelist)

            filename = ''
            for f in filelist:
                if id_driver in f:
                    filename = id_driver + os.path.splitext(f)[1]
                    print(filename)
                    self.ftp.delete(filename)
                    print("SUCCESSFULLY REMOVED DRIVER")

            self.ftp.cwd("/plate_number")
            filelist = []
            self.ftp.retrlines('LIST', filelist.append)
            print(filelist)

            filename = ''
            for f in filelist:
                if id_driver in f:
                    filename = id_driver + os.path.splitext(f)[1]
                    print(filename)
                    self.ftp.delete(filename)
                    print("SUCCESSFULLY REMOVED PLATE NUMBER")

            self.ftp.quit()
            return True, 'Successfully Remove Image'
        except Exception as e:
            msg = "Error: " + str(e)
            print(msg)
            self.ftp.quit()
            return False, msg

    # Download all files from server's directories
    def dw_all_files(self, mode):
        try:
            self.ftp = ftplib.FTP(self.host)
            self.ftp.login(self.user, self.password)

            if mode == 1:
                self.ftp.cwd("/driver")  # Folder path
            elif mode == 2:
                self.ftp.cwd("/plate_number")  # Folder path
            elif mode == 3:
                self.ftp.cwd("/webcam")  # Folder path

            for f in self.ftp.nlst():
                with open(f, "wb") as file:
                    # Command for Uploading the file "STOR filename"
                    self.ftp.retrbinary(f"RETR {f}", file.write)

            file.close()
            self.ftp.close()
            return True
        except BaseException as err:
            print("Error: ", err)
            return False



# db = Database()
# for i in range(0,1000):
#     db.update_connection()
# db.connect()

"""
    MySQL
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
    MySQL
    Latest Version
"""
# db.search_driver('a', 'plate', 'all')
# db.insert_vehicle('CAB1234', 'Anqib', 'Pijot', '2022-12-15')
# db.insert_student('B999999999', 'ABC', 2, 'Campus', '2 Dose', 'CAB1234', 'Yamaha', '2022-12-15')
# db.insert_staff('B23456789', 'CBA', "Lecturer", "CBA1234", "2 dose", "Proton", "2022-12-15")
# db.insert_admin('abc', '123456789', '123', '123')
# db.insert_officer('1234', 'abc', '123', '123', 'abc')
# db.insert_officer('4321', 'cba', '123', '123', 'cba', 'AAA1111', 'Bike', 'Yamaha', 'R15', '2022-12-15')

"""
    FileZilla
"""
# fl = Filezilla()
# fl.up_to_server("tom.png", "B031910127.png", 2)
# fl.dw_from_server(os.path.join('temp', 'driver'), "B031910126", 1)
