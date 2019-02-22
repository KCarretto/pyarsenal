"""
This module contains Auth API functions.
"""
from pyarsenal.objects import User, Role, APIKey

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

def create_api_key(self, allowed_api_calls=None, user_context=None):
    """
    Create an API Key for the current user.

    Only an administrator may specify a user_context.
    """
    resp = self.call(
        'CreateAPIKey',
        allowed_api_calls=allowed_api_calls,
        user_context=user_context,
    )

    return resp['api_key']

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

def get_role(self, role_name):
    """
    Retrieve information about a role.
    """
    resp = self.call(
        'GetRole',
        role_name=role_name,
    )
    return Role(resp['role'])

def get_current_context(self):
    """
    Retrieve the currently authenticated username.
    """
    resp = self.call(
        'GetCurrentContext'
    )
    return User(resp['user'])

def list_users(self, include_roles=None, include_api_calls=None):
    """
    Return a list of users with information.
    """
    resp = self.call(
        'ListUsers',
        include_roles=include_roles,
        include_api_calls=include_api_calls,
    )
    return [User(user) for user in resp['users']]

def list_api_keys(self, user_context=None):
    """
    Return a list of API keys registered for a user.
    """
    resp = self.call(
        'ListAPIKeys',
        user_context=user_context
    )
    return [APIKey(key) for key in resp['api_keys']]

def list_roles(self):
    """
    Return a list of roles.
    """
    resp = self.call(
        'ListRoles',
    )

    return [Role(role) for role in resp['roles']]

def delete_user(self, username):
    """
    Remove a user.
    """
    self.call(
        'DeleteUser',
        username=username
    )
    return True

def delete_role(self, role_name):
    """
    Delete a role.
    """
    self.call(
        'DeleteRole',
        role_name=role_name
    )
    return True

def revoke_api_key(self, api_key, user_context=None):
    """
    Revoke an API key.
    """
    self.call(
        'RevokeAPIKey',
        api_key=api_key,
        user_context=user_context,
    )
    return True
