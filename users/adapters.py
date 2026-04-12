from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom account adapter to prevent default allauth messages.
    We handle login/logout messages with custom signals in users/signals.py
    """
    
    def add_message(self, request, level, message_template, message_context=None, extra_tags=''):
        """
        Override to prevent default allauth messages.
        Our custom signal handlers will add ironic Danish messages instead.
        """
        # Common allauth message patterns to block
        blocked_patterns = [
            'successfully signed in',
            'signed in as',
            'incorrect',
            'password is incorrect',
            'unable to log in',
            'please try again',
        ]
        
        # Check if message should be blocked
        message_lower = message_template.lower()
        for pattern in blocked_patterns:
            if pattern in message_lower:
                return
        
        # Allow all other messages (confirmations, etc.)
        super().add_message(request, level, message_template, message_context, extra_tags)
