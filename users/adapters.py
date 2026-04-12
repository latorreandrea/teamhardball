from allauth.account.adapter import DefaultAccountAdapter
from django.contrib import messages


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom account adapter to completely suppress allauth default messages.
    We handle all login/logout messages with custom signals in users/signals.py
    """
    
    def add_message(self, request, level, message_template, message_context=None, extra_tags=''):
        """
        Override to completely suppress allauth messages during authentication.
        Our custom signal handlers provide all user feedback with ironic Danish messages.
        """
        # Block all SUCCESS and ERROR messages from allauth during authentication
        # Our signals handle login success/failure with custom messages
        if level in (messages.SUCCESS, messages.ERROR):
            return
        
        # Allow INFO and WARNING messages (if needed for other purposes)
        super().add_message(request, level, message_template, message_context, extra_tags)
