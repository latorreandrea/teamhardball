from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userachievement',
            name='source',
        ),
    ]
