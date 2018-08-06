
# Note: In order to avoid ERROR "ImportError: No module named 'raas'" please read:
#    https://stackoverflow.com/questions/10253826/path-issue-with-pytest-importerror-no-module-named-yadayadayada#34140498
#  i.e.: "The least invasive solution is adding an empty file named conftest.py [...]"
#



from raas import api
import json
import os
import pytest
import requests_mock

# Our sample alarm:
sample_notification_identifier = 'eric2g:pl-wawa:34566'
sample_alarm = {
    'notification_identifier': sample_notification_identifier,
    'perceived_severity': 1,
    'additional_text': 'Sample alarm created for demo purpose.'
}
sample_alarm_json = json.dumps(sample_alarm)

# URL of our sample web service:
apiurl = 'http://foo.raas.api.org'


@pytest.fixture()
def client():
    '''create a new client instance for each run of a test_* method'''
    return api.ClientV1(apiurl)

def test_get_alarm(client):
    '''verify that API get_alarm forwards request to an HTTP web service with correct parameters'''
    url = apiurl + 'v1/rawalarms?notificationIdentifier=' + sample_notification_identifier
    
    with requests_mock.Mocker() as m:
        # Let's register what web service will return when client uses GET method on it.
        m.get(url, text=sample_alarm_json, status_code=200)
        
        # Let's run client.get_alarm.
        returned_alarm = client.get_alarm(sample_notification_identifier)
        
        # Let's check that web service was used and a returned result is correct.
        assert m.called
        assert sample_alarm == returned_alarm
    
    
def test_put_alarm(client):
    '''verify that API put_alarm forwards request to an HTTP web service with correct parameters'''
    url = apiurl + 'v1/rawalarms/' + sample_notification_identifier
    
    with requests_mock.Mocker() as m:
        # Let's register what web service will return when client uses PATCH method on it.
        m.patch(requests_mock.ANY)   # We allow any request. (because in requests_mock library I do not see any other possibility...)
        
        # Let's run client.put_alarm
        client.put_alarm(sample_notification_identifier, sample_alarm)
        
        # Let's check that web service was used.
        assert m.called == 1
        assert m.request_history[0].method == 'PATCH'
        assert m.request_history[0].url == url
        assert m.request_history[0].text == sample_alarm_json
        
    