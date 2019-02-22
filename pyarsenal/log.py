"""
This module contains Log API functions.
"""
from pyarsenal.objects import Log

def create_log(
        self,
        application,
        level,
        message):
    """
    Generate a log on the teamserver.
    """
    self.call(
        'CreateLog',
        application=application,
        level=level,
        message=message,
    )

    return True

def list_logs(
        self,
        application=None,
        since=None,
        include_archived=None,
        levels=None):
    """
    List logs from the teamserver, optionally filtering.
    """
    resp = self._list_logs_raw(application, since, include_archived, levels) # pylint: disable=protected-access

    return [Log(log_data) for log_data in resp['logs']]

def _list_logs_raw(self, application, since, include_archived, levels):
    """
    Returns the raw response of the ListLogs API call.
    """
    return self.call(
        'ListLogs',
        application=application,
        since=since,
        include_archived=include_archived,
        levels=levels,
    )
