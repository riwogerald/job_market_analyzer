# Generated migration for adding GIN indexes to array fields

from django.db import migrations
from django.contrib.postgres.indexes import GinIndex


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='jobposting',
            index=GinIndex(fields=['skills_required'], name='jobs_jobposting_skills_gin'),
        ),
        migrations.AddIndex(
            model_name='jobposting',
            index=GinIndex(fields=['technologies'], name='jobs_jobposting_tech_gin'),
        ),
    ]
