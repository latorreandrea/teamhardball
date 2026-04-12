from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_joinrequest'),
    ]

    operations = [
        # User model renames
        migrations.RenameField(
            model_name='user',
            old_name='nome',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='cognome',
            new_name='last_name',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='rango',
            new_name='rank',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='nazionalita',
            new_name='nationality',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='luogo_residenza',
            new_name='residence',
        ),
        # JoinRequest model renames
        migrations.RenameField(
            model_name='joinrequest',
            old_name='nome',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='joinrequest',
            old_name='cognome',
            new_name='last_name',
        ),
        migrations.RenameField(
            model_name='joinrequest',
            old_name='telefono',
            new_name='phone',
        ),
    ]
