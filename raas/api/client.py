
import json
import logging
import requests

log = logging.getLogger(__name__)

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
        '''Get an alarm for the given Notification Identifier.
        :param notif_id str: A Notification Identifier
        :returns: dict object (representing JSON content of an Alarm) or None if Alarm does not exist
        :raises requests.exceptions.RequestException: On API error.
        '''
        
        url = self._base_url + 'v1/rawalarms?notificationIdentifier=' + notif_id

        log.info('get_alarm(%s): from: %s', notif_id, url)
        response = requests.get(url)

        if response.ok:

            if not response.content:
                # It means alarm does not exist.
                return None
            else:
                # RAAS returns alarms as JSON.
                #
                alarm_as_dict = response.json()
                
                attributes_count = len(alarm_as_dict)
                log.info('get_alarm(%s): success: returned %s attributes', notif_id, attributes_count)
            
                return alarm_as_dict
            
        else:
            log.info('get_alarm(%s): failure', notif_id)
            
            # If failure, print the resulting http error code with description
            response.raise_for_status()

            
    def put_alarm(self, notif_id, alarm):
        '''Put an alarm for the given Notification Identifier.
        :param notif_id str: A Notification Identifier
        :param alarm dict: key-value pairs defining names and values of attributes of the alarm
        '''
        url = self._base_url + 'v1/rawalarms/' + notif_id
        
        log.info('put_alarm(%s): to: %s', notif_id, url)
        
        response = requests.patch(url, json.dumps(alarm))
        
        if response.ok:
            log.info('put_alarm(%s): success', notif_id)
        else:
            log.info('put_alarm(%s): failure', notif_id)
            
            # If failure, print the resulting http error code with description
            response.raise_for_status()
