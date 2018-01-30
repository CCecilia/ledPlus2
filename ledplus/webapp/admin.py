from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import User

from .models import Agent, Subtype

# class AgentInline(admin.StackedInline):
#     model = Agent
#     can_delete = False
#     verbose_name_plural = 'agent'

# # Define a new User admin
# class UserAdmin(BaseUserAdmin):
#     inlines = (AgentInline, )

# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(Agent, UserAdmin)
admin.site.register(Subtype)
admin.site.register(Agent)
# admin.site.register(UserAdmin)
