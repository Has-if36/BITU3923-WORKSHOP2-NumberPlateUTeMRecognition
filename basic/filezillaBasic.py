"""
 Server side:
     1. Install/Start FileZilla (Server) from XAMPP Control Panel
     2. On the 'Edit' tab (top left corner), open 'Users'
     4. In 'general', Add User, For Ex; pnrAdmin (Plate Number Recognition)
     5. Enable password if want and put the same pass as Username for easier access
     6. In 'Shared Folders', Add shared folders and set any directory (The first time set is your home directory)
           Ex; 'Plate Number Recognition Project'
     7. On 'Files' category, tick necessary item (all if want)
     8. On 'Directories' category, tick necessary item (all if want)
     9. Make sure to allow firewall

 Allow Firewall for FileZilla (Server)
     1. Open Firewall, go to 'Advanced Settings' (on the left bar)
     2. Go to 'Inbound Rules' (on the left bar), add 'New Rule...' (on the right bar)
     3.1. 'Rule Type', set to 'port'
     3.2. 'Protocol and Ports', set to 'TCP' and set 'Specific local ports', put '21' (same as the default port of FileZilla)
     3.3. 'Action', set to 'Allow the Connection'
     3.4. 'Profile', ONLY tick 'private', untick the rest ('Thus, make sure the Wi-Fi you connected is 'home network' for this to work')
     3.5. 'Name', set any name (Ex; 'filezilla'). Then click 'finish'
     4. add 'New Rule...' and repeat Step 3, But in 'Protocol and Ports', set to 'UDP'
     5. Go to 'Outbound Rules' (on the left bar), add 'New Rule...' (on the right bar)
     6. add 'New Rule...' and repeat Step 3
     7. add 'New Rule...' and repeat Step 3, But in 'Protocol and Ports', set to 'UDP'
NOTE: You should still be safe even after allowing this in your Firewall, unless you port forward this port 21 (which allows port 21 goes public)
Note: This will only allow any device shared same network with the server to enter (aka. Intranet)

 Client side
     1. Download and install FileZilla for Client (There are two types of Software, FileZilla (Client) and FileZilla (Server))
     2. For host, put your IP Address of the server
     3. Username and password is the same one as you created in server side (Step 3 and 4)
     4. The default port is 21
"""

import os
import ftplib
import zipfile

ftp = ftplib.FTP("192.168.1.254")
ftp.login("pnrAdmin", "pnrAdmin")

savefile = r"C:/Users/user/Desktop"            # Client Side Path File
os.chdir(savefile)
dir = ftp.cwd("./Driver Pic")                   # Server Side Path File
                                                # Inside 'Plate Number Recognition Project', 'Driver Pic' folder was created

file = open("Snoop.png", "wb")                  # Selecting item to download, Ex. file; Snoop.png
ftp.retrbinary("RETR Snoop.png", file.write)    # Start Download
file.close()
ftp.cwd("../")
print("Done")