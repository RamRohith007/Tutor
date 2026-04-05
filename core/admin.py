
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Admission, Phase, Assignment, CourseBatch, Note, Recording
from .models import CurriculumPhase, CurriculumSection, PracticumProject, PracticumVertical
from .models import Faculty, LogisticsSession, EnrollmentFee

# Faculty
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("name", "title")

# Logistics
@admin.register(LogisticsSession)
class LogisticsSessionAdmin(admin.ModelAdmin):
    list_display = ("order", "title")
    ordering = ("order",)

# Enrollment Fee
@admin.register(EnrollmentFee)
class EnrollmentFeeAdmin(admin.ModelAdmin):
    list_display = ("currency_inr", "currency_usd")

class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "user_type",
        "active",
        "current_role",
        "mobile_number",
        "enrolled_batch",
        "faculty",
        "is_staff",
        "is_superuser",
    )
    list_filter = ("user_type", "active", "is_staff", "is_superuser")
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("user_type", "active", "current_role", "mobile_number", "enrolled_batch", "faculty")} ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": ("user_type", "active", "current_role", "mobile_number", "enrolled_batch", "faculty")} ),
    )
    search_fields = ("username", "email", "faculty__name", "mobile_number", "enrolled_batch__name")

admin.site.register(User, CustomUserAdmin)
admin.site.register(Admission)
admin.site.register(Phase)
admin.site.register(Assignment)

@admin.register(CourseBatch)
class CourseBatchAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date", "faculty", "is_active")
    list_filter = ("is_active", "faculty")
    search_fields = ("name", "faculty__name")

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "batch", "created_by", "created_at")
    list_filter = ("batch", "created_by")
    search_fields = ("title", "content")

@admin.register(Recording)
class RecordingAdmin(admin.ModelAdmin):
    list_display = ("title", "batch", "created_by", "created_at")
    list_filter = ("batch", "created_by")
    search_fields = ("title", "url")

@admin.register(CurriculumPhase)
class CurriculumPhaseAdmin(admin.ModelAdmin):
	list_display = ("order", "title")
	ordering = ("order",)

@admin.register(CurriculumSection)
class CurriculumSectionAdmin(admin.ModelAdmin):
	list_display = ("phase", "order", "name")
	ordering = ("phase", "order")

@admin.register(PracticumProject)
class PracticumProjectAdmin(admin.ModelAdmin):
	list_display = ("order", "title", "icon")
	ordering = ("order",)

@admin.register(PracticumVertical)
class PracticumVerticalAdmin(admin.ModelAdmin):
	list_display = ("order", "name")
	ordering = ("order",)
