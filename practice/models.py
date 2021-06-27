

from django.db import models
# Create your models here.


class user_info(models.Model):
    user_id = models.AutoField(primary_key=True,blank=False,null=False)
    first_name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    password = models.CharField(max_length=6,blank=False,null=False)
    
    
    def disp(self):
        print(self.user_id,' ',self.first_name,' ',self.designation)   

    def __str__(self):
        return self.first_name 



class blog_det(models.Model):
    blog_name = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    owner = models.ForeignKey(user_info,on_delete=models.CASCADE)
def __str__(self):
    return f'{self.text[:30]}...'





