def get_time_hh_mm_ss(secs):
	"""
	ThisCode is to convert number of seconds into HH:MM:SS format for Table avalability scheduler.
	"""
	from datetime import timedelta
	td_str = str(timedelta(seconds=secs))
	# split string into individual component
	x = td_str.split(':')
	if int(x[0])<10:
		strFinalTime = str("0"+x[0]+":"+x[1]+":"+x[2])
	else:
		strFinalTime = str(x[0]+":"+x[1]+":"+x[2])
	return strFinalTime
