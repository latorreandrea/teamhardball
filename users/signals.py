import random
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.contrib import messages
from django.dispatch import receiver


# Ironic welcome phrases in Full Metal Jacket style (Danish)
WELCOME_PHRASES = [
    "Velkommen tilbage, {}! Jeg håber du har dit gevær klar!",
    "Ser godt ud, {}! Klart til kamp eller bare her for kaffen?",
    "Åh, du er tilbage, {}! Troede du havde deserteret!",
    "Endelig besluttede du dig for at dukke op, {}!",
    "Velkommen til basen, {}! Lad os se hvad du er lavet af!",
    "Se hvem der besluttede at vise sig, {}! Bedre sent end aldrig!",
    "Godmorgen, {}! Håber du er klar til at svede!",
    "Der er du, {}! Jeg begyndte at tro du var blevet civil!",
    "Velkommen, {}! Dine fjender venter ikke på dig!",
    "Åh fantastisk, {} er her! Lad showet begynde!",
]

# Ironic logout phrases in Full Metal Jacket style (Danish)
LOGOUT_PHRASES = [
    "Så du stikker af, {}? Håber du ikke regner med at slippe væk så nemt!",
    "Farvel, {}! Prøv ikke at savne basen for meget!",
    "Du vil altid være velkommen tilbage, {}... hvis du tør!",
    "Desertering allerede, {}? Jeg troede du var hårdere end det!",
    "Vi ses snart, {}! Fjenden sover aldrig!",
    "Tak for besøget, {}! Nu ved jeg hvem jeg IKKE skal stole på i kamp!",
    "Hej hej, {}! Husk at tjekke under din seng i nat!",
    "Åh, skal du hjem til mor, {}? Sikke en overraskelse!",
    "Farvel, {}! Prøv at huske hvordan man logger ind næste gang!",
    "Du er logget ud, {}! Håber civilivet er kedeligt nok til dig!",
]

# Ironic error phrases in Full Metal Jacket style (Danish)
ERROR_PHRASES = [
    "Det var det dummeste forsøg på at logge ind, jeg nogensinde har set! Prøv igen, rekryt!",
    "Din email eller password er forkert! Selv min bedstemor kunne gøre det bedre!",
    "Adgang nægtet! Du kan ikke engang huske dit eget password!",
    "Forkerte legitimationsoplysninger! Vil du have mig til at tegne det for dig?!",
    "Login fejlede! Hvad troede du dette var, en legeplads?!",
    "Det var patetisk! Email eller password er forkert, rekrut!",
    "Jeg har set bedre forsøg fra civile! Prøv igen!",
    "Dit login forsøg var så dårligt, at det gør ondt at se på!",
    "Forkert! Forkert! Forkert! Prøv at tænke næste gang!",
    "Det var det værste login forsøg i militærhistorien! Prøv igen!",
]


@receiver(user_logged_in)
def login_success(sender, request, user, **kwargs):
    """
    Signal handler for successful login with ironic phrases.
    The custom adapter blocks allauth messages, so we only add our custom message.
    """
    # Get user's rank and surname
    rank = user.get_rank_display()
    last_name = user.last_name
    
    # Random selection of a welcome phrase
    phrase = random.choice(WELCOME_PHRASES)
    
    # Format the phrase with rank and surname
    message = phrase.format(f"{rank} {last_name}")
    
    # Add our custom success message
    messages.success(request, message)


@receiver(user_logged_out)
def logout_success(sender, request, user, **kwargs):
    """
    Signal handler for successful logout with ironic phrases.
    The custom adapter blocks allauth messages, so we only add our custom message.
    """
    # User might be None if already logged out
    if user:
        # Get user's rank and surname
        rank = user.get_rank_display()
        last_name = user.last_name
        
        # Random selection of a logout phrase
        phrase = random.choice(LOGOUT_PHRASES)
        
        # Format the phrase with rank and surname
        message = phrase.format(f"{rank} {last_name}")
    else:
        # Fallback if user is already logged out
        message = "Du er nu logget ud! Kom sikkert tilbage!"
    
    # Add our custom success message
    messages.success(request, message)


@receiver(user_login_failed)
def login_failed(sender, credentials, request, **kwargs):
    """
    Signal handler for failed login with ironic phrases.
    """
    # Random selection of an error phrase
    message = random.choice(ERROR_PHRASES)
    
    # Add error message
    messages.error(request, message)
