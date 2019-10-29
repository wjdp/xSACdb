

class ModelComposeMixin(object):
    """Instantiates objects under each instance of the parent class"""
    # TODO spin out into generic module
    compose_classes = {}

    def __init__(self, *args, **kwargs):
        super(ModelComposeMixin, self).__init__(*args, **kwargs)
        for key, class_ref in self.compose_classes.items():
            setattr(self, key, class_ref(self))

class BaseModelComposeObject(object):
    def __init__(self, instance):
        self.instance = instance

class ModelPermissions(BaseModelComposeObject):
    pass
