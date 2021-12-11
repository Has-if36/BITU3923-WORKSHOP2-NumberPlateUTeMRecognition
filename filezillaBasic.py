# Server side:
# 1. Install/Start FileZilla (Server) from XAMPP Control Panel
# 2. On the 'Edit' tab (top left corner), open 'Users'
# 4. In 'general', Add User, For Ex; pnrAdmin (Plate Number Recognition)
# 5. Enable password if want and put the same pass as Username for easier access
# 6. In 'Shared Folders', Add shared folders and set any directory (The first time set is your home directory)
#       Ex; 'Plate Number Recognition Project'
# 7. On 'Files' category, tick necessary item (all if want)
# 8. On 'Directories' category, tick necessary item (all if want)
# 9. Make sure to allow firewall

# Allow Firewall for FileZilla (Server)
# 1. Open Firewall, go to 'Advanced Settings' (on the left bar)
# 2. Go to 'Inbound Rules' (on the left bar), add 'New Rule...' (on the right bar)
# 3.1. 'Rule Type', set to 'port'
# 3.2. 'Protocol and Ports', set to 'TCP' and set 'Specific local ports', put '21' (same as the default port of FileZilla)
# 3.3. 'Action', set to 'Allow the Connection'
# 3.4. 'Profile', ONLY tick 'private', untick the rest ('Thus, make sure the Wi-Fi you connected is 'home network' for this to work')
# 3.5. 'Name', set any name (Ex; 'filezilla'). Then click 'finish'
# 4. add 'New Rule...' and repeat Step 3, But in 'Protocol and Ports', set to 'UDP'
# 5. Go to 'Outbound Rules' (on the left bar), add 'New Rule...' (on the right bar)
# 6. add 'New Rule...' and repeat Step 3
# 7. add 'New Rule...' and repeat Step 3, But in 'Protocol and Ports', set to 'UDP'
# NOTE: You should still be safe even after allowing this in your Firewall, unless you port forward this port 21 (which allows port 21 goes public)
# Note: This will only allow any device shared same network with the server to enter (aka. Intranet)

# Client side
# 1. Download and install FileZilla for Client (There are two types of Software, FileZilla (Client) and FileZilla (Server))
# 2. For host, put your IP Address of the server
# 3. Username and password is the same one as you created in server side (Step 3 and 4)
# 4. The default port is 21

import os
import ftplib
import zipfile

"""ftp = ftplib.FTP("192.168.1.254")"""

"""
savefile = r"C:/Users/user/Desktop"            # Client Side Path File
os.chdir(savefile)
dir = ftp.cwd("./Driver Pic")                   # Server Side Path File
                                                # Inside 'Plate Number Recognition Project', 'Driver Pic' folder was created

file = open("Snoop.png", "wb")                  # Selecting item to download, Ex. file; Snoop.png
ftp.retrbinary("RETR Snoop.png", file.write)    # Start Download
file.close()
ftp.cwd("../")
print("Done")"""

ftp = ftplib.FTP("127.0.0.1")
ftp.login("pnrAdmin", "1234")

class Filezilla:
    # To upload files to server
    def up_to_server(self, imgfile, id, mode):

        if mode == 1:
            ftp.cwd("/Driver images")  # Folder path
        elif mode == 2:
            ftp.cwd("/Plate num")  # Folder path
        elif mode == 3:
            ftp.cwd("/Webcam image")  # Folder path

        with open(imgfile, "rb") as file:
            # Command for Uploading the file "STOR filename"
            ftp.storbinary(f"STOR {imgfile}", file)

        # Change file name into studentid/staffid
        for f in ftp.nlst():
            if id in f:
                ftp.delete(id)
            if imgfile in f:
                ftp.rename(imgfile, id)

        os.remove(imgfile) #Delete file from local/client side
        ftp.dir()

        file.close()
        ftp.quit()

    # To download files from server
    def dw_from_server(self, imgfile, mode):

        if mode == 1:
            ftp.cwd("/Driver images")  # Folder path
        elif mode == 2:
            ftp.cwd("/Plate num")  # Folder path
        elif mode == 3:
            ftp.cwd("/Webcam image")  # Folder path

        filelist = []
        ftp.retrlines('LIST', filelist.append)
        print(filelist)

        f = 0

        for f in filelist:
            if imgfile in f:
                with open(imgfile, "wb") as file:
                    # Command for Uploading the file "STOR filename"
                    ftp.retrbinary(f"RETR {imgfile}", file.write)
                    f = 1

                ftp.dir()
                file.close()
                print("SUCCESSFULLY TRANSFERRED")

        if f == 0:
            print("FILE DOES NOT EXIST")

        ftp.quit()

    # Download all files from server's directories
    def dw_all_files(self, mode):

        if mode == 1:
            ftp.cwd("/Driver images")  # Folder path
        elif mode == 2:
            ftp.cwd("/Plate num")  # Folder path
        elif mode == 3:
            ftp.cwd("/Webcam image")  # Folder path

        for f in ftp.nlst():
            with open(f, "wb") as file:
                # Command for Uploading the file "STOR filename"
                ftp.retrbinary(f"RETR {f}", file.write)

        file.close()
        ftp.close()

fl = Filezilla()

fl.up_to_server("tom.png", "B031910127.png", 2)  # Take image from client
# fl.dw_from_server("img1.png", 1)  #Take image from server
# fl.dw_all_files(id, 1) #Take all files in server's directories