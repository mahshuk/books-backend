
from django.db import models


class Page (models.Model):
    book_name = models.CharField(max_length=255)
    category = models.ManyToManyField("pages.Category")
    description = models.TextField()
    user_name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    featured_image = models.FileField(upload_to="media/Book_image",null=True,blank=True)
    
    like = models.ManyToManyField("auth.User")
    class Meta: 
        ordering = ["-date"]

    def __str__(self):
        return self.book_name
    

class Category (models.Model):
    name = models.CharField(max_length=255)

    class Meta : 
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
    

class Comment (models.Model):
    comment = models.TextField()
    username = models.ForeignKey("auth.User",on_delete=models.CASCADE)
    book = models.ForeignKey("pages.Page",on_delete=models.CASCADE)    
    is_deleted = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta :
        ordering = ["-date"]


    def __str__(self):
        return self.comment