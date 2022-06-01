from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm


from .models import User, Subscription, Image, TemporaryLink


admin.site.register(Image)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin, DynamicArrayMixin):
    pass


@admin.register(TemporaryLink)
class TemporaryLinkAdmin(admin.ModelAdmin):
    fields = ('image', 'duration', 'expiration', 'slug')
    readonly_fields = ('expiration', 'slug')


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('subscription',)}),
    )


admin.site.register(User, MyUserAdmin)