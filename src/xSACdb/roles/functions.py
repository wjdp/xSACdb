from .groups import *

# FIXME Replace with a permission based model...


def is_allowed(user, groups):
    # FIXME Fetches whole memberprofile, wasteful! Make request select memberprofile every req
    if not is_verified(user):
        # Should be verified before any group stuff is allowed
        return False

    user_groups = user.memberprofile.user_groups_values()
    for group in user_groups:
        if group in groups:
            return True
    return False


def is_all(user):
    return True


def is_verified(user):
    return user.memberprofile.verified


def is_instructor(user):  # User is either by having a qualification or being training
    groups = [GROUP_ADMIN, GROUP_TRAINING, GROUP_DO]
    if is_allowed(user, groups):
        return True
    elif user.memberprofile.is_instructor() and is_verified(user):
        return True
    else:
        return False


def is_trusted(user):
    # is the user trusted with personal data, added as a quick fix for #141
    groups = [GROUP_ADMIN, GROUP_TRAINING, GROUP_MEMBERS, GROUP_DO]
    return is_allowed(user, groups)


def is_training(user):
    groups = [GROUP_ADMIN, GROUP_TRAINING, GROUP_DO]
    return is_allowed(user, groups)


def is_trips(user):
    groups = [GROUP_ADMIN, GROUP_TRAINING, GROUP_TRIPS, GROUP_DO]
    return is_allowed(user, groups)


def is_sites(user):
    groups = [GROUP_ADMIN, GROUP_TRAINING, GROUP_TRIPS, GROUP_SITES, GROUP_MEMBERS, GROUP_DO]
    return is_allowed(user, groups)


def is_members(user):
    groups = [GROUP_ADMIN, GROUP_TRAINING, GROUP_MEMBERS, GROUP_DO]
    return is_allowed(user, groups)


def is_diving_officer(user):
    groups = [GROUP_ADMIN, GROUP_DO]
    return is_allowed(user, groups)


def is_admin(user):
    groups = [GROUP_ADMIN]
    return is_allowed(user, groups)
