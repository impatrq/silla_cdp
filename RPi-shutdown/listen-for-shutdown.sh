#! /bin/sh

### BEGIN INIT INFO
# Provides: 		listen-for-shutdown.py
# Required-Start:	$remote_fs $syslog
# Required-Stop:	$remote_fs $syslog
# Default-Start:	2 3 4 5
# Default-Stop:		0 1 6
### END INIT INFO

case "$1" in
start)
echo "Starting listen-for-shutdown.py"
python /usr/local/bin/listen-for-shutdown.py &
;;
stop)
echo "Stopping listen-for-shutdown.py"
pkill -f /usr/local/bin/listen-for-shutdown.py &
;;
*)
echo "Uso: /etc/init.d/listen-for-shutdown.sh {start|stop}"
exit 1
;;
esac
exit 0
