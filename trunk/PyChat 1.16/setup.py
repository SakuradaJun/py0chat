from distutils.core import setup
import py2exe, sys
# python -OO setup.py py2exe

sys.argv.append('py2exe') 
"""windows= [{
    "script":"pychat.py",
    }],
"""
setup(
    
    #windows
    console = [
               {
               'script':"pychat.py",
               "icon_resources": [(1, 'icon_of_exe.ico')]
               }
    ], 
    
    options= {
		"py2exe":{
			"includes":["sip","PyQt4", "PyQt4.QtNetwork","PyQt4.QtNetwork","PyQt4.QtWebKit"],
			"optimize": 2,
			'compressed':True,
			}
	}
	
    
    
    
    )

import os
os.system("pyrcc4.exe -o res_.py res_.qrc")

# setup(
    # version = "0.5.0",
    # description = "py2exe sample script",
    # name = "py2exe samples",
    
    # windows = ["chat_from.py"],
    # console= ["Nullchat.py"],  
    # )

