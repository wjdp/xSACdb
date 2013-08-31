def is_allowed(user,groups):
	for group in user.groups.all():
	    if group.pk in groups:
	        return True
	return False

# Training: 2,3,7
# Trips: 2,3,4,7
# Sites: 2,5,7
# Members: 2,3,6,7
# Diving Off: 2,7
# Admin: 2

def is_training(user):
	groups=[2,3,7]
	return is_allowed(user,groups)
def is_trips(user):
	groups=[2,3,4,7]
	return is_allowed(user,groups)
def is_sites(user):
	groups=[2,5,7]
	return is_allowed(user,groups)
def is_members(user):
	groups=[2,3,6,7]
	return is_allowed(user,groups)
def is_diving_officer(user):
	groups=[2,7]
	return is_allowed(user,groups)
def is_admin(user):
	groups=[2]
	return is_allowed(user,groups)