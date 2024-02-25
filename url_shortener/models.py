from djongo import models


class AppUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    _id = models.ObjectIdField(primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'users'


class URL(models.Model):
    short_url = models.CharField(max_length=100, unique=True)
    original_url = models.URLField(unique=True)
    user = models.EmailField()
    _id = models.ObjectIdField(primary_key=True)

    def __str__(self):
        return self.short_url

    class Meta:
        db_table = 'urls'


class UsedURL(models.Model):
    short_url = models.CharField(max_length=100, unique=True)
    _id = models.ObjectIdField(primary_key=True)

    def __str__(self):
        return self.short_url

    class Meta:
        db_table = 'used_urls'
