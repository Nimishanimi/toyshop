from django.db import models

# Create your models here.
class toyreg_tb(models.Model):
	name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password= models.CharField(max_length=255)





##########################################################################################################################################
#################################################ADMIN####################################################################################
class product_tb(models.Model):
	proname=models.CharField(max_length=255)
	price=models.CharField(max_length=255)
	prodescription=models.CharField(max_length=255)
	proimage= models.ImageField(upload_to="product/")

class admreg_tb(models.Model):
	admname = models.CharField(max_length=255)
	admemail = models.CharField(max_length=255)
	admpassword = models.CharField(max_length=255)


class cart_tb(models.Model):
	pid = models.ForeignKey(product_tb, on_delete=models.CASCADE)
	uid = models.ForeignKey(toyreg_tb, on_delete=models.CASCADE)
	pqty = models.CharField(max_length=255)
	totalprice = models.CharField(max_length=255)
	status = models.CharField(max_length=255,default="pending")

class check_tb(models.Model):
	fname=models.CharField(max_length=255)
	pnumber=models.CharField(max_length=255)
	landm=models.CharField(max_length=255)
	town=models.CharField(max_length=255)
	uid = models.ForeignKey(toyreg_tb, on_delete=models.CASCADE)
	


class pay_tb(models.Model):
	uid = models.ForeignKey(toyreg_tb, on_delete=models.CASCADE)
	totalp= models.CharField(max_length=255)
	pstatus= models.CharField(max_length=255,default="pending")
	


	