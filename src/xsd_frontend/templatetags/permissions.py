from __future__ import unicode_literals

from django import template

register = template.Library()

@register.tag()
def permission(parser, token):
    try:
        # get the arguments passed to the template tag;
        # first argument is the tag name
        tag_name, username, permission, object = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly 3 arguments" % token.contents.split()[0])
    # look for the 'endpermission' terminator tag
    nodelist = parser.parse(('endpermission',))
    parser.delete_first_token()
    return PermissionNode(nodelist, username, permission, object)


class PermissionNode(template.Node):
    def __init__(self, nodelist, user, permission, object):
        self.nodelist = nodelist
        # evaluate the user instance as a variable and store
        self.user = template.Variable(user)
        # store the permission string
        self.permission = permission
        # evaluate the object instance as a variable and store
        self.object = template.Variable(object)

    def render(self, context):
        user_inst = self.user.resolve(context)
        object_inst = self.object.resolve(context)

        content = self.nodelist.render(context)

        # Permissions directly on model
        if hasattr(object_inst, self.permission):
            # check to see if the permissions object has the permissions method
            # provided in the template tag
            perm_func = getattr(object_inst, self.permission)
            # execute that permissions method
            if perm_func(user_inst):
                return content
        # Permissions on permissions sub-object
        if hasattr(object_inst, 'permissions'):
            # check to see if the permissions object has the permissions method
            # provided in the template tag
            perm_func = getattr(object_inst.permissions, self.permission)
            # execute that permissions method
            if perm_func(user_inst):
                return content
        return ""


