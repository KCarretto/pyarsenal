"""
This module contains Auth API functions.
"""
from .objects import User, Role, APIKey

def create_user(self, username, password):
    """
    This method creates a user.
    """
    self.call(
        'CreateUser',
        username=username,
        password=password,
    )

    return True

def create_api_key(self, allowed_api_calls, user_context=None):
    """
    Create an API Key for the current user.

    Only an administrator may specify a user_context.
    """
    resp = self.call(
        'CreateAPIKey',
        allowed_api_calls=allowed_api_calls,
        user_context=user_context,
    )

    return APIKey(resp['api_key'])

def create_role(self, name, allowed_api_calls, users):
    """
    Create a Role.
    """
    self.call(
        'CreateRole',
        name=name,
        allowed_api_calls=allowed_api_calls,
        users=users,
    )

    return True

def update_user_password(self, current_password, new_password, user_context=None):
    """
    Change the user's password.

    Only an administrator may specify a user_context.
    """
    self.call(
        'UpdateUserPassword',
        current_password=current_password,
        new_password=new_password,
        user_context=user_context
    )

    return True

def update_role_permissions(self, role_name, allowed_api_calls):
    """
    Override a role's permissions with a new set.
    """
    self.call(
        'UpdateRolePermissions',
        role_name=role_name,
        allowed_api_calls=allowed_api_calls,
    )

    return True

def add_role_member(self, role_name, username):
    """
    Add a user to a role.
    """
    self.call(
        'AddRoleMember',
        role_name=role_name,
        username=username
    )

    return True

def remove_role_member(self, role_name, username):
    """
    Remove a user from a role.
    """
    self.call(
        'RemoveRoleMember',
        role_name=role_name,
        username=username
    )

    return True

def get_user(self, username, include_roles=False, include_api_calls=True):
    """
    Retrieve user information.
    """
    resp = self.call(
        'GetUser',
        username=username,
        include_roles=include_roles,
        include_api_calls=include_api_calls,
    )

    return User(resp['user'])

def get_current_context(self):
    """
    Retrieve the currently authenticated username.
    """
    resp = self.call(
        'GetCurrentContext'
    )
    return resp['username']
