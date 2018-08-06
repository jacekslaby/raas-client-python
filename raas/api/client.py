


class ClientV1(object):
    '''ClientV1 provides basic access to RAAS API.
    
    Instances of this class can be used like this:
    client = api.ClientV1('http://localhost:8080/')
    alarm = client.get_alarm('dummy_notification_identifier')
    '''
    
    def __init__(self, base_url='https://api.raas.com/'):
        '''
        :param base_url str: A URL to RAAS service.
        '''
        self._base_url = base_url
    
    def get_alarm(self, notif_id):
        pass

            
    def put_alarm(self, notif_id, alarm):
        pass
