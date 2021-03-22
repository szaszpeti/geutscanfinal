from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Technician



def technician_profile(sender, instance, created, **kwargs):
	if created:
		#after registration the user will be added to the customer group 
		#and will get a customer profile
		group = Group.objects.get(name='technician')
		instance.groups.add(group)
		print('DONE TILL GROUPING')
		Technician.objects.create(
			user = instance,
			name = instance.username,
			)

		print('Customer created')
	else:
		print('NO SIGNALS BEEING ACTIVATED')
		print(sender, instance, created)

post_save.connect(technician_profile, sender=User)