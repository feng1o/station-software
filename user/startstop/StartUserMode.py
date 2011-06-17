from startStop import *
from hslog import *
import sys
import time
path='%s:' %os.getenv("HISPARC_DRIVE")

import ConfigParser
import os
import glob


def start():
	setLogMode(MODE_BOTH)
	log('\nStarting User-Mode applications...')

        c = ConfigParser.ConfigParser()
        c.read(os.path.join(path, '/persistent/configuration/config.ini'))
	
	try:
		#start mySql
		log('Starting MySQL...')
		datapath = "%s/persistent/data/mysql" % path
		binlogs = glob.glob(os.path.join(datapath, 'mysql-bin.*'))
		if binlogs:
			log("Removing stale MySQL binary logs...")
			for f in binlogs:
				os.remove(f)

		mySqlHandler=StartStop()
		mySqlHandler.exeName='mysqld.exe'
		mySqlHandler.ShowWindow=win32con.SW_HIDE
		mySqlHandler.command="%s\\user\\mysql\\bin\\mysqld.exe" %path
		mySqlHandler.currentDirectory="%s\\user\\mysql\\bin" %path
		mySqlHandler.title='MySQL server'
		resMySql=mySqlHandler.startProcess()
		if resMySql==0:
			log('Status:running')
		elif resMySql==1:
			log('Status:stopped')
		else:
			log ('An exception was generated!')
	except:
		log('An exception was generated while starting MySQL:' + str(sys.exc_info()[1]))
	
	try:
		#start LabView
                if c.getboolean('Detector', 'enabled'):
                    log('Starting LabView...')
                    labViewHandler=StartStop()
                    labViewHandler.exeName='hisparcdaq.exe'
                    labViewHandler.currentDirectory="%s\\user\\hisparcdaq" %path
                    labViewHandler.command="%s\\user\\hisparcdaq\\hisparcdaq.exe" %path
                    resLabView=labViewHandler.startProcess()
                    if resLabView==0:
                            log('Status:running')
                    elif resLabView==1:
                            log('Status:stopped')
                    else:
                            log ('An exception was generated!')
                else:
                    log('HiSPARC detector disabled...')
        except:
                log('An exception was generated while starting LabView:' + str(sys.exc_info()[1]))

	try:
		#start LabView weather
                if c.getboolean('Weerstation', 'enabled'):
                    log('Starting LabView weather...')
                    labViewHandler=StartStop()
                    labViewHandler.exeName='hisparcweather.exe'
                    labViewHandler.currentDirectory="%s\\user\\hisparcweather" %path
                    labViewHandler.command="%s\\user\\hisparcweather\\hisparcweather.exe" %path
                    resLabView=labViewHandler.startProcess()
                    if resLabView==0:
                            log('Status:running')
                    elif resLabView==1:
                            log('Status:stopped')
                    else:
                            log ('An exception was generated!')
                else:
                    log('HiSPARC weather station disabled...')
        except:
                log('An exception was generated while starting LabView:' + str(sys.exc_info()[1]))

        # Introduce a 30-second pause to let MySQL start completely
        time.sleep(30)
	
	try:
		#start HSMonitor
		log('Starting HSMonitor...')
		hsMonitorHandler=CMDStartStop()
		hsMonitorHandler.exeName='python.exe'
		hsMonitorHandler.title='HISPARC MONITOR: hsmonitor'
		hsMonitorHandler.currentDirectory="%s\user\hsmonitor\src" %path
		hsMonitorHandler.command="%s\user\python\python.exe HsMonitor.py" % path
		resHSMonitor=hsMonitorHandler.startProcess()
		if resHSMonitor==0:
			log('Status:running')
		elif resHSMonitor==1:
			log('Status:stopped')
		else:
			log ('An exception was generated')

	except:
		log('An exception was generated while starting HSMonitor:' + str(sys.exc_info()[1]))
	try:
		#start updater
		log('Starting Updater...')
		updaterHandler=CMDStartStop()
		updaterHandler.exeName='python.exe'
		updaterHandler.title='HISPARC Updater: updater'
		updaterHandler.currentDirectory="%s\\user\\updater" %path
		updaterHandler.command="%s\\user\\python\\python.exe Update.py" % path
		resUpdater=updaterHandler.startProcess()
		if resUpdater==0:
			log('Status:running')
		elif resHSMonitor==1:
			log('Status:stopped')
		else:
			log ('An exception was generated')
		
	except:
		log('An exception was generated while starting the Updater:' + str(sys.exc_info()[1]))


start()

