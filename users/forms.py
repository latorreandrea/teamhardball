from django import forms
from django.core.exceptions import ValidationError
from .models import JoinRequest, User

import io
from PIL import Image


# Mapping ISO 3166-1 alpha-3 → alpha-2 (lowercase) for flagcdn.com
ALPHA3_TO_ALPHA2 = {
    'AFG':'af','ALB':'al','DZA':'dz','AND':'ad','AGO':'ao','ARG':'ar','ARM':'am',
    'AUS':'au','AUT':'at','AZE':'az','BHS':'bs','BHR':'bh','BGD':'bd','BLR':'by',
    'BEL':'be','BLZ':'bz','BEN':'bj','BTN':'bt','BOL':'bo','BIH':'ba','BWA':'bw',
    'BRA':'br','BRN':'bn','BGR':'bg','BFA':'bf','BDI':'bi','CPV':'cv','KHM':'kh',
    'CMR':'cm','CAN':'ca','CAF':'cf','TCD':'td','CHL':'cl','CHN':'cn','COL':'co',
    'COD':'cd','COG':'cg','CRI':'cr','CIV':'ci','HRV':'hr','CUB':'cu','CYP':'cy',
    'CZE':'cz','DNK':'dk','DJI':'dj','DOM':'do','ECU':'ec','EGY':'eg','SLV':'sv',
    'GNQ':'gq','ERI':'er','EST':'ee','SWZ':'sz','ETH':'et','FJI':'fj','FIN':'fi',
    'FRA':'fr','GAB':'ga','GMB':'gm','GEO':'ge','DEU':'de','GHA':'gh','GRC':'gr',
    'GTM':'gt','GIN':'gn','GNB':'gw','GUY':'gy','HTI':'ht','HND':'hn','HUN':'hu',
    'ISL':'is','IND':'in','IDN':'id','IRN':'ir','IRQ':'iq','IRL':'ie','ISR':'il',
    'ITA':'it','JAM':'jm','JPN':'jp','JOR':'jo','KAZ':'kz','KEN':'ke','PRK':'kp',
    'KOR':'kr','KWT':'kw','KGZ':'kg','LAO':'la','LVA':'lv','LBN':'lb','LSO':'ls',
    'LBR':'lr','LBY':'ly','LIE':'li','LTU':'lt','LUX':'lu','MDG':'mg','MWI':'mw',
    'MYS':'my','MDV':'mv','MLI':'ml','MLT':'mt','MRT':'mr','MUS':'mu','MEX':'mx',
    'MDA':'md','MCO':'mc','MNG':'mn','MNE':'me','MAR':'ma','MOZ':'mz','MMR':'mm',
    'NAM':'na','NPL':'np','NLD':'nl','NZL':'nz','NIC':'ni','NER':'ne','NGA':'ng',
    'MKD':'mk','NOR':'no','OMN':'om','PAK':'pk','PAN':'pa','PNG':'pg','PRY':'py',
    'PER':'pe','PHL':'ph','POL':'pl','PRT':'pt','QAT':'qa','ROU':'ro','RUS':'ru',
    'RWA':'rw','SAU':'sa','SEN':'sn','SRB':'rs','SLE':'sl','SGP':'sg','SVK':'sk',
    'SVN':'si','SOM':'so','ZAF':'za','SSD':'ss','ESP':'es','LKA':'lk','SDN':'sd',
    'SUR':'sr','SWE':'se','CHE':'ch','SYR':'sy','TWN':'tw','TJK':'tj','TZA':'tz',
    'THA':'th','TLS':'tl','TGO':'tg','TTO':'tt','TUN':'tn','TUR':'tr','TKM':'tm',
    'UGA':'ug','UKR':'ua','ARE':'ae','GBR':'gb','USA':'us','URY':'uy','UZB':'uz',
    'VEN':'ve','VNM':'vn','YEM':'ye','ZMB':'zm','ZWE':'zw',
}


