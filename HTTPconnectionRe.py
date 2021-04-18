from requests.packages.urllib3.connectionpool import HTTPConnectionPool
import socks
import socket
import requests
import sys
from bs4 import BeautifulSoup as BS


def _make_request(self, conn, method, url, **kwargs):
        response = self._old_make_request(conn, method, url, **kwargs)
        sock = getattr(conn, 'sock', False)
        if sock:
            setattr(response, 'peer', sock.getpeername())
        else:
            setattr(response, 'peer', None)
        return response


def setup_socks():
        socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
        socket.socket = socks.socksocket
        HTTPConnectionPool._old_make_request = HTTPConnectionPool._make_request
        HTTPConnectionPool._make_request = _make_request


def check_tor_browser():
        try:
                ip = requests.get('http://checkip.dyndns.org').content
                soup = BS(ip, 'html.parser')
                print('[УДАЧНО] VPN TOR браузера работает')
                print(soup.find('body').text)
        except:
                print('Вы не застили TOR браузер! Запустите его, а после запустите скрипт снова!')
                sys.exit()


def checkIP():
        ip = requests.get('http://checkip.dyndns.org').content
        soup = BS(ip, 'html.parser')
        print(soup.find('body').text)

