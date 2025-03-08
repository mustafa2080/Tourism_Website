from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('destinations', '0002_auto_populate_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destinations', to='destinations.category'),
        ),
    ]
