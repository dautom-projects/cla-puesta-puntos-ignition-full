#* DAUTOM SAS CONFIDENTIAL
#*_________________________
#*
#* [2013] - [2025] DAUTOM SAS
#* All Rights Reserved.
#*
#* NOTICE: All information contained herein is, and remains the property
#* of DAUTOM SAS and its suppliers, if any. The intellectual and 
#* technical concepts contained herein are proprietary to DAUTOM SAS
#* and its suppliers and may be covered by U.S and Foreign Patents, 
#* patents in process, and are protected by trade secret or copyright law. 
#* Dissemination of this information or reproduction of this material
#* is strictly forbidden unless prior written permission is obtained
#* from DAUTOM SAS.

'''
This script is designed to take two arguments, [message,level], for the Ignition Logging engine.  Message is the payload published to the MES logger
and the level is the severity of the log to publish to.
Options are fatal, error, warn, info, debug, trace.

'''

def log(loggerName,message,level):
	import system
	logger = system.util.getLogger(loggerName)
	
	if level == 'info':
		logger.info(message)
		
	elif level == 'warn':
		logger.warn(message)
	
	elif level == 'fatal':
		logger.fatal(message)
	
	elif level == 'debug':
		logger.debug(message)
	
	elif level == 'error':
		logger.error(message)
	
	elif level == 'trace':
		logger.trace(message)