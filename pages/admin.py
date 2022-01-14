from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from pages.models import User, Lesson, SubGroup, Group, School, Day, Mark, SchoolSubject, Period



@admin.register(User)
class UserDisplay(UserAdmin):
    # exclude = ('last_login', "user_permissions")
    # fields = ('is_teacher')
    UserAdmin.list_display = ('first_name', 'last_name', 'username', 'is_superuser', )
    UserAdmin.list_filter = ('first_name', 'last_name', 'username', 'is_superuser', )
    list_display = UserAdmin.list_display + ("subgroup", "age", "is_teacher", )
    list_filter = UserAdmin.list_filter + ("is_teacher", "subgroup", "age", )
    fieldsets = UserAdmin.fieldsets
    fieldsets[1][1]['fields'] = ["first_name", "last_name", "subgroup", "age", "is_teacher"]

@admin.register(Lesson)
class LessonDisplay(admin.ModelAdmin):
    list_display = ["students", "subject", "date"]


@admin.register(SubGroup)
class SubGroupDisplay(admin.ModelAdmin):
    list_display = ["group", "index"]


@admin.register(Group)
class GroupDisplay(admin.ModelAdmin):
    list_display = ["name", "school"]


@admin.register(School)
class SchoolDisplay(admin.ModelAdmin):
    list_display = ["address"]


@admin.register(Day)
class DayDisplay(admin.ModelAdmin):
    list_display = ["date"]


@admin.register(Mark)
class MarkDisplay(admin.ModelAdmin):
    list_display = ["mark", "lesson", "student"]


@admin.register(SchoolSubject)
class SubjectDisplay(admin.ModelAdmin):
    list_display = ["name", "school"]


@admin.register(Period)
class PeriodDisplay(admin.ModelAdmin):
    list_display = ["name", "date_from", "date_to"]