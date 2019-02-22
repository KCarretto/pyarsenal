"""
This module contains Agent API functions.
"""
from pyarsenal.objects import Agent

def register_agent(self, agent_version, supported_actions):
    """
    Register an agent with the teamserver.
    """
    self.call(
        'RegisterAgent',
        agent_version=agent_version,
        supported_actions=supported_actions,
    )
    return True

def get_agent(self, agent_version):
    """
    Fetch agent information from the teamserver.
    """
    resp = self.call(
        'GetAgent',
        agent_version=agent_version,
    )
    return Agent(resp['agent'])

def list_agents(self):
    """
    Retrieve a list of agents from the teamserver.
    """
    resp = self.call(
        'ListAgents'
    )
    return [Agent(agent) for agent in resp['agents']]

def unregister_agent(self, agent_version):
    """
    Remove an agent registration from the teamserver.
    """
    self.call(
        'UnregisterAgent',
        agent_version=agent_version
    )
