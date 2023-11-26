from django.contrib import admin

from simpleblog.contact.models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'created_at']
    readonly_fields = ['email', 'name', 'content', 'created_at']
    list_filter = ['created_at']
    actions = []
    save_on_top = False
    save_as_continue = False

    def has_add_permission(self, request):
        return False
