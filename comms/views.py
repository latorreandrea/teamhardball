from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView

from .forms import EventDetailsForm, EventPostForm, NewsForm
from .models import Attendance, Event, Post


class PostListView(ListView):
    model = Post
    template_name = 'comms/post_list.html'
    context_object_name = 'posts'
    paginate_by = 12

    def get_queryset(self):
        return Post.objects.select_related('author').prefetch_related('event_details')


class PostDetailView(DetailView):
    model = Post
    template_name = 'comms/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        event = getattr(post, 'event_details', None)
        context['event'] = event
        if event and self.request.user.is_authenticated:
            attendance = Attendance.objects.filter(
                user=self.request.user, event=event
            ).first()
            context['user_attendance'] = attendance
        return context


@login_required
def rsvp(request, event_pk):
    """Toggle RSVP status for an event (AJAX endpoint)."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    event = get_object_or_404(Event, pk=event_pk)
    status = request.POST.get('status')
    if status not in ('confirmed', 'declined', 'standby'):
        return JsonResponse({'error': 'Invalid status'}, status=400)

    attendance, _ = Attendance.objects.update_or_create(
        user=request.user,
        event=event,
        defaults={'status': status},
    )
    return JsonResponse({'status': attendance.status})


# ─────────────────────────────────────────────────────────────────────────────
# ADMIN VIEWS — only staff members can access these
# ─────────────────────────────────────────────────────────────────────────────

@staff_member_required
def admin_news_list(request):
    """List all plain news posts (no linked event)."""
    news = Post.objects.filter(event_details__isnull=True).select_related('author')
    return render(request, 'comms/admin/news_list.html', {'news': news})


@staff_member_required
def admin_news_create(request):
    """Create a new news post."""
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, f'Nyhed "{post.title}" er oprettet.')
            return redirect('comms:admin_news_list')
    else:
        form = NewsForm()
    return render(request, 'comms/admin/news_form.html', {'form': form, 'action': 'Opret'})


@staff_member_required
def admin_news_edit(request, slug):
    """Edit an existing news post."""
    post = get_object_or_404(Post, slug=slug, event_details__isnull=True)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, f'Nyhed "{post.title}" er opdateret.')
            return redirect('comms:admin_news_list')
    else:
        form = NewsForm(instance=post)
    return render(request, 'comms/admin/news_form.html', {'form': form, 'action': 'Rediger', 'post': post})


@staff_member_required
def admin_news_delete(request, slug):
    """Delete a news post (confirmation page)."""
    post = get_object_or_404(Post, slug=slug, event_details__isnull=True)
    if request.method == 'POST':
        title = post.title
        post.delete()
        messages.success(request, f'Nyhed "{title}" er slettet.')
        return redirect('comms:admin_news_list')
    return render(request, 'comms/admin/confirm_delete.html', {'object': post, 'type': 'nyhed'})


@staff_member_required
def admin_events_list(request):
    """List all events."""
    events = Event.objects.select_related('related_post', 'related_post__author').order_by('-event_date')
    return render(request, 'comms/admin/events_list.html', {'events': events})


@staff_member_required
def admin_event_create(request):
    """Create a new event (Post + Event details in one form)."""
    if request.method == 'POST':
        post_form = EventPostForm(request.POST, request.FILES)
        event_form = EventDetailsForm(request.POST)
        if post_form.is_valid() and event_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            event = event_form.save(commit=False)
            event.related_post = post
            event.save()
            messages.success(request, f'Event "{post.title}" er oprettet.')
            return redirect('comms:admin_events_list')
    else:
        post_form = EventPostForm()
        event_form = EventDetailsForm()
    return render(request, 'comms/admin/event_form.html', {
        'post_form': post_form,
        'event_form': event_form,
        'action': 'Opret',
    })


@staff_member_required
def admin_event_edit(request, event_pk):
    """Edit an existing event."""
    event = get_object_or_404(Event, pk=event_pk)
    post = event.related_post
    if request.method == 'POST':
        post_form = EventPostForm(request.POST, request.FILES, instance=post)
        event_form = EventDetailsForm(request.POST, instance=event)
        if post_form.is_valid() and event_form.is_valid():
            post_form.save()
            event_form.save()
            messages.success(request, f'Event "{post.title}" er opdateret.')
            return redirect('comms:admin_events_list')
    else:
        post_form = EventPostForm(instance=post)
        event_form = EventDetailsForm(instance=event)
    return render(request, 'comms/admin/event_form.html', {
        'post_form': post_form,
        'event_form': event_form,
        'action': 'Rediger',
        'event': event,
    })


@staff_member_required
def admin_event_delete(request, event_pk):
    """Delete an event (and its related post)."""
    event = get_object_or_404(Event, pk=event_pk)
    post = event.related_post
    if request.method == 'POST':
        title = post.title
        post.delete()  # cascades to Event via OneToOneField
        messages.success(request, f'Event "{title}" er slettet.')
        return redirect('comms:admin_events_list')
    return render(request, 'comms/admin/confirm_delete.html', {'object': post, 'type': 'event'})


@staff_member_required
def admin_event_attendees(request, event_pk):
    """Show attendees list for a specific event."""
    event = get_object_or_404(Event, pk=event_pk)
    attendances = (
        Attendance.objects
        .filter(event=event)
        .select_related('user')
        .order_by('status', 'user__last_name')
    )
    confirmed = [a for a in attendances if a.status == 'confirmed']
    standby   = [a for a in attendances if a.status == 'standby']
    declined  = [a for a in attendances if a.status == 'declined']
    return render(request, 'comms/admin/event_attendees.html', {
        'event': event,
        'confirmed': confirmed,
        'standby': standby,
        'declined': declined,
    })



class PostListView(ListView):
    model = Post
    template_name = 'comms/post_list.html'
    context_object_name = 'posts'
    paginate_by = 12

    def get_queryset(self):
        return Post.objects.select_related('author').prefetch_related('event_details')


class PostDetailView(DetailView):
    model = Post
    template_name = 'comms/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        # Add event details if this post is an event
        event = getattr(post, 'event_details', None)
        context['event'] = event
        if event and self.request.user.is_authenticated:
            attendance = Attendance.objects.filter(
                user=self.request.user, event=event
            ).first()
            context['user_attendance'] = attendance
        return context


@login_required
def rsvp(request, event_pk):
    """Toggle RSVP status for an event (AJAX endpoint)."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    event = get_object_or_404(Event, pk=event_pk)
    status = request.POST.get('status')
    if status not in ('confirmed', 'declined', 'standby'):
        return JsonResponse({'error': 'Invalid status'}, status=400)

    attendance, _ = Attendance.objects.update_or_create(
        user=request.user,
        event=event,
        defaults={'status': status},
    )
    return JsonResponse({'status': attendance.status})
