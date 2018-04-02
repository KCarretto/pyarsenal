"""
This module contains Log API functions.
"""
from .exceptions import parse_error
from .objects import Log

def create_log(
        self,
        application,
        level,
        message):
    """
    Generate a log on the teamserver.
    """
    resp = self.call(
        'CreateLog',
        application=application,
        level=level,
        message=message)

    if resp.get('error', True):
        parse_error(resp)

def list_logs(
        self,
        application=None,
        since=None,
        include_archived=None):
    """
    List logs from the teamserver, optionally filtering.
    """
    resp = self._list_logs_raw(application, since, include_archived) # pylint: disable=protected-access

    if resp.get('error', True):
        parse_error(resp)

    return [Log(log_data) for log_data in resp['logs']]

def _list_logs_raw(self, application, since, include_archived):
    """
    Returns the raw response of the ListLogs API call.
    """
    return self.call(
        'ListLogs',
        application=application,
        since=since,
        include_archived=include_archived
    )
