from django.contrib import admin

from .models import Critique


class CritiqueAdmin(admin.ModelAdmin):
    fields = ("url", "message", "email", "user_agent", "created",)
    list_display = ("id", "url", "get_message", "email", "user_agent", "created",)
    list_filter = ("created",)
    readonly_fields = ("created",)
    search_fields = ("url", "email",)

    def get_message(self, obj):
        """Returns a truncated 'message' field."""
        return "{0}...".format(obj.message[:60])
    get_message.short_description = "Message"


admin.site.register(Critique, CritiqueAdmin)
