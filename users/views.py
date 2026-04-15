from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .forms import JoinRequestForm, ProfileForm
from .models import JoinRequest, User


def join_request(request):
    """
    View for non-registered users to submit a membership request.
    Displays a form to collect name, surname, email, and phone number.
    """
    if request.user.is_authenticated:
        messages.info(request, 'Hør her, soldat! Er du blind eller bare dum?! Du er ALLEREDE indskrevet i enheden! Vend om og MARCH!')
        return redirect('home:index')
    if request.method == 'POST':
        form = JoinRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 
                'Din anmodning er blevet modtaget! Vi vil kontakte dig hurtigst muligt. / '
                'Your request has been received! We will contact you as soon as possible.'
            )
            return redirect('home:index')
    else:
        form = JoinRequestForm()
    
    return render(request, 'users/join_request.html', {'form': form})


@login_required
@login_required
def enheden(request):
    """
    Members-only page showing the unit structure as a tactical pyramid.
    Tiers: GEN → Officers (CPT–2LT) → NCOs (SGT1C–SGT) → Enlisted (CPL–PVT)
    """
    rank_order = User.RANK_ORDER
    all_members = list(User.objects.filter(is_active=True))
    all_members.sort(key=lambda u: (
        rank_order.index(u.rank) if u.rank in rank_order else 99,
        u.last_name
    ))

    gen_members = [u for u in all_members if u.rank == 'gen']
    officers    = [u for u in all_members if u.rank in ('cpt', '1lt', '2lt')]
    ncos        = [u for u in all_members if u.rank in ('sgt1c', 'ssgt', 'sgt')]
    enlisted    = [u for u in all_members if u.rank in ('cpl', 'spc', 'pvt1', 'pvt2', 'pvt')]

    return render(request, 'users/enheden.html', {
        'gen_members': gen_members,
        'officers':    officers,
        'ncos':        ncos,
        'enlisted':    enlisted,
    })


@login_required
def operator_detail(request, user_id):
    """Detail page for a single operator — shows full card with 3D tilt."""
    import random
    from .forms import ALPHA3_TO_ALPHA2

    _BIO_PLACEHOLDERS = [
        'Vi er stadig ved at afhøre vedkommende for at finde ud af, hvem han er og hvem der sender ham — men han er et hårdt nød at knække.',
        'Operatørens baggrund er [FORTROLIGT]. Vi mistænker, at han selv ikke husker det.',
        'Intet at rapportere. Enheden venter stadig på en forklaring fra operatøren selv. Det kan vente længe.',
        'Klassificeret. Eller også er operatøren bare for doven til at skrive noget. Efterretningerne peger på det sidstnævnte.',
        'Denne operatørs identitet er endnu ikke bekræftet. Han var dog tydeligvis for optaget af at skyde folk til at skrive noget her.',
    ]

    member = get_object_or_404(User, id=user_id, is_active=True)
    nat_flag_code = ALPHA3_TO_ALPHA2.get(member.nationality, '')
    bio_placeholder = random.choice(_BIO_PLACEHOLDERS) if not member.bio else ''
    return render(request, 'users/operator_detail.html', {
        'member': member,
        'nat_flag_code': nat_flag_code,
        'bio_placeholder': bio_placeholder,
    })


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


@login_required
def edit_profile(request):
    """
    Allow authenticated members to edit their profile card:
    profile image (converted to WebP), nationality, and bio.
    Name, surname and rank are read-only.
    """
    from .forms import NATIONALITY_CHOICES, ALPHA3_TO_ALPHA2
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Din profil er blevet opdateret.')
                return redirect('users:edit_profile')
            except Exception:
                messages.warning(
                    request,
                    'Der opstod et problem under behandlingen af dine oplysninger. '
                    'Prøv igen, og kontakt en administrator, hvis problemet fortsætter.'
                )
    else:
        form = ProfileForm(instance=request.user)

    # Build a dict for quick flag/label lookup in the template
    nat_map = {code: label for code, label in NATIONALITY_CHOICES if code}
    nat_label = nat_map.get(request.user.nationality, request.user.nationality or '')
    nat_short = nat_label.split(' – ')[0] if ' – ' in nat_label else nat_label
    nat_flag_code = ALPHA3_TO_ALPHA2.get(request.user.nationality, '')

    return render(request, 'users/edit_profile.html', {
        'form': form,
        'nat_label': nat_label,
        'nat_short': nat_short,
        'nat_flag_code': nat_flag_code,
    })


