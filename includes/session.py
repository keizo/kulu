
"""User session handling functions."""
# standard library imports
import time
import random

import sha

# webpy imports
import web

# drupy imports
from drupy import *
import glbl
import loader
mod = loader.import_('modules')


def read():
    """returns a user storage object associated with the session"""
    cookies = web.cookies()
    if not hasattr(cookies,'_SID_'): 
        # this is the case of first time visitors and clients that 
        # don't store cookies (eg. web crawlers).
        print 'not capable of cookies or a brand new user, so i am adding one'
        new_sid = _generate_id()
        user = mod.user.anonymous_user(sid=new_sid)
        return user

    #Otherwise, if the session is still active, we have a record of the client's session in the database.
    sid = cookies._SID_
    query = web.query("SELECT u.*, s.* FROM users u INNER JOIN sessions s \
                      ON u.uid = s.uid WHERE s.sid = $sid", vars=locals())
    print web.query("SELECT u.*, s.* FROM users u INNER JOIN sessions s \
            ON u.uid = s.uid WHERE s.sid = $sid", vars=locals(), _test=True)
    try:
        user = query[0]
    except IndexError:
        # most likely this means they have a cookie, but are anonymous. 
        # so we'll make an anoymous user using their sid
        # or their cookie could have expired or something, i don't really understand
        #new_sid = _generate_id()
        query = web.query("SELECT * FROM sessions s \
                           WHERE s.sid = $sid", vars=locals())
        try:
            query[0]
            user = mod.user.anonymous_user(sid=sid)
        except IndexError:
            # their cookie is fucked up, assume they are first time visitors
            print 'fucked up cookie, assuming first time visitor'
            new_sid = _generate_id()
            user = mod.user.anonymous_user(sid=new_sid)
            return user
    
    if user.uid > 0:
        # they are an authenticated user
        # Add roles to user
        user.roles = {glbl.constant.authenticated_role_id:'authenticated user'}
        result = web.query("SELECT r.rid, r.name FROM role r INNER JOIN users_roles ur \
                           ON ur.rid = r.rid WHERE ur.uid = $user.uid", vars=locals())
        for role in result:
            user.roles[role.rid] = role.name
    else:
        # they are anonymous, so make sure they keep the sid from the cookie and not from the
        # users table that was queried to make the user object
        user = mod.user.anonymous_user(sid=sid)
        # They have a session id in the db, so we set that before
        # returning the user.
    user.session_in_db = True
    return user


def write(key, value='',user=None):
    """updates the users cookie and session in the database"""
    
    if user.remember_me:
        expires = glbl.constant.remember_me_length
    else: expires = ''
    
    if user is None: 
        user = mod.user.anonymous_user(sid=key)
    
    if not web.cookies():
        # If the client doesn't have a session cookie, set one and do nothing else.
        # We could also insert into the sessions table, but we do not by design.
        # This keeps crawlers out of the session table so they don't inflate the 
        # "Who's Online" count.  The drawback is it also keeps out first time 
        # users who only view one page.
        web.setcookie("_SID_",key,expires=expires)
    
    elif web.cookies() and user.session_in_db is False:
        # Insert session data only when the browser sends a cookie and is not 
        # in the sessions table. 
        sid = key
        cache = 0
        hostname = web.ctx.env['REMOTE_ADDR']
        timestamp = int(time.time())
        print web.query("INSERT INTO sessions (sid, uid, cache, hostname, session, timestamp) \
            VALUES ($sid, $user.uid, $cache, $hostname, $value, $timestamp)", vars=locals(), _test=True)
        web.query("INSERT INTO sessions (sid, uid, cache, hostname, session, timestamp) \
            VALUES ($sid, $user.uid, $cache, $hostname, $value, $timestamp)", vars=locals())
        web.setcookie("_SID_",sid,expires=expires)
    else:
        # We have their session in the database, now update it.
        sid=key
        cache = 0
        hostname = web.ctx.env['REMOTE_ADDR']
        timestamp = int(time.time())
        web.query("UPDATE sessions SET uid = $user.uid, cache = $cache, hostname = $hostname, \
            session = $value, timestamp = $timestamp WHERE sid = $sid", vars=locals())
        web.setcookie("_SID_",sid,expires=expires)
        
        #TODO: this can be an expensive query. Perhaps only execute it every x minutes. 
        #      Requires investigation into cache expiration.
        if user.uid:
            web.query("UPDATE users SET access = $timestamp WHERE uid = $user.uid", vars=locals())

def _generate_id():
    '''implicit session id generator
    "hashes" ip, time, seed ...'''
    seed = '%s %s %s %s' % (random.random(), time.time(), web.ctx.ip, glbl.variable['site_name'])

    return sha.new(seed).hexdigest()
        
def regenerate(uid=0):
    """Called when an anonymous user becomes authenticated or vice-versa."""
    old_session_id = web.cookies()._SID_
    new_session_id = _generate_id()
    web.setcookie("_SID_",new_session_id)
    #uid = int(uid)
    #print web.query("UPDATE sessions SET uid = '$uid', sid = $new_session_id WHERE sid = $old_session_id", vars=locals(),_test=True)
    web.query("UPDATE sessions SET uid = $uid, sid = $new_session_id WHERE sid = $old_session_id", vars=locals())

def count(timestamp = 0, anonymous = 'both'):
    """Returns how many users have sessions. Can count either 
    anonymous sessions, authenticated sessions, or both.
    
    * @param int $timestamp
    *   A Unix timestamp representing a point of time in the past.
    *   The default is 0, which counts all existing sessions.
    * @param int $anonymous
    *   TRUE counts only anonymous users.
    *   FALSE counts only authenticated users.
    *   Default value will return the count of both authenticated and anonymous users.
    * @return  int
    *   The number of users with sessions.
    """
    if anonymous is 'both': query = ''
    elif anonymous is True: query = ' AND uid = 0'
    elif anonymous is False: query = ' AND uid > 0'
    return web.query('SELECT COUNT(sid) AS count FROM sessions \
                    WHERE timestamp >= $timestamp'+query, vars=locals())[0]

def destroy_sid(sid):
    web.query("DELETE FROM sessions WHERE sid = $sid", vars=locals())

def destroy_uid(uid):
    web.query('DELETE FROM sessions WHERE uid = $uid', vars=locals())

def clean(lifetime=2592000):
    """Delete all sessions older than lifetime
    We could call this on every request, but may as well just do it 
    at some periodic interval. """
    timestamp = int(time.time()) - lifetime
    web.query("DELETE FROM sessions WHERE timestamp < $timestamp", vars=locals())
    return True

