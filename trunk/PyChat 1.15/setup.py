from distutils.core import setup
import py2exe, sys
# Use this cmd: python -OO setup.py py2exe
sys.argv.append('py2exe') 

setup(

    #windows = ["main.py"],
	windows= [{
		"script":"main.py",
		}],
    
    options= {
		"py2exe":{
			"includes":["sip"],
			"optimize": 2,
			'compressed':True,
			}
	}
	
    
    
    
    )

# setup(
# version = "0.5.0",
# description = "py2exe sample script",
# name = "py2exe samples",

# windows = ["chat_from.py"],
# console= ["Nullchat.py"],  
# )