from django.contrib import admin
from django.utils.html import format_html
from .models import CustomUser, student, Employer

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('email', 'name')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'email', 'phone_number', 'district', 'verification_status', 'view_id_card')
    list_filter = ('verification_status', 'academic_status', 'district')
    search_fields = ('student_name', 'email', 'phone_number')
    list_editable = ('verification_status',) # Allow toggling verification directly from list

    def view_id_card(self, obj):
        if obj.id_card:
            return format_html('<a href="{}" target="_blank" class="button">View ID Card</a>', obj.id_card.url)
        return "No ID Uploaded"
    view_id_card.short_description = 'ID Card'

class EmployerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_person', 'email', 'phone', 'verification_status', 'district')
    list_filter = ('verification_status', 'district', 'industry')
    search_fields = ('company_name', 'email', 'phone')
    list_editable = ('verification_status',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(student, StudentAdmin)
admin.site.register(Employer, EmployerAdmin)
