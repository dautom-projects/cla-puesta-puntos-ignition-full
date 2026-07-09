def log(message,level):
	import system
	logger = system.util.getLogger('PAPO_Logger')
	
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