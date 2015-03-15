
### WTF configuration ###
WTF_CSRF_ENABLED = True   #activates CSRF prevention
                          # http://en.wikipedia.org/wiki/Cross-site_request_forgery     
SECRET_KEY = 'change_this_later' #only needed when CSRF is enabled
                                #Used to create a token that is used to
                                #validate a form


#### Obsolete? ####
STEAM_API_KEY = "D7BC71E91BD7E9A204C48BD83EFD29BB" 

OPENID_PROVIDERS = [ 
    {'name': 'Steam', 'url': 'http://steamcommunity.com/openid'}
    ]