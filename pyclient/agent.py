"""
This module contains Agent API functions.
"""
from .objects import Agent

def register_agent(self, agent_version, supported_actions):
    """
    Register an agent with the teamserver.
    """
    self.call(
        agent_version=agent_version,
        supported_actions=supported_actions,
    )
    return True

def get_agent():
    pass

def list_agents():
    pass

def unregister_agent():
    pass
