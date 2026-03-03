from django.contrib import admin
from .models import SiteSettings, Project, Skill, Experience, ContactMessage

# 1. تخصيص إعدادات الموقع
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('English Content (Hero)', {
            'fields': ('hero_title_en', 'hero_desc_en', 'contact_desc_en')
        }),
        ('Arabic Content (Hero)', {
            'fields': ('hero_title_ar', 'hero_desc_ar', 'contact_desc_ar')
        }),
        ('Social Media Links', {
            'fields': ('linkedin_url', 'github_url', 'twitter_url'),
            'classes': ('collapse',),
        }),
    )

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

# 2. تنظيم المشاريع - تم تعديل list_display_links لحل الخطأ
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('order', 'name', 'tech_stack') 
    list_display_links = ('name',) # جعل الاسم هو الرابط بدلاً من الترتيب
    list_editable = ('order',) 
    search_fields = ('name', 'title_en', 'title_ar')
    list_filter = ('tech_stack',)
    
    fieldsets = (
        ('Core Info', {'fields': ('name', 'tech_stack', 'order','image')}),
        ('Content (EN)', {'fields': ('title_en', 'description_en')}),
        ('Content (AR)', {'fields': ('title_ar', 'description_ar')}),
        ('Dev Source', {'fields': ('code_snippet',)}),
    )

# 3. تنظيم الخبرات والتعليم - تم إضافة list_display_links لحل الخطأ
@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('order', 'title_en', 'organization_en', 'type', 'period')
    list_display_links = ('title_en',) # جعل العنوان هو الرابط لفتح التعديل
    list_editable = ('order',)
    list_filter = ('type',)
    search_fields = ('organization_en', 'title_en')

# 4. تنظيم المهارات
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

# 5. رسائل التواصل
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    readonly_fields = ('name', 'email', 'message', 'created_at')
    search_fields = ('name', 'email')

# تخصيص نصوص لوحة التحكم
admin.site.site_header = "ALHANOUF Architecture | Control Center"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to your Neural Network Management"