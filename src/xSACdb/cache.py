from __future__ import unicode_literals

from django.core.cache import cache

def object_cache_key(model, pk, name):
    return '{0}_{1}_{2}'.format(model, pk, name)


class object_cached_property(object):
    """
    Decorator that converts a method with a single self argument into a
    property cached on the instance in redis.
    """
    def __init__(self, func, name=None):
        self.func = func
        self.name = name or func.__name__


    def __get__(self, instance, type=None):
        # if instance is None:
        #     return self
        # res = instance.__dict__[self.name] = self.func(instance)
        cache_key = object_cache_key(type(instance).__class__.__name__, instance.pk, self.name)
        if cache.get(cache_key):
            return cache.get(cache_key)
        else:
            value = self.func(instance)
            cache.set(cache_key, value)
            return value

class ObjectPropertyCacheInvalidationMixin(object):
    """Invalidates object_cached_property on save"""
    def get_cached_properties(self):
        """Returns list of properties to clear. Setup as a function so mixins can append to."""
        return []

    def invalidate_object_property_cache(self, property):
        """Invalidate a single property, useful for calling from elsewhere"""
        cache.delete(object_cache_key(self.__class__.__name__, self.pk, property))

    def invalidate_object_property_cache_all(self):
        """Invalidate all cached properties that are definded via get_cached_properties"""
        for property in self.get_cached_properties():
            self.invalidate_object_property_cache(property)

    def save(self):
        self.invalidate_object_property_cache_all()
        return super(ObjectPropertyCacheInvalidationMixin, self).save()
