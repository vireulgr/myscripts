import subprocess
import re

#userName = "VirtUser"
subprocess.run( "sc create BatchInstallationService binpath=\"C:\\Users\\VirtUser\\Desktop\\misc\\BatchInstallationService.exe\"" )
#subprocess.check_output("sc create", "BatchInstallationService", "binpath=\"C:\Users\VirtUser\Desktop\misc\BatchInstallationService.exe\"" )

serviceSID = subprocess.check_output( "sc sdshow BatchInstallationService" ).decode("cp866").strip()

#print( serviceSID ) 

resp = subprocess.check_output( "whoami /USER /NH" ).decode( "cp866" ).strip()
#userSID = subprocess.check_output( "whoami /all" ).decode( "cp866" ).strip()
userSID = resp.split()[1]
#regexpstr = "{0}\s+([-0-9a-zA-Z]+)".format( userName ) 
#print ( regexpstr )
#m = re.search( regexpstr, userSID, flags=re.IGNORECASE )
#if m:
#    #print( m.group(1) )
#    userSID = m.group(1)
#else:
#    print( "Cannot determine user SID :(" )
#    exit( 0 )

#print( userSID )

newSvcSID = "{0}(A;;RPWPDT;;;{1})".format( serviceSID, userSID )
#newSvcSID = serviceSID + "(A;;RPWPDT;;;" +  userSID + ")"
#print( newSvcSID )

cmd = "sc sdset BatchInstallationService {0}".format( newSvcSID )

print( cmd )
#subprocess.run( cmd )

