import time

import web

def log(type, message, severity=0, uid=0, link=''):
    """Log a system message.
    
    * @param type: The category to which this message belongs.
    * @param message: The message to store in the log.
    * @param severity: The severity of the message. One of the following values:
    *   - WATCHDOG_NOTICE = 0
    *   - WATCHDOG_WARNING = 1
    *   - WATCHDOG_ERROR = 2
    * @param link: A link to associate with the message.
    """
    referer = web.ctx.env.get('HTTP_REFERER','')
    location = web.ctx.homedomain + web.ctx.fullpath
    timestamp = int(time.time())
    hostname = web.ctx.env['REMOTE_ADDR']
    web.query("INSERT INTO watchdog (uid, type, message, severity, link, location, referer, hostname, timestamp) VALUES \
        ($uid, $type, $message, $severity, $link, $location, $referer, $hostname, $timestamp)", vars=locals())
