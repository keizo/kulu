
import md5
import time

from web import form
import web

from drupy import *
import glbl
import loader
inc = loader.import_('includes')
mod = loader.import_('modules')



urls = (
    '/user','user',
    '/user/(.+)','user_profile',
    '/register','register',
    '/retrieve_pass','retrieve_pass',
    '/logout','logout',
    '/admin/user/access','admin_access',
    '/denied','access_denied',
    )
perms = (
    'administer access control', 
    'administer users', 
    'view user profiles', 
    'change own username',
    )
#
## CONTROLLERS
#    
class user(page):
    def GET(self):
        page = self.page
        if page.user.uid:
            web.redirect('/user/'+page.user.name)
        form = form_login()
        web.render('login.html')
        
    def POST(self):
        page = self.page
        form = form_login()
        if form.validates():
            # successful login info
            data = form.d
            login(email=data.email,remember_me=data.remember_me)
            web.redirect('/user')
        else:
            web.render('login.html')
        
class user_profile(page):
    @access('view user profiles')
    def GET(self,name):
        print name, 'user page'
        
class register(page):
    def GET(self):
        page = self.page
        if page.user.uid:
            web.redirect('/user')
        
        form = form_register()
        captcha = ''
        if inc.has_key('recaptcha'):
            if glbl.variable['recaptcha_private_key'] and \
               glbl.variable['recaptcha_public_key']:
                captcha = inc.recaptcha.displayhtml(
                          glbl.variable['recaptcha_public_key'])
            else:
                page.message = 'Error: ReCaptcha installed, but the api keys \
                                are not set.  Please notify the administrator'
                page.message += ' ' + glbl.variable['email_admin']
                                
        web.render('register.html')

    def POST(self):
        page = self.page
        if page.user.uid:
            web.redirect('/user')
        
        form = form_register()
        captcha = ''
        success = False
        i = web.input()
        if form.validates():
            if inc.has_key('recaptcha'):  # recaptcha installed
                captcha = inc.recaptcha.submit(i.recaptcha_challenge_field, 
                                        i.recaptcha_response_field, 
                                        glbl.variable['recaptcha_private_key'], 
                                        web.ctx.ip)
                if captcha.is_valid:
                    success = True
                elif captcha.error_code == 'incorrect-captcha-sol':
                    captcha = inc.recaptcha.displayhtml(
                              glbl.variable['recaptcha_public_key'])
                    page.message = "Please fill out the \
                                    word verification correctly."
                else:  # Recaptcha is broken
                    # TODO: file a watchdog error, tell the user something useful
                    print 'captcha is broken'
            else:  # recaptcha not installed
                # TODO: maybe require email activation confirmation 
                # since there is no captcha installed
                success = True
        else:  # Didn't work.
            if inc.has_key('recaptcha'):
                captcha = inc.recaptcha.displayhtml(
                          glbl.variable['recaptcha_public_key'])
        if success:
            new_user(i.name, i.password, i.email)
            web.redirect('/user')
            # TODO: pass a message saying it was a success and to now login
            # use session to do this?
        else:
            web.render('register.html')
        
class logout:
    def GET(self):
        inc.session.regenerate()
        web.redirect('/')

class admin_access(page):
    def GET(self):
        page = self.page
        form = form_admin_access()
        content = '<form method="post">' + form.render() + '<input type="submit" /></form>'
        web.render('generic.html')

    def POST(self):
        roles = {}
        for rid in glbl.role:
            roles['role_'+str(rid)] = []
        roles = web.input(**roles)

        for rid in roles:
            key = int(rid.lstrip('role_'))
            if glbl.perm.has_key(key):
                print 'new permissions set'
                glbl.perm[key] = ', '.join(roles[rid])
        # TODO: put a message to show that it was updated.
        web.redirect('/admin/user/access')

class access_denied(page):
    def GET(self):
        page = self.page
        page.message = "Access denied, please login."
        form = form_login()
        web.render('login.html')
        
    def POST(self):
        # This is almost identical to the POST in the user class
        # Could get rid of this function it by changing  where the 
        # form posts to.
        page = self.page
        form = form_login()
        if form.validates():
            # successful login
            login(email=form.d.email)
            if web.input().has_key('url'):
                web.redirect(web.input().url)
            web.redirect('/user')
        else:
            self.message = 'Invalid login, try again.'
            web.render('login.html')
#
## FORMS
#

