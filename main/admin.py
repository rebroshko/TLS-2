from django.contrib import admin
from .models import Post, Contact, Calendar, Record


admin.site.register(Contact)


@admin.register(Record)
class Record(admin.ModelAdmin):
    list_display = ('name', 'phone', 'choice_Rec')
    list_filter = ('choice_Rec', 'name')
    search_fields = ('name', 'phone', 'choice_Rec')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'publish', 'status')
    list_filter = ('status', 'created', 'publish')
    search_fields = ('title', 'body', 'short')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_go', 'publish', 'status')
    list_filter = ('status', 'created', 'date_go', 'publish')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

