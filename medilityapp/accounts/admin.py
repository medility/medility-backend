from django.contrib.auth import get_user_model
from django.contrib import admin
from accounts.models import User, AddressList

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm


from .models import Profile, PhoneOTP

admin.site.register(PhoneOTP)


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('name', 'phone',  'admin',)
    list_filter = ('staff','active' ,'admin', )
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('name', 'email', 'dob', 'gender', 'primary_user_ref', 'user_type')}),
        ('Permissions', {'fields': ('admin','staff','active', 'is_account_activate', 'is_family_member')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2')}
        ),
    )


    # search_fields = ('phone','name')
    ordering = ['id']
    # filter_horizontal = ()
    #
    #
    #
    # def get_inline_instances(self, request, obj=None):
    #     if not obj:
    #         return list()
    #     return super(UserAdmin, self).get_inline_instances(request, obj)

admin.site.register(User, UserAdmin),
admin.site.register(AddressList),




# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)