# Override the form class for the crazy admin/user/access form
# TODO: Maybe it should just use a template to render!? cause this is ugly.
class Form(form.Form):
    def render(self):
        out = ''
        out += self.rendernote(self.note)
        out += '<table>\n'
        out += '<tr>'
        # this attrs['role_name'] doesn't work stupid
        prev = self.inputs[0].value
        i=0
        while self.inputs[i].value == prev:
            out += '<td></td><th>'
            out += glbl.role[int(self.inputs[i].name.lstrip('role_'))]
            out += '</th>'
            prev = self.inputs[i].value
            i += 1
        out += '<td></td></tr><tr>'

        prev = ''
        for i in self.inputs:
            if i.value != prev:
                out += '</tr>'
                out += '   <tr><th><label for="%s">%s</label></th>' % (i.id, i.description)
            out += "<td>"+i.pre+i.render()+i.post+"</td>"
            out += '<td id="note_%s">%s</td>\n' % (i.id, self.rendernote(i.note))
            prev = i.value
        out += '</tr>'
        out += "</table>"
        return out

def form_admin_access():
    # TODO: rewrite this without the db query, since the role and permission
    # tables are kept in memory at all times (in glbl).
    # TODO: the perms are grouped by module, so put a title with each group
    query = web.query('SELECT * FROM role r INNER JOIN permission p \
            ON r.rid=p.rid ORDER BY r.name')

    fields = []
    roles = []
    for role in query:
        role.perm = role.perm.split(', ')
        roles.append(role)

    for key in mod:
        if hasattr(mod[key],'perms'):
            perms = list(mod[key].perms)
            perms.sort()
            for perm in perms:
                for role in roles:
                    if perm in role.perm: checked = True
                    else: checked = False
                    fields.append(form.CheckboxList('role_'+str(role.rid), 
                        value=perm, checked=checked, description=perm))
    fields = tuple(fields)
    return Form(*fields)

def _name_valid(name):
    query = web.query('SELECT * FROM users WHERE name=$name',vars=locals())
    try: 
        user = query[0]
    except IndexError:
        user = False
    if not user: return True
    else: return False
    
def _email_valid(email):
    query = web.query('SELECT * FROM users WHERE email=$email',vars=locals())
    try: 
        user = query[0]
    except IndexError:
        user = False
    if not user: return True
    else: return False

form_register = form.Form(
    form.Textbox('name',
            form.notnull,
            form.Validator('Your name must be 4 characters or more.', lambda x:len(x)>3),
            form.Validator('Name already taken, please choose another.', 
                _name_valid),
            description='Display Name:',
            size='40',
            post='<p>Your preferred display name.  This will be \
                permanent and set your profile url to \
                http://www.ocpaddler.com/user/(name)</p>'),
    form.Textbox('email',
            form.notnull,
            form.regexp('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$','Not a valid email address.'),
            form.Validator('This email address was already registered. \
                Have you lost your password?', _email_valid),
            description='Email address:',
            size='40',
            post='<p>A valid e-mail address that you use to login with.  \
                The e-mail address is not made public and will only be used \
                if you wish to receive a new password or \
                notifications by e-mail.</p>'),
    form.Password('password',
            form.notnull,
            form.Validator("Password must be 4 characters or more.", lambda x:len(x)>3),
            description='Password:',
            size='40',
            post='<p>Minimum of 4 characters.</p>'),
    )


def _login_valid(form):
    pass_submitted = md5.new(form.password).hexdigest()
    try:
        user = web.select('users',where='email = $form.email',vars=locals())[0]
    except:
        return False
    if user.password == pass_submitted:
        return True
    return False
    
form_login = form.Form(
    form.Textbox('email',
        form.notnull,
        form.regexp('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$','Not a valid email address.'),
        description='Email:',
        size='40',
        ),
    form.Password('password',
        form.notnull,
        description='Password:',
        size='40',
        ),
    form.Checkbox('remember_me',
        description='Remember Me:',
        ),
    validators = [form.Validator("Incorrect login.", _login_valid)]
    )
        
#
## FUNCTIONS
#

def anonymous_user(sid = ''):
    return web.storify({},uid = 0,hostname = web.ctx.env['REMOTE_ADDR'], 
        roles={glbl.constant.anonymous_role_id:'anonymous user'},sid=sid,
        session_in_db=False, remember_me=True)

def login(email='',user='',remember_me=''):
    # TODO: implement login by username in addition to email
    r = '0'
    if remember_me:
        r = '1'
    login_time = int(time.time())
    user = web.select('users',where='email = $email',vars=locals())[0]
    #print user
    web.transact()
    web.query("UPDATE users SET login = $login_time, remember_me = $r \
        WHERE uid = $user.uid", vars=locals())
    #print user.uid
    inc.session.regenerate(uid=user.uid)
    web.commit()

def new_user(name, password, email):
    pw = md5.new(password).hexdigest()
    now = int(time.time())
    return web.insert('users', name=name, password=pw, email=email, 
                      created=now, init=email)
    
    