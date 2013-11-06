from urllib import request

import info


def setup():
    # set up auth
    auth_handler = request.HTTPBasicAuthHandler()
    auth_handler.add_password(
        realm='MyAnimeList API',
        uri='http://myanimelist.net',
        **info.mal_args)
    opener = request.build_opener(auth_handler)
    # ...and install it globally so it can be used with urlopen.
    request.install_opener(opener)


def ffrequest(url):
    req = request.Request(
        url,
        headers={'User-Agent':
                 'Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20100101 ' +
                 'Firefox/24.0'})
    return request.urlopen(req)
