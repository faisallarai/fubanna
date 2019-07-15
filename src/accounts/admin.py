from django.contrib import admin

from django.contrib.auth import get_user_model
from .models import Agent

User = get_user_model()


class AgentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'slug')

    class Meta:
        model = Agent


admin.site.register(User)
admin.site.register(Agent, AgentAdmin)
