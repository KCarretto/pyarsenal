"""
This module contains exceptions raised by the pyclient library.
"""
from functools import wraps

class ServerConnectionError(Exception):
    """
    Raised when the client cannot connect to the teamserver.
    """
    pass

class ServerInternalError(Exception):
    """
    Raised when the teamserver encounters an unhandled error, and does not return proper json.
    """
    pass

class APIException(Exception):
    """
    Raised when the teamserver API returns an error.
    """
    name = 'unhandled-exception'

class ActionUnboundSession(APIException):
    """
    This exception is raised when the Session that an Action was assigned to no longer exists.
    """
    name = 'action-unbound-session'

class SessionUnboundTarget(APIException):
    """
    This exception is raised when a Session's Target does not exist.
    """
    name = 'session-unbound-target'

class CannotCancelAction(APIException):
    """
    This exception is raised when an attempt to cancel an action is made
    but cannot be completed.
    """
    name = 'cannot-cancel-action'

class CannotAssignAction(APIException):
    """
    This exception is raised when an Action is unable to be assigned to the given session_id.
    """
    name = 'cannot-assign-action'

class CannotBindAction(APIException):
    """
    This exception is raised when an Action is attempted to be assigned to a
    Target that does not exist.
    """
    name = 'cannot-bind-action'

class ActionSyntaxError(APIException):
    """
    This exception is raised when an error was encountered while parsing an action string.
    """
    name = 'action-syntax-error'

class MembershipError(APIException):
    """
    This exception is raised when an attempt to modify group membership is made
    and cannot be completed.
    """
    name = 'membership-error'

class ValidationError(APIException):
    """
    Raised when data sent to the teamserver does not meet constraints.
    """
    name = 'validation-error'

class ResourceNotFound(APIException):
    """
    Raised when a resource was not found.
    """
    name = 'resource-not-found'

class ResourceAlreadyExists(APIException):
    """
    Raised when a resource already exists.
    """
    name = 'resource-already-exists'

class MissingParameter(APIException):
    """
    Raised when an API call was not sent a required parameter.
    """
    name = 'missing-parameter'

class InvaidUser(APIException):
    """
    Raised when the username sent to the teamserver is not a valid user.
    """
    name = 'invalid-user'

class InvalidCredentials(APIException):
    """
    Raised when the credentials sent to the teamserver are invalid.
    """
    name = 'invalid-credentials'

class InvalidAPIKey(APIException):
    """
    Raised when an invalid api key was sent.
    """
    name = 'invalid-api-key'

class PermissionDenied(APIException):
    """
    Raised when the user does not have permission to execute a function.
    """
    name = 'permission-denied'

def parse_error(data):
    """
    Parse an error response and raise the appropriate exception.
    """
    errors = {
        APIException.name: APIException,
        ActionUnboundSession.name: ActionUnboundSession,
        SessionUnboundTarget.name: SessionUnboundTarget,
        CannotCancelAction.name: CannotCancelAction,
        CannotAssignAction.name: CannotAssignAction,
        CannotBindAction.name: CannotBindAction,
        ActionSyntaxError.name: ActionSyntaxError,
        MembershipError.name: MembershipError,

        ValidationError.name: ValidationError,
        ResourceNotFound.name: ResourceNotFound,
        ResourceAlreadyExists.name: ResourceAlreadyExists,
        MissingParameter.name: MissingParameter,

        InvaidUser.name: InvaidUser,
        InvalidCredentials.name: InvalidCredentials,
        InvalidAPIKey.name: InvalidAPIKey,
        PermissionDenied.name: PermissionDenied,
    }
    error_type = data.get('error_type', APIException.name)

    exception = errors.get(error_type, APIException)

    raise exception(data.get('description', 'No description available.'))

def handle_exceptions(func):
    """
    This function can be used as a decorator to wrap functions.
    Wrapped functions will be surrounded in a try / except block that
    includes necessary error handling, including logging and
    returning error responses.
    """

    @wraps(func)
    def wrapper(*args, **kwargs): #pylint: disable-all
        """
        This uses the func tools library to wrap a function.
        """
        try:
            retval = func(*args, **kwargs)
            return retval

        except ActionUnboundSession:
            print('Error: Session that Action was assigned to no longer exists.')
        except SessionUnboundTarget:
            print('Error: Target that Session was assigned to no longer exists.')
        except CannotCancelAction:
            print('Error: Cannot cancel action.\
            The action may have already been sent to an agent.')
        except CannotAssignAction:
            print('Error: Cannot assign action to session.\
            The action may be bound to another session_id.')
        except CannotBindAction:
            print('Error: The Action cannot be assigned to this\
            Target because it does not exist.')
        except ActionSyntaxError:
            print('Error: Invalid Action syntax.')
        except MembershipError as exception:
            print('Error: Invalid Membership Modification.')
            print(exception)

        except ValidationError:
            print('Error: Invalid argument type.')
        except ResourceNotFound:
            print('Error: One or more requested resources were not found.')
        except ResourceAlreadyExists:
            print('Error: This resource already exists.')
        except MissingParameter:
            print('Error: Missing required parameter.')


        except InvaidUser:
            print('Error: Invalid user.')
        except InvalidCredentials:
            print('Error: Invalid Credentials.')
        except PermissionDenied:
            print('Error: Permission denied.')
        except InvalidAPIKey:
            print('Error: Invalid API Key.')

        except ServerConnectionError:
            print("Error: Could not connect to teamserver.")
        except ServerInternalError:
            print("Error: Teamserver encountered unexpected error")

        except APIException as exception:
            print('Error: Teamserver encountered unhandled exception')
            print(exception)

        except Exception as exception: # pylint: disable=broad-except
            print('Error: Client encountered unhandled exception')
            print(type(exception))
            print(exception)
            raise exception

    return wrapper
