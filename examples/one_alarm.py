
# For now let's avoid complexity of installing a package.  (i.e. we just import the API module from filesystem)
import os
path = os.path.abspath('..')
os.sys.path.append(path)

# From logging we want to see INFO's.
import logging.config
logging_conf_file = 'logging.conf'
if os.path.isfile(logging_conf_file):
    logging.config.fileConfig(logging_conf_file)

# Helper function to "pretty" print alarms. (i.e. sorted by key name)
def sorted_dict_repr(d):
    import json
    return json.dumps(d, sort_keys=True)
    


# The example client code starts here.
#
    
# We need access to RAAS API.
from raas import api

# RAAS API is available as an HTTP service, se we need its base URL.
#
# In case we have a local dev server we use:
# base_url = 'http://localhost:8080/'
#
# Otherwise, in case of a vagrantbox, we check 'netstat -rn', and we use gateway address like this:
# base_url = 'http://10.0.2.2:8080/'
#
base_url = 'http://10.0.2.2:8080/'

# Let's create a local wrapper for the remote API.
client = api.ClientV1(base_url)

# Our sample alarm:
sample_notification_identifier = 'eric2g:pl-wawa:34566'
sample_alarm = {
    'notification_identifier': sample_notification_identifier,
    'perceived_severity': 1,
    'additional_text': 'Sample alarm created for demo purpose.'
}

# Let's retrieve the alarm. Maybe it exists already ?
#
print('Getting alarm...')
returned_alarm = client.get_alarm(sample_notification_identifier)
print('Existing alarm: ', sorted_dict_repr(returned_alarm))
print()

if returned_alarm:
    # Such alarm already exists.  (most likely it was created when we run this client code a moment ago)
    # Let's modify our sample alarm to make it look a bit different.
    #
    severity = returned_alarm.get('perceived_severity')    # perceived_severity may not exist so we use get()
    if not isinstance(severity, int):
        severity = 1
    else:
        severity = (int(severity) + 1) % 6     # allowed values are 0..5
        
    sample_alarm['perceived_severity'] = severity

# Let's save our alarm.
#
print('Saving alarm...')
print('Saving alarm:   ', sorted_dict_repr(sample_alarm))
client.put_alarm(sample_notification_identifier, sample_alarm)
print('Saved.')
print()

# Let's retrieve the alarm.
#
print('Getting saved alarm...')
returned_alarm = client.get_alarm(sample_notification_identifier)
print('Returned alarm: ', sorted_dict_repr(returned_alarm))
print()