# ISO 3166-1 alpha-3 country list (no emoji — flag shown via flagcdn.com)
NATIONALITY_CHOICES = [
    ('', '— Vælg nationalitet —'),
    ('AFG', 'AFG – Afghanistan'),
    ('ALB', 'ALB – Albanien'),
    ('DZA', 'DZA – Algeriet'),
    ('AND', 'AND – Andorra'),
    ('AGO', 'AGO – Angola'),
    ('ARG', 'ARG – Argentina'),
    ('ARM', 'ARM – Armenien'),
    ('AUS', 'AUS – Australien'),
    ('AUT', 'AUT – Østrig'),
    ('AZE', 'AZE – Aserbajdsjan'),
    ('BHS', 'BHS – Bahamas'),
    ('BHR', 'BHR – Bahrain'),
    ('BGD', 'BGD – Bangladesh'),
    ('BLR', 'BLR – Hviderusland'),
    ('BEL', 'BEL – Belgien'),
    ('BLZ', 'BLZ – Belize'),
    ('BEN', 'BEN – Benin'),
    ('BTN', 'BTN – Bhutan'),
    ('BOL', 'BOL – Bolivia'),
    ('BIH', 'BIH – Bosnien-Hercegovina'),
    ('BWA', 'BWA – Botswana'),
    ('BRA', 'BRA – Brasilien'),
    ('BRN', 'BRN – Brunei'),
    ('BGR', 'BGR – Bulgarien'),
    ('BFA', 'BFA – Burkina Faso'),
    ('BDI', 'BDI – Burundi'),
    ('CPV', 'CPV – Kap Verde'),
    ('KHM', 'KHM – Cambodja'),
    ('CMR', 'CMR – Cameroun'),
    ('CAN', 'CAN – Canada'),
    ('CAF', 'CAF – Centralafrikanske Republik'),
    ('TCD', 'TCD – Tchad'),
    ('CHL', 'CHL – Chile'),
    ('CHN', 'CHN – Kina'),
    ('COL', 'COL – Colombia'),
    ('COD', 'COD – DR Congo'),
    ('COG', 'COG – Congo'),
    ('CRI', 'CRI – Costa Rica'),
    ('CIV', 'CIV – Elfenbenskysten'),
    ('HRV', 'HRV – Kroatien'),
    ('CUB', 'CUB – Cuba'),
    ('CYP', 'CYP – Cypern'),
    ('CZE', 'CZE – Tjekkiet'),
    ('DNK', 'DNK – Danmark'),
    ('DJI', 'DJI – Djibouti'),
    ('DOM', 'DOM – Dominikanske Republik'),
    ('ECU', 'ECU – Ecuador'),
    ('EGY', 'EGY – Egypten'),
    ('SLV', 'SLV – El Salvador'),
    ('GNQ', 'GNQ – Ækvatorialguinea'),
    ('ERI', 'ERI – Eritrea'),
    ('EST', 'EST – Estland'),
    ('SWZ', 'SWZ – Eswatini'),
    ('ETH', 'ETH – Etiopien'),
    ('FJI', 'FJI – Fiji'),
    ('FIN', 'FIN – Finland'),
    ('FRA', 'FRA – Frankrig'),
    ('GAB', 'GAB – Gabon'),
    ('GMB', 'GMB – Gambia'),
    ('GEO', 'GEO – Georgien'),
    ('DEU', 'DEU – Tyskland'),
    ('GHA', 'GHA – Ghana'),
    ('GRC', 'GRC – Grækenland'),
    ('GTM', 'GTM – Guatemala'),
    ('GIN', 'GIN – Guinea'),
    ('GNB', 'GNB – Guinea-Bissau'),
    ('GUY', 'GUY – Guyana'),
    ('HTI', 'HTI – Haiti'),
    ('HND', 'HND – Honduras'),
    ('HUN', 'HUN – Ungarn'),
    ('ISL', 'ISL – Island'),
    ('IND', 'IND – Indien'),
    ('IDN', 'IDN – Indonesien'),
    ('IRN', 'IRN – Iran'),
    ('IRQ', 'IRQ – Irak'),
    ('IRL', 'IRL – Irland'),
    ('ISR', 'ISR – Israel'),
    ('ITA', 'ITA – Italien'),
    ('JAM', 'JAM – Jamaica'),
    ('JPN', 'JPN – Japan'),
    ('JOR', 'JOR – Jordan'),
    ('KAZ', 'KAZ – Kasakhstan'),
    ('KEN', 'KEN – Kenya'),
    ('PRK', 'PRK – Nordkorea'),
    ('KOR', 'KOR – Sydkorea'),
    ('KWT', 'KWT – Kuwait'),
    ('KGZ', 'KGZ – Kirgisistan'),
    ('LAO', 'LAO – Laos'),
    ('LVA', 'LVA – Letland'),
    ('LBN', 'LBN – Libanon'),
    ('LSO', 'LSO – Lesotho'),
    ('LBR', 'LBR – Liberia'),
    ('LBY', 'LBY – Libyen'),
    ('LIE', 'LIE – Liechtenstein'),
    ('LTU', 'LTU – Litauen'),
    ('LUX', 'LUX – Luxembourg'),
    ('MDG', 'MDG – Madagaskar'),
    ('MWI', 'MWI – Malawi'),
    ('MYS', 'MYS – Malaysia'),
    ('MDV', 'MDV – Maldiverne'),
    ('MLI', 'MLI – Mali'),
    ('MLT', 'MLT – Malta'),
    ('MRT', 'MRT – Mauretanien'),
    ('MUS', 'MUS – Mauritius'),
    ('MEX', 'MEX – Mexico'),
    ('MDA', 'MDA – Moldova'),
    ('MCO', 'MCO – Monaco'),
    ('MNG', 'MNG – Mongoliet'),
    ('MNE', 'MNE – Montenegro'),
    ('MAR', 'MAR – Marokko'),
    ('MOZ', 'MOZ – Mozambique'),
    ('MMR', 'MMR – Myanmar'),
    ('NAM', 'NAM – Namibia'),
    ('NPL', 'NPL – Nepal'),
    ('NLD', 'NLD – Holland'),
    ('NZL', 'NZL – New Zealand'),
    ('NIC', 'NIC – Nicaragua'),
    ('NER', 'NER – Niger'),
    ('NGA', 'NGA – Nigeria'),
    ('MKD', 'MKD – Nordmakedonien'),
    ('NOR', 'NOR – Norge'),
    ('OMN', 'OMN – Oman'),
    ('PAK', 'PAK – Pakistan'),
    ('PAN', 'PAN – Panama'),
    ('PNG', 'PNG – Papua Ny Guinea'),
    ('PRY', 'PRY – Paraguay'),
    ('PER', 'PER – Peru'),
    ('PHL', 'PHL – Filippinerne'),
    ('POL', 'POL – Polen'),
    ('PRT', 'PRT – Portugal'),
    ('QAT', 'QAT – Qatar'),
    ('ROU', 'ROU – Rumænien'),
    ('RUS', 'RUS – Rusland'),
    ('RWA', 'RWA – Rwanda'),
    ('SAU', 'SAU – Saudi-Arabien'),
    ('SEN', 'SEN – Senegal'),
    ('SRB', 'SRB – Serbien'),
    ('SLE', 'SLE – Sierra Leone'),
    ('SGP', 'SGP – Singapore'),
    ('SVK', 'SVK – Slovakiet'),
    ('SVN', 'SVN – Slovenien'),
    ('SOM', 'SOM – Somalia'),
    ('ZAF', 'ZAF – Sydafrika'),
    ('SSD', 'SSD – Sydsudan'),
    ('ESP', 'ESP – Spanien'),
    ('LKA', 'LKA – Sri Lanka'),
    ('SDN', 'SDN – Sudan'),
    ('SUR', 'SUR – Surinam'),
    ('SWE', 'SWE – Sverige'),
    ('CHE', 'CHE – Schweiz'),
    ('SYR', 'SYR – Syrien'),
    ('TWN', 'TWN – Taiwan'),
    ('TJK', 'TJK – Tadsjikistan'),
    ('TZA', 'TZA – Tanzania'),
    ('THA', 'THA – Thailand'),
    ('TLS', 'TLS – Østtimor'),
    ('TGO', 'TGO – Togo'),
    ('TTO', 'TTO – Trinidad og Tobago'),
    ('TUN', 'TUN – Tunesien'),
    ('TUR', 'TUR – Tyrkiet'),
    ('TKM', 'TKM – Turkmenistan'),
    ('UGA', 'UGA – Uganda'),
    ('UKR', 'UKR – Ukraine'),
    ('ARE', 'ARE – Forenede Arabiske Emirater'),
    ('GBR', 'GBR – Storbritannien'),
    ('USA', 'USA – USA'),
    ('URY', 'URY – Uruguay'),
    ('UZB', 'UZB – Usbekistan'),
    ('VEN', 'VEN – Venezuela'),
    ('VNM', 'VNM – Vietnam'),
    ('YEM', 'YEM – Yemen'),
    ('ZMB', 'ZMB – Zambia'),
    ('ZWE', 'ZWE – Zimbabwe'),
]

