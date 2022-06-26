from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User, default=User, on_delete=models.CASCADE)
	name = models.CharField(max_length=20, default="Name")	
	profile_img = models.ImageField(upload_to='images/',default='/images/basic.png')
	bg_img = models.ImageField(upload_to='images/',default='/images/basicbg.png')
	bio = models.CharField(max_length=50,default="No Description")
	followers = models.ManyToManyField("self",blank=True, symmetrical=False,related_name='+')
	following = models.ManyToManyField("self",blank=True, symmetrical=False,related_name='+')
	

	@property
	def total_posts(self):
		return self.author.all().count()

class Post(models.Model):
	author = models.ForeignKey(Profile,default=Profile,null=True, on_delete=models.CASCADE,related_name='author')

	text = models.CharField(max_length=100)
	date = models.DateTimeField("Date of Post",auto_now=True)
	likers = models.ManyToManyField(Profile,related_name='likers',default=author)
	sharers = models.ManyToManyField(Profile,related_name='sharers',default=author)

	@property
	def total_comments(self):
		return self.postc.all().count()
	
	@property
	def total_likes(self):
		return self.likers.all().count()
	@property
	def total_sharers(self):
		return self.sharers.all().count()

class Comment(models.Model):

	author = models.ForeignKey(Profile,default=Profile,null=True, on_delete=models.CASCADE,related_name='author1')

	text = models.CharField(max_length=100)

	date = models.DateTimeField("Date of Сomment",auto_now=True)

	post = models.ForeignKey(Post,null=True, on_delete=models.CASCADE,related_name='postc')
