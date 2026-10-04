from django.contrib import admin
from .models import Internship, Application, Notification, Payment

# Custom Admin Site Branding
admin.site.site_header = "InternHub Administration Portal"
admin.site.site_title = "InternHub Admin"
admin.site.index_title = "College Internship & Application Management"


@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'company_name',
        'location',
        'duration',
        'stipend',
        'application_deadline',
        'created_at',
    )
    search_fields = (
        'title',
        'company_name',
        'location',
        'skills_required',
    )
    list_filter = (
        'location',
        'application_deadline',
        'created_at',
    )
    ordering = ('-created_at',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'student_name',
        'internship_title',
        'amount',
        'status',
        'payment_method',
        'transaction_id',
        'paid_at',
    )
    list_filter = (
        'status',
        'payment_method',
        'paid_at',
    )
    search_fields = (
        'application__student__name',
        'application__student__email',
        'application__internship__title',
        'transaction_id',
    )
    ordering = ('-paid_at',)

    def student_name(self, obj):
        return obj.application.student.name
    student_name.short_description = "Student"

    def internship_title(self, obj):
        return obj.application.internship.title
    internship_title.short_description = "Internship"


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'internship',
        'status',
        'payment_status_badge',
        'applied_at',
    )
    list_filter = (
        'status',
        'payment__status',
        'internship',
        'applied_at',
    )
    search_fields = (
        'student__name',
        'student__email',
        'internship__title',
        'internship__company_name',
    )

    def payment_status_badge(self, obj):
        if hasattr(obj, 'payment'):
            if obj.payment.status == 'Success':
                return f"✓ Paid (₹{obj.payment.amount})"
            return f"⏳ Pending (₹{obj.payment.amount})"
        return "—"
    payment_status_badge.short_description = "Application Fee"
    ordering = ('-applied_at',)
    actions = [
        'mark_under_review',
        'mark_shortlisted',
        'mark_selected',
        'mark_rejected',
    ]

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = Application.objects.get(pk=obj.pk)
            if old_obj.status != obj.status:
                Notification.objects.create(
                    student=obj.student,
                    message=(
                        f"Your application for "
                        f"'{obj.internship.title}' has been "
                        f"updated to {obj.status}."
                    )
                )
        super().save_model(request, obj, form, change)

    @admin.action(description="Mark selected applications as Under Review")
    def mark_under_review(self, request, queryset):
        count = 0
        for app in queryset:
            if app.status != 'Under Review':
                app.status = 'Under Review'
                app.save()
                Notification.objects.create(
                    student=app.student,
                    message=f"Your application for '{app.internship.title}' is now Under Review."
                )
                count += 1
        self.message_user(request, f"{count} applications marked as Under Review.")

    @admin.action(description="Mark selected applications as Shortlisted")
    def mark_shortlisted(self, request, queryset):
        count = 0
        for app in queryset:
            if app.status != 'Shortlisted':
                app.status = 'Shortlisted'
                app.save()
                Notification.objects.create(
                    student=app.student,
                    message=f"Congratulations! Your application for '{app.internship.title}' has been Shortlisted."
                )
                count += 1
        self.message_user(request, f"{count} applications marked as Shortlisted.")

    @admin.action(description="Mark selected applications as Selected")
    def mark_selected(self, request, queryset):
        count = 0
        for app in queryset:
            if app.status != 'Selected':
                app.status = 'Selected'
                app.save()
                Notification.objects.create(
                    student=app.student,
                    message=f"Congratulations! You have been Selected for the '{app.internship.title}' internship!"
                )
                count += 1
        self.message_user(request, f"{count} applications marked as Selected.")

    @admin.action(description="Mark selected applications as Rejected")
    def mark_rejected(self, request, queryset):
        count = 0
        for app in queryset:
            if app.status != 'Rejected':
                app.status = 'Rejected'
                app.save()
                Notification.objects.create(
                    student=app.student,
                    message=f"Update on your application for '{app.internship.title}': Status changed to Rejected."
                )
                count += 1
        self.message_user(request, f"{count} applications marked as Rejected.")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'message',
        'is_read',
        'created_at',
    )
    list_filter = (
        'is_read',
        'created_at',
    )
    search_fields = (
        'student__name',
        'student__email',
        'message',
    )
    ordering = ('-created_at',)