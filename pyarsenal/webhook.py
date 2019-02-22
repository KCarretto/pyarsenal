"""
This module contains Webhook API functions.
"""
from pyarsenal.objects import Webhook


def register_webhook(self, post_url, event_triggers):
    """
    Hook an API call or other event, and receive information from the event.
    Useful for developing integrations.

    Args:
        post_url: The URL that data should be sent via an HTTP POST request.
        event_triggers: A list of events to subscribe to.

    Returns the ID of the webhook
    """
    resp = self.call(
        'RegisterWebhook',
        post_url=post_url,
        event_triggers=event_triggers,
    )
    return resp['hook_id']

def unregister_webhook(self, hook_id):
    """
    Unregister a webhook owned by the current user.
    """
    self.call(
        'UnregisterWebhook',
        hook_id=hook_id
    )
    return True

def list_webhooks(self, user_context=None):
    """
    Return a list of the current users webhooks.
    Administrators may specify an administrative user context.
    """
    resp = self.call(
        'ListWebhooks',
        user_context=user_context
    )
    return [Webhook(hook) for hook in resp['hooks']]
