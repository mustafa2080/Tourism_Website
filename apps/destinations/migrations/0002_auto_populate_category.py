from django.db import migrations

def create_default_category(apps, schema_editor):
    Category = apps.get_model('destinations', 'Category')
    Destination = apps.get_model('destinations', 'Destination')
    
    # Create default category if it doesn't exist
    default_category, created = Category.objects.get_or_create(
        name='عام',
        defaults={
            'description': 'الفئة الافتراضية',
            'slug': 'general'
        }
    )
    
    # Update all destinations without category
    Destination.objects.filter(category__isnull=True).update(category=default_category)

def reverse_default_category(apps, schema_editor):
    Category = apps.get_model('destinations', 'Category')
    Category.objects.filter(name='عام').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('destinations', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_category, reverse_default_category),
    ]
