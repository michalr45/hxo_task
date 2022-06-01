from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from.models import User, Subscription, Image, TemporaryLink


admin.site.register(User)
admin.site.register(Image)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin, DynamicArrayMixin):
    pass


@admin.register(TemporaryLink)
class TemporaryLinkAdmin(admin.ModelAdmin):
    fields = ('image', 'duration', 'expiration', 'slug')
    readonly_fields = ('expiration', 'slug')
