import random
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.contrib import messages
from django.dispatch import receiver


# Frasi di benvenuto ironiche stile Full Metal Jacket in danese
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

# Frasi di errore ironiche stile Full Metal Jacket in danese
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
    Signal handler per login riuscito con frasi ironiche.
    """
    # Ottiene il grado e cognome dell'utente
    rango = user.get_rango_display()
    cognome = user.cognome
    
    # Selezione casuale di una frase di benvenuto
    phrase = random.choice(WELCOME_PHRASES)
    
    # Formatta la frase con grado e cognome
    message = phrase.format(f"{rango} {cognome}")
    
    # Aggiunge il messaggio di successo
    messages.success(request, message)


@receiver(user_login_failed)
def login_failed(sender, credentials, request, **kwargs):
    """
    Signal handler per login fallito con frasi ironiche.
    """
    # Selezione casuale di una frase di errore
    message = random.choice(ERROR_PHRASES)
    
    # Aggiunge il messaggio di errore
    messages.error(request, message)
