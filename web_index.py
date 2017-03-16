import morepath
import logging

# logger block:config
FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)

class App(morepath.App):
    pass


@App.path(path='')
class Root(object):
    pass


@App.view(model=Root)
def hello_world(self, request):
    
    #logger block
    d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}
    logger = logging.getLogger('tcpserver')
    logger.warning('Protocol problem: %s', 'connection reset', extra=d)

    return "Hello world!"


if __name__ == '__main__':
    morepath.run(App())