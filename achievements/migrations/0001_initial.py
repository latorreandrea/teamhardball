from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AchievementDefinition",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("slug", models.SlugField(blank=True, db_index=True, max_length=120, unique=True)),
                ("title", models.CharField(max_length=120)),
                ("description", models.TextField(blank=True)),
                ("icon", models.ImageField(blank=True, null=True, upload_to="achievement_badges/")),
                ("is_active", models.BooleanField(default=True)),
                (
                    "award_mode",
                    models.CharField(
                        choices=[("automatic", "Automatic"), ("manual", "Manual"), ("hybrid", "Hybrid")],
                        default="manual",
                        max_length=16,
                    ),
                ),
                (
                    "rule_type",
                    models.CharField(
                        choices=[
                            ("none", "No automatic rule"),
                            ("confirmed_attendance_count_gte", "Confirmed attendance count >= N"),
                            ("account_age_days_gte", "Account age days >= N"),
                            ("rank_is", "Rank is one of"),
                            ("join_request_approved", "Join request approved"),
                        ],
                        default="none",
                        max_length=64,
                    ),
                ),
                ("rule_config", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "achievement definition",
                "verbose_name_plural": "achievement definitions",
                "ordering": ["title"],
            },
        ),
        migrations.CreateModel(
            name="UserAchievement",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("awarded_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("reason", models.TextField(blank=True)),
                ("source", models.CharField(choices=[("auto", "Automatic"), ("manual", "Manual")], default="manual", max_length=10)),
                (
                    "achievement",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="awards", to="achievements.achievementdefinition"),
                ),
                (
                    "awarded_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="awarded_achievements",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="achievements", to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={
                "verbose_name": "user achievement",
                "verbose_name_plural": "user achievements",
                "ordering": ["-awarded_at"],
            },
        ),
        migrations.AddConstraint(
            model_name="userachievement",
            constraint=models.UniqueConstraint(fields=("user", "achievement"), name="unique_user_achievement"),
        ),
    ]
