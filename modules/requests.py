from requests_futures.sessions import FuturesSession
import sys, logging

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s %(message)s',)

def __exception_handler__(s, resp):
    if not resp.ok:
        logging.info('Warning! HTTP {0} Request to \'{1}\' failed with response status {2}'.format(resp.request.method,resp.url,resp.status_code,))

class Communicator():
    '''Asynchronous HTTP Request communicator'''
    
    def __init__(self,workers=10):
        self.session = FuturesSession(max_workers=workers)
        
    def get(self,url):
        return self.session.get(url, background_callback=__exception_handler__)

    def post(self,url,data=None):
        if data:
            return self.session.post(url, data, background_callback=__exception_handler__)
        else:
            return self.session.post(url, background_callback=__exception_handler__)
        