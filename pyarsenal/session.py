"""
This module contains Session API functions.
"""
from pyarsenal.objects import Action, Session

def create_session( #pylint: disable=too-many-arguments
        self,
        target_uuid,
        servers=None,
        interval=None,
        interval_delta=None,
        config_dict=None,
        facts=None,
        agent_version=None,):
    """
    This method creates an Session, and returns it's session_id.
    """
    resp = self.call(
        'CreateSession',
        target_uuid=target_uuid,
        servers=servers,
        interval=interval,
        interval_delta=interval_delta,
        config_dict=config_dict,
        facts=facts,
        agent_version=agent_version,
    )

    return resp['session_id']

def get_session(self, session_id):
    """
    Returns an Session object from the teamserver.
    """
    resp = self._get_session_raw(session_id) # pylint: disable=protected-access

    return Session(resp['session'])

def _get_session_raw(self, session_id):
    """
    Returns the raw response of the GetSession API call.
    """
    return self.call(
        'GetSession',
        session_id=session_id)

def session_checkin(self, session_id, responses=None, config=None, facts=None, public_ip=None):
    """
    Checks in a Session. Optionally you may include any
    responses from Actions that were completed. The API call
    will return any data needed for the Session, including
    new actions or configuration changes.
    """
    resp = self.call(
        'SessionCheckIn',
        session_id=session_id,
        responses=responses,
        config=config,
        facts=facts,
        public_ip=public_ip,)

    actions = resp.get('actions', [])

    return {
        'session_id': resp['session_id'],
        'actions': [Action(action) for action in actions]
    }

def update_session_config(self, session_id, **kwargs):
    """
    Updates a Session's configuration.
    Settings include interval, interval_delta, servers, config_dict.
    """
    interval = kwargs.get('interval', None)
    interval_delta = kwargs.get('interval_delta', None)
    servers = kwargs.get('servers', None)
    config_dict = kwargs.get('config_dict', None)

    resp = self.call(
        'UpdateSessionConfig',
        session_id=session_id,
        interval=interval,
        interval_delta=interval_delta,
        servers=servers,
        config_dict=config_dict
    )

    return resp.get('config', {})

def list_sessions(self):
    """
    Returns a list of Session Objects from the teamserver.
    """
    resp = self._list_sessions_raw() # pylint: disable=protected-access

    return [Session(session) for session_id, session in resp['sessions'].items()]

def _list_sessions_raw(self):
    """
    Returns the raw response of the ListSessions API call.
    """
    return self.call(
        'ListSessions'
    )
