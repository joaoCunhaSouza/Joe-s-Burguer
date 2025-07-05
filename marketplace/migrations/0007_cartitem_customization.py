from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0006_cartitem_combo'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='customization',
            field=models.JSONField(default=dict, blank=True, null=True),
        ),
    ]
