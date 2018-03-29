"""
This module contains Action API functions.
"""
from .arsenal import ArsenalObject
from .action import Action
from .exceptions import parse_error

class Session(ArsenalObject):
    """
    This object represents a Session from the teamserver.
    """

    session_id = None
    target_name = None
    status = None
    timestamp = None
    config = None

    @staticmethod
    def create_session( #pylint: disable=too-many-arguments
            mac_addrs,
            servers=None,
            interval=None,
            interval_delta=None,
            config_dict=None,
            facts=None):
        """
        This method creates an Session, and returns it's session_id.
        """
        resp = ArsenalObject._call(
            'CreateSession',
            mac_addrs=mac_addrs,
            servers=servers,
            interval=interval,
            interval_delta=interval_delta,
            config_dict=config_dict,
            facts=facts)

        if resp.get('error', True):
            parse_error(resp)

        return resp['session_id']

    @staticmethod
    def get_session(session_id):
        """
        Returns an Session object from the teamserver.
        """
        resp = Session._get_session_raw(session_id)
        if resp.get('error', True):
            parse_error(resp)

        return Session(resp['session'])

    @staticmethod
    def _get_session_raw(session_id):
        """
        Returns the raw response of the GetSession API call.
        """
        return ArsenalObject._call(
            'GetSession',
            session_id=session_id)

    @staticmethod
    def session_checkin(session_id, responses=None, config=None, facts=None):
        """
        Checks in a Session. Optionally you may include any
        responses from Actions that were completed. The API call
        will return any data needed for the Session, including
        new actions or configuration changes.
        """
        resp = ArsenalObject._call(
            'SessionCheckIn',
            session_id=session_id,
            responses=responses,
            config=config,
            facts=facts)

        if resp.get('error', True):
            parse_error(resp)

        actions = resp.get('actions', [])

        return {
            'session_id': resp['session_id'],
            'actions': [Action(action) for action in actions]
        }

    @staticmethod
    def update_session_config(session_id, **kwargs):
        """
        Updates a Session's configuration.
        Settings include interval, interval_delta, servers, config_dict.
        """
        interval = kwargs.get('interval', None)
        interval_delta = kwargs.get('interval_delta', None)
        servers = kwargs.get('servers', None)
        config_dict = kwargs.get('config_dict', None)

        resp = ArsenalObject._call(
            'UpdateSessionConfig',
            session_id=session_id,
            interval=interval,
            interval_delta=interval_delta,
            servers=servers,
            config_dict=config_dict
        )

        if resp.get('error', True):
            parse_error(resp)

        return resp.get('config', {})

    @staticmethod
    def list_sessions():
        """
        Returns a list of Session Objects from the teamserver.
        """
        resp = Session._list_sessions_raw()

        if resp.get('error', True):
            parse_error(resp)

        return [Session(session) for session_id, session in resp['sessions'].items()]

    @staticmethod
    def _list_sessions_raw():
        """
        Returns the raw response of the ListSessions API call.
        """
        return ArsenalObject._call(
            'ListSessions'
        )
