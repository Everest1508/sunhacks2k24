from django.contrib import admin
from .models import Career, Application
# from django import forms
# from ckeditor.widgets import CKEditorWidget

# class CareerAdminForm(forms.ModelForm):
#     description = forms.CharField(widget=CKEditorWidget())
#     requirements = forms.CharField(widget=CKEditorWidget())
#     responsibilities = forms.CharField(widget=CKEditorWidget())

#     class Meta:
#         model = Career
#         fields = '__all__'


class ApplicationInline(admin.TabularInline):
    model = Application
    extra = 0

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    # form = CareerAdminForm
    list_display = ('title', 'location', 'salary', 'is_active', 'created_at', 'updated_at')
    list_filter = ('location', 'salary', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'requirements', 'responsibilities')
    inlines = [ApplicationInline]

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('career', 'user','created_at')
    list_filter = ('created_at',)
    search_fields = ('career__title', 'email')