@staff_member_required
def admin_dashboard(request):
    """
    Custom admin dashboard with all site management functionalities.
    Displays pending join requests count and provides access to various admin sections.
    """
    pending_requests_count = JoinRequest.objects.filter(status='pending').count()
    
    context = {
        'pending_requests_count': pending_requests_count,
    }
    
    return render(request, 'users/admin_dashboard.html', context)


@staff_member_required
def admin_kommandostruktur(request):
    """
    Admin view for managing the command structure.
    Shows all active users in a sortable table with rank assignment.
    """
    sort_by = request.GET.get('sort', 'rank')
    order = request.GET.get('order', 'asc')

    allowed_sorts = {'rank': 'rank', 'last_name': 'last_name', 'nationality': 'nationality', 'residence': 'residence'}
    sort_field = allowed_sorts.get(sort_by, 'rank')
    qs = User.objects.filter(is_active=True)
    if order == 'desc':
        qs = qs.order_by(f'-{sort_field}')
    else:
        qs = qs.order_by(sort_field)

    context = {
        'users': qs,
        'rank_choices': User.RANK_CHOICES,
        'sort_by': sort_by,
        'order': order,
    }
    return render(request, 'users/admin_kommandostruktur.html', context)


@staff_member_required
def update_rank(request, user_id):
    """AJAX endpoint to update a user's rank."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    member = get_object_or_404(User, id=user_id)
    new_rank = request.POST.get('rank')

    # GEN is reserved for superusers only — cannot be assigned or removed via this endpoint
    if member.is_superuser:
        return JsonResponse({'error': 'Er det her et mytteri?! Den generals rang kan ikke ændres, soldat! Træd tilbage FØR JEG FÅR DIG DEGRADERET!'}, status=403)
    if new_rank == 'gen':
        return JsonResponse({'error': 'Hør her din elendige rekrut! GEN-rangen er forbeholdt Generalen! Du er ikke engang værdig til at udtale det ord!'}, status=403)

    valid_ranks = [r[0] for r in User.RANK_CHOICES if r[0] != 'gen']
    if new_rank not in valid_ranks:
        return JsonResponse({'error': 'Ugyldigt rang'}, status=400)
    
    old_rank_display = member.get_rank_display()
    member.rank = new_rank
    member.save(update_fields=['rank'])
    
    messages.success(
        request,
        f'{member.get_full_name()} er nu tildelt rangen {member.get_rank_display()} (tidligere {old_rank_display}).'
    )
    return JsonResponse({'ok': True, 'new_rank_display': member.get_rank_display()})


@staff_member_required
def new_recruits(request):
    """
    View for admins to manage membership join requests.
    Shows all pending, approved, and rejected requests with filtering options.
    """
    status_filter = request.GET.get('status', 'pending')
    
    if status_filter == 'all':
        join_requests = JoinRequest.objects.all()
    else:
        join_requests = JoinRequest.objects.filter(status=status_filter)
    
    pending_count = JoinRequest.objects.filter(status='pending').count()
    
    context = {
        'requests': join_requests,  # Changed key to match template variable
        'status_filter': status_filter,
        'pending_count': pending_count,
    }
    
    return render(request, 'users/new_recruits.html', context)


@staff_member_required
def approve_request(request, request_id):
    """
    Approve a join request and create a new user account.
    Generates a temporary password and sends welcome email.
    """
    join_req = get_object_or_404(JoinRequest, id=request_id)
    
    if join_req.status != 'pending':
        messages.warning(request, 'Denne anmodning er allerede behandlet.')
        return redirect('users:new_recruits')

    if User.objects.filter(email=join_req.email).exists():
        messages.error(
            request,
            f'Der findes allerede en bruger med emailen {join_req.email}. Ryd testdata eller brug en anden email.'
        )
        return redirect('users:new_recruits')
    
    # Generate password
    password = join_req.generate_password()
    
    # Create new user
    user = User.objects.create_user(
        email=join_req.email,
        password=password,
        first_name=join_req.first_name,
        last_name=join_req.last_name,
        rank='pvt'
    )
    
    # Update join request status
    join_req.status = 'approved'
    join_req.processed_at = timezone.now()
    join_req.processed_by = request.user
    join_req.save()
    
    # Send approval email
    email_sent = send_approval_email(join_req, password)
    if not email_sent:
        messages.warning(
            request,
            'Anmodning godkendt, men der opstod et problem med at sende velkomst-emailen. / '
            'Request approved, but there was a problem sending the welcome email.'
        )
    else:
        messages.success(
            request,
            f'Anmodning godkendt! {join_req.first_name} {join_req.last_name} er nu medlem.'
        )
    
    return redirect('users:new_recruits')


@staff_member_required
def reject_request(request, request_id):
    """
    Reject a join request with a reason.
    Sends rejection email to the applicant.
    """
    join_req = get_object_or_404(JoinRequest, id=request_id)
    
    if join_req.status != 'pending':
        messages.warning(request, 'Denne anmodning er allerede behandlet.')
        return redirect('users:new_recruits')
    
    if request.method == 'POST':
        rejection_reason = request.POST.get('reason', '')
        
        if not rejection_reason:
            messages.error(request, 'Du skal angive en årsag til afvisning.')
            return redirect('users:new_recruits')
        
        # Update join request status
        join_req.status = 'rejected'
        join_req.rejection_reason = rejection_reason
        join_req.processed_at = timezone.now()
        join_req.processed_by = request.user
        join_req.save()
        
        # Send rejection email
        email_sent = send_rejection_email(join_req)
        if not email_sent:
            messages.warning(
                request,
                'Anmodning afvist, men der opstod et problem med at sende afvisnings-emailen. / '
                'Request rejected, but there was a problem sending the rejection email.'
            )
        else:
            messages.info(
                request,
                f'Anmodning afvist. {join_req.first_name} {join_req.last_name} er blevet informeret.'
            )
        
        return redirect('users:new_recruits')
    
    return redirect('users:new_recruits')


def send_approval_email(join_request, password):
    """Send approval email to new member. Returns True on success, False on failure."""
    subject = 'Velkommen til N.S.O.G.! / Welcome to N.S.O.G.!'
    discord = getattr(settings, 'DISCORD_LINK', '[Discord link]')
    
    message = f"""
