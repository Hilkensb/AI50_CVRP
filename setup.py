import sys
import os
import subprocess

logo: str = """
                          WX0Okxxddoolllloxk0XW                                                     
                       WNK000KXXNNNNNXK0kdlccldOXW                                                  
                     WNXXNW              WXOdlccokOKW                                               
                     WWW                    N0dccccokN                                              
                                              XklccccxXW                                            
                                               NklccccdKW                                           
                                                NkllcccdX                                           
             WWNXXK0000000KXXNW                  XOdccccxX                                          
         WX0OkdollccccccccllloxkOKNW             WW0occccxX                                         
     WN0kdoccccccccccccccccccccccloxOXW            NklccccxXW                            WXXW       
   N0kolccccccccccccccccccccccccccccclx0NW          Xxccccco0N                         WXkoox0NW    
WNOdlccccccccccccccccccccccccccccccccccld0N          XdccccclxKW                     WXOdccccldkKW  
0dcccccccccccccccloxkO000K000OkxolccccccclxKW         XxlcccccldOXW               WN0koccccccccclxOX
OdlcccccccccccoxOKNW           WNKOdlcccccco0W         Nklcccccccldk0KXNNWWWNNXK0Oxolccccccccccccclk
WNKkolcccccldOXW                   NKxlccccclON         WKxlcccccccccllodddddollccccccccccccccccld0N
   WN0xlccd0N                        WKxlcccclOW          N0xlccccccccccccccccccccccccccccccccox0N  
      WXOOXW                           NOocccco0W           WKkdlccccccccccccccccccccccccclox0XW    
         W                              W0occccdX             WNKOkdolccccccccccccccccldxOKNW       
                                         W0occclkNW               WWXK0OkkxxdddxxkkO0KXNW           
                                          WOlccclONW                      WWWWWWW                   
                                           WOlcccox0W                                               
                                            WOlcccco0W                                              
                                             W0dccccoON                                             
                                              WXkolccld0NW                WNNNW                     
                                                WX0OdlccoxOKNWW      WWNXKKKNW                      
                                                   WNKOxolclodxkkOOOkkkO0KNW                        
                                                       WNK0OkkkxxkkO0KNW                            
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                     WNNNW            WNXXNW              WW          WWNNNW                        
                    KdxOOkx0W       NOxkOOkxON          W0okN         KdxOOOkON                     
                    0o0  WklO      NxoKW  WKodN         0dxoxN        OoK  WXxoK                    
                    0lkKK0xdK      0lO      OlO        KdkWKoOW       koK    XoxW                   
                    0ldOkloK       0lkW     Ol0       NockOOoc0       OoK    KlxW                   
                    0o0  KdxX      WkoONWWNOoxN      WkoO0000ooX      Ol0WNX0dxX                    
                    0d0   XoxW      WOloddolkN       KoOW    KoOW     OclddookN                     
"""

print(logo)

# Display the detected python version
print("Python version detected: ", sys.version)

# Check python version
if int(sys.version_info[0]) != 3 or int(sys.version_info[1]) < 8:
    # Wrong python version 
    print("The ROAD project requires a python version of 3.8+. You should upgrade your python version and then re-run the setup.")
    sys.exit()
elif int(sys.version_info[1]) > 9:
    print("The python version you have has not been tested. If any problem consider downgrading your python version to python 3.8 or 3.9.")
    
# Check the system
print("Operting system detected: ", sys.platform)
if sys.platform not in ["win32", "linux"]:
    # Wrong os platform
    print("Your os will not be supported fully by the ROAD project. Some features will not work properly with your os.")

# Install the python librairies
print("Python dependancies will be installed. Use the default pip command ? [y/n]: ", end="")
answer: str = input()

command: str = "pip install -r requirements.txt"
if answer.lower() == "n":
    print("Please enter the pip you want to use (for example pip3): ", end="")
    pip_to_use: str = input()
    command: str = pip_to_use.strip() + " install -r requirements.txt"
elif answer.lower() not in ["n", "y"]:
    print("Unknown answer: ", answer, ". The default pip will be used.")

os.system(command)

print("The setup is now finished.")