# Allowed image formats
ALLOWED_IMAGE_FORMATS = {'JPEG', 'WEBP'}
MAX_IMAGE_SIZE_BYTES = 2 * 1024 * 1024  # 2 MB


class ProfileForm(forms.ModelForm):
    """Form for members to edit their own profile card."""

    nationality = forms.ChoiceField(
        choices=NATIONALITY_CHOICES,
        required=False,
        label='Nationalitet',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = User
        fields = ['profile_image', 'nationality', 'residence', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Fortæl om dig selv... (maks. 500 tegn)',
                'maxlength': 500,
            }),
            'profile_image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/webp',
            }),
            'residence': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'F.eks. København, Milano, Oslo…',
            }),
        }
        labels = {
            'profile_image': 'Profilbillede',
            'bio': 'Om mig',
            'residence': 'Bopælsby',
        }
        help_texts = {
            'residence': 'Angiv den by eller det område, hvor du er bosiddende.',
        }

    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image')
        if not image or not hasattr(image, 'name'):
            # No new file uploaded — keep existing
            return image

        # Size check
        if image.size > MAX_IMAGE_SIZE_BYTES:
            raise ValidationError('Billedet må højst være 2 MB.')

        # Format check — open with Pillow to detect actual format
        try:
            img = Image.open(image)
            img.verify()
        except Exception:
            raise ValidationError('Ugyldigt billedformat. Brug JPG eller WebP.')

        image.seek(0)
        img = Image.open(image)
        if img.format not in ALLOWED_IMAGE_FORMATS:
            raise ValidationError('Kun JPG og WebP er tilladt.')

        # Aspect ratio check — target 600×840 (5:7). Allow ±15 % tolerance.
        w, h = img.size
        if w == 0 or h == 0:
            raise ValidationError('Ugyldigt billede.')
        ratio = w / h
        target_ratio = 600 / 840  # ≈ 0.714
        if abs(ratio - target_ratio) > target_ratio * 0.15:
            raise ValidationError(
                f'Billedforhold skal være ca. 600×840 px (portræt). '
                f'Det uploadede billede er {w}×{h} px.'
            )

        image.seek(0)
        return image

    def save(self, commit=True):
        user = super().save(commit=False)
        new_image = self.cleaned_data.get('profile_image')

        if new_image and hasattr(new_image, 'read'):
            # Delete old image from storage
            if user.profile_image:
                try:
                    user.profile_image.delete(save=False)
                except Exception:
                    pass

            # Convert to WebP and resize to fit within 600×840
            img = Image.open(new_image)
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGB')
            img.thumbnail((600, 840), Image.LANCZOS)

            buffer = io.BytesIO()
            save_kwargs = {'format': 'WEBP', 'quality': 82, 'method': 6}
            if img.mode == 'RGBA':
                save_kwargs['lossless'] = False
            img.save(buffer, **save_kwargs)
            buffer.seek(0)

            from django.core.files.base import ContentFile
            filename = f"profiles/profile_{user.pk}.webp"
            user.profile_image.save(filename, ContentFile(buffer.read()), save=False)

        if commit:
            user.save(update_fields=['profile_image', 'nationality', 'bio', 'residence'])
        return user


class JoinRequestForm(forms.ModelForm):
    """Form for users to request membership"""

    class Meta:
        model = JoinRequest
        fields = ['first_name', 'last_name', 'email', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Indtast dit fornavn'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Indtast dit efternavn'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'din.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+45 12 34 56 78'
            }),
        }
        labels = {
            'first_name': 'Fornavn',
            'last_name': 'Efternavn',
            'email': 'Email',
            'phone': 'Telefonnummer',
        }
