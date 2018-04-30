import gps

session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

while True:

	report = session.next()
	if report['class'] == 'TPV':
		if hasattr(report, 'time'):
			print report.time
