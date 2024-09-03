from django.db import models

# Create your models here.
class vowner(models.Model):
    owname = models.CharField(max_length=50)
    mobile = models.CharField(max_length=40)
    photo = models.ImageField(upload_to='images/')
    vname = models.CharField(max_length=50)
    vnumber = models.CharField(max_length=50)
    vphoto = models.ImageField(upload_to='images/')
    mincharge = models.IntegerField()
    rate = models.IntegerField()
    uname = models.CharField(max_length=50)
    pword = models.CharField(max_length=50)
    status=models.CharField(max_length=50, default='NT')

class staff(models.Model):
    sname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    mobile = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='images/')
    uname = models.CharField(max_length=50)
    pword = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='NS')

class Userreg(models.Model):
    usname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    mobile = models.CharField(max_length=50)
    idproof = models.ImageField(upload_to='images/')
    photo = models.ImageField(upload_to='images/')
    uname = models.CharField(max_length=50)
    pword = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='User')

class roomtype(models.Model):
    rmtype = models.CharField(max_length=50)
    nobeds = models.IntegerField()
    photo = models.ImageField(upload_to='images/')
    rate = models.IntegerField()

class room(models.Model):
    rno = models.IntegerField()
    rt = models.CharField(max_length=40)

class booking(models.Model):
    bno = models.IntegerField()
    bdate = models.DateField()
    custid = models.IntegerField()
    custname = models.CharField(max_length=50)
    nop = models.IntegerField(default=0)
    rtype = models.CharField(max_length=50)
    datef = models.DateField()
    dateto = models.DateField()
    nod = models.IntegerField()
    totamt = models.IntegerField()
    cardno = models.CharField(max_length=50)
    status = models.CharField(max_length=30, default='NB')

class bsub(models.Model):
    bno = models.IntegerField()
    bdate = models.DateField()
    rtype = models.CharField(max_length=50)
    rno = models.IntegerField()

class temp(models.Model):
    rno = models.IntegerField()

class temp1(models.Model):
    rno = models.IntegerField()