Kære {join_request.first_name} {join_request.last_name},

Din anmodning om medlemskab er blevet godkendt!

Log ind på dit private område: {settings.SITE_URL}/accounts/login/

Dine login-oplysninger:
Email: {join_request.email}
Password: {password}

VIGTIGT: Efter dit første login skal du ændre din adgangskode.

Velkommen ombord!
Her er vores Discord-kanal: {discord}

---

Dear {join_request.first_name} {join_request.last_name},

Your membership request has been approved!

Access your private area: {settings.SITE_URL}/accounts/login/

Your login credentials:
Email: {join_request.email}
Password: {password}

IMPORTANT: After your first login, you must change your password.

Welcome aboard!
Here is our Discord channel: {discord}

---
N.S.O.G. - Crudeles in Proelio
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [join_request.email],
            fail_silently=False,
        )
        return True
    except Exception:
        return False


def send_rejection_email(join_request):
    """Send rejection email to applicant. Returns True on success, False on failure."""
    subject = 'Din anmodning til N.S.O.G. / Your N.S.O.G. application'
    
    message = f"""
Kære {join_request.first_name} {join_request.last_name},

Desværre kan vi ikke godkende din anmodning om medlemskab på nuværende tidspunkt.

Årsag: {join_request.rejection_reason}

Du er velkommen til at ansøge igen i fremtiden.

---

Dear {join_request.first_name} {join_request.last_name},

Unfortunately, we cannot approve your membership request at this time.

Reason: {join_request.rejection_reason}

You are welcome to apply again in the future.

---
N.S.O.G. - Crudeles in Proelio
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [join_request.email],
            fail_silently=False,
        )
        return True
    except Exception:
        return False
