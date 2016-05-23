def is_allowed(user,groups):
    # FIXME Fetches whole memberprofile, wasteful!
    user_groups = user.memberprofile.user_groups_values()
    for group in user_groups:
        if group in groups:
            return True
    return False

# Training: 2,3,7
# Trips: 2,3,4,7
# Sites: 2,3,4,5,6,7
# Members: 2,3,6,7
# Diving Off: 2,7
# Admin: 2

def is_all(user):
    return True

def is_verified(user):
    return not user.memberprofile.new_notify

def is_instructor(user):    #User is either by having a qualification or being training
    groups=[2,3,7]
    if is_allowed(user,groups):
        return True
    elif user.memberprofile.is_instructor():
        return True
    else:
        return False

def is_trusted(user):
    # is the user trusted with personal data, added as a quick fix for #141
    groups=[2,3,6,7]
    return is_allowed(user, groups)

def is_training(user):
    groups=[2,3,7]
    return is_allowed(user,groups)
def is_trips(user):
    groups=[2,3,4,7]
    return is_allowed(user,groups)
def is_sites(user):
    groups=[2,3,4,5,6,7]
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
