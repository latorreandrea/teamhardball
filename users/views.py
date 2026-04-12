from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def profile_area(request):
    """
    Display the user's private area with profile information and navigation options.
    This view is primarily used for mobile/tablet devices to provide a dedicated page
    instead of a dropdown menu.
    """
    return render(request, 'users/profile_area.html', {
        'user': request.user
    })
