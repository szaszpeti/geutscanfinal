from django.db import models
import sys
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from pyuploadcare.dj.models import ImageField

# Create your models here.

class Technician(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Inspection(models.Model):

	date = models.DateTimeField(auto_now_add=True)
	location = models.CharField(max_length=50)
	wtglocalnumber = models.CharField(max_length=3)
	wtgnumber = models.CharField(max_length=15)
	technician_one = models.ForeignKey(Technician, null=True, on_delete= models.SET_NULL)
	technician_two = models.CharField(max_length=50)
	technician_three = models.CharField(max_length=50, null=True, blank=True)
	notes = models.TextField(null=True, blank=True)
	#picture = models.ImageField(null=True)

	TRAVEL_OFFICE_WTG = 'Travel Office --> WTG'
	TRAVEL_WTG_OFFICE = 'Travel WTG --> Office'
	TRAVEL_HOTEL_WTG = 'Travel Hotel --> WTG'
	TRAVEL_WTG_HOTEL = 'Travel WTG --> Hotel'
	TRAVEL_EXTRA = 'Travel Extra'
	WORK_PREPARATION = 'Work Preparation'
	UT_INSPECTION = 'UT Inspection'
	STANDBY_WEATHER = 'Standby Weather'
	STANDBY_WTG_DISORDER = 'Standby WTG Disorder'
	CLEANING = 'Cleaning'
	OTHER = 'Other'

	ACTIVITY = [(TRAVEL_OFFICE_WTG, 'Travel Office --> WTG '),
				(TRAVEL_WTG_OFFICE, 'Travel WTG --> Office'),
				(TRAVEL_HOTEL_WTG, 'Travel Hotel --> WTG'),
				(TRAVEL_WTG_HOTEL, 'Travel WTG --> Hotel'),
				(TRAVEL_EXTRA, 'Travel Extra'),
				(WORK_PREPARATION, 'Work Preparation'),
				(UT_INSPECTION, 'UT Inspection'),
				(STANDBY_WEATHER, 'Standby Weather'),
				(STANDBY_WTG_DISORDER, 'Standby WTG Disorder'),
				(CLEANING, 'Cleaning'),
				(OTHER, 'Other'),
				]

	activity_1 = models.CharField(choices=ACTIVITY, max_length=50)
	time_start_1 = models.TimeField(null=True,blank=True, auto_now=False, auto_now_add=False)
	time_end_1 = models.TimeField(null=True,blank=True, auto_now=False, auto_now_add=False)
	note_1 = models.CharField(max_length=200, blank=True)

	activity_2 = models.CharField(choices=ACTIVITY, max_length=50)
	time_start_2 = models.TimeField(null=True,blank=True, auto_now=False, auto_now_add=False)
	time_end_2 = models.TimeField(null=True,blank=True, auto_now=False, auto_now_add=False)
	note_2 = models.CharField(max_length=200, blank=True)

	activity_3 = models.CharField(choices=ACTIVITY, max_length=50)
	time_start_3 = models.TimeField(null=True,blank=True, auto_now=False, auto_now_add=False)
	time_end_3 = models.TimeField(null=True,blank=True, auto_now=False, auto_now_add=False)
	note_3 = models.CharField(max_length=200, blank=True)

	activity_4 = models.CharField(choices=ACTIVITY, max_length=50)
	time_start_4 = models.TimeField(null=True,blank=True, auto_now=False, auto_now_add=False)
	time_end_4 = models.TimeField(null=True,blank=True, auto_now=False, auto_now_add=False)
	note_4 = models.CharField(max_length=200, blank=True)

	activity_5 = models.CharField(choices=ACTIVITY, max_length=50)
	time_start_5 = models.TimeField(null=True,blank=True, auto_now=False, auto_now_add=False)
	time_end_5 = models.TimeField(null=True,blank=True, auto_now=False, auto_now_add=False)
	note_5 = models.CharField(max_length=200, blank=True)

	activity_6 = models.CharField(choices=ACTIVITY, max_length=50)
	time_start_6 = models.TimeField(null=True,blank=True, auto_now=False, auto_now_add=False)
	time_end_6 = models.TimeField(null=True,blank=True, auto_now=False, auto_now_add=False)
	note_6 = models.CharField(max_length=200,blank=True)

	photo = ImageField(blank=True, manual_crop="")

	def __str__(self):
		return f'{self.location + " - " + self.wtgnumber}'



class InspectionImage(models.Model):
    inspection = models.ForeignKey(Inspection, default=None, on_delete=models.CASCADE)
    images = models.FileField(upload_to = 'images/')

    def save(self, *args, **kwargs):
        if not self.id:
            self.images = self.compressImage(self.images)
        super(InspectionImage, self).save(*args, **kwargs)

    def compressImage(self,images):
        imageTemproary = Image.open(images)
        outputIoStream = BytesIO()
        #imageTemproaryResized = imageTemproary.resize( (1020,573) )
        imageTemproary.save(outputIoStream , format='JPEG', quality=60)
        outputIoStream.seek(0)
        images = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % images.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return images


    def __str__(self):
        return self.inspection.wtgnumber

class Post(models.Model):
    photo = ImageField(blank=True, manual_crop="")
# class Tag(models.Model):
#     name = models.CharField(max_length=200, null=True)

#     def __str__(self):
#         return self.name

# class Product(models.Model):
#     CATEGORY = (
#             ('Indoor', 'Indoor'),
#             ('Out Door', 'Out Door'),
#             )

#     name = models.CharField(max_length=200, null=True)
#     price = models.FloatField(null=True)
#     category = models.CharField(max_length=200, null=True, choices=CATEGORY)
#     description = models.CharField(max_length=200, null=True, blank=True)
#     date_created = models.DateTimeField(auto_now_add=True, null=True)
#     tags = models.ManyToManyField(Tag)

#     def __str__(self):
#         return self.name

# class Order(models.Model):
#     STATUS = (
#             ('Pending', 'Pending'),
#             ('Out for delivery', 'Out for delivery'),
#             ('Delivered', 'Delivered'),
#             )

#     customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
#     product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
#     date_created = models.DateTimeField(auto_now_add=True, null=True)
#     status = models.CharField(max_length=200, null=True, choices=STATUS)
#     note = models.CharField(max_length=1000, null=True)

#     def __str__(self):
#         return self.product.name

