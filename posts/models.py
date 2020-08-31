from django.db import models
from django.urls import reverse
 
 
class Post(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField('date published', auto_now_add=True)
    author = models.ForeignKey('core.User',
                                on_delete=models.CASCADE,)
    body = models.TextField()
    image = models.ImageField(upload_to='images', default='No image')
 
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('posts:post-view', args=(self.id, ))
        
        
