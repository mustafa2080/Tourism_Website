# destinations/models.py
from django.db import models
from django.utils.text import slugify
from django.conf import settings



# destinations/models.py
class Destination(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, null=True)  # تأكد من أن unique=True
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/', null=True, blank=True)
    location = models.CharField(max_length=200)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # إنشاء slug إذا لم يكن موجودًا
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Destinations"
    
    
# destinations/models.py
class Review(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)