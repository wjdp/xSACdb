def get_user_display(user):
    """Adaptor for allauth ACCOUNT_USER_DISPLAY"""
    return user.get_full_name()
