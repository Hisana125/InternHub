from django.contrib import admin
from django.utils.html import format_html
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'name', 'email', 'phone', 'course', 'resume_link', 'created_at')
    search_fields = ('registration_number', 'name', 'email', 'phone', 'course')
    list_filter = ('course', 'created_at')

    def resume_link(self, obj):
        if obj.resume:
            return format_html('<a href="{}" target="_blank" style="font-weight: bold; color: #2563EB;">📄 View Resume</a>', obj.resume.url)
        return format_html('<span style="color: #94A3B8;">Not Uploaded</span>')

    resume_link.short_description = "Resume / CV"
