from django.db import models

# Create your models here.

class SiteSettings(models.Model):
    # نصوص الهيرو - إنجليزي
    hero_title_en = models.CharField(max_length=200, default="ALHANOUF <br> <span class='text-[#EB3678]'>ALLUHAYDAN</span>")
    hero_desc_en = models.TextField(default="Architecting high-performance digital ecosystems...")
    
    # نصوص الهيرو - عربي
    hero_title_ar = models.CharField(max_length=200, default="الهنوف <br> <span class='text-[#EB3678]'>اللحيدان</span>")
    hero_desc_ar = models.TextField(default="هندسة النظم الرقمية عالية الأداء باستخدام...")

    # نصوص قسم الاتصال
    contact_desc_en = models.TextField(default="Ready to architect the next big thing?")
    contact_desc_ar = models.TextField(default="هل أنت مستعد لبناء المشروع العظيم القادم؟")

    # روابط التواصل الاجتماعي
    linkedin_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    contact_email = models.EmailField(default="alhanoufkhalaf1@gmail.com", help_text="الإيميل الذي سيظهر للزوار")
    class Meta:
        verbose_name = "Global Site Settings"
        verbose_name_plural = "Global Site Settings"

    def __str__(self):
        return "Main Site Content"

# 2. المشاريع (Neural Archives)
class Project(models.Model):
    name = models.CharField(max_length=100, help_text="مثال: HealthLink.cs")
    
    # تفاصيل إنجليزية
    title_en = models.CharField(max_length=200)
    description_en = models.TextField()
    
    # تفاصيل عربية
    title_ar = models.CharField(max_length=200)
    description_ar = models.TextField()
    
    tech_stack = models.CharField(max_length=50, help_text="مثال: C# أو Python")
    code_snippet = models.TextField(help_text="أدخل كود HTML الخاص بتنسيق الألوان هنا")
    order = models.IntegerField(default=0)
    image = models.ImageField(upload_to='projects/', null=True, blank=True)
    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('Languages', '01. Core Languages'),
        ('Web Architecture', '02. Web Architecture'),
        ('Data Intelligence', '03. Data Intelligence'),
        ('Infrastructure', '04. Infrastructure & Tools'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=50) # مثال: PYTHON, DJANGO

    def __str__(self):
        return f"{self.category}: {self.name}"

# 4. الخبرات والتعليم (Experience & Education)
class Experience(models.Model):
    TYPE_CHOICES = [
        ('work', 'Deployment Logs (Work)'),
        ('edu', 'Knowledge Base (Education)'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    
    # تفاصيل إنجليزية
    title_en = models.CharField(max_length=150) # Software Engineer
    organization_en = models.CharField(max_length=150) # Tabuk Health Cluster
    details_en = models.TextField(help_text="استخدم علامة | للفصل بين النقاط")

    # تفاصيل عربية
    title_ar = models.CharField(max_length=150)
    organization_ar = models.CharField(max_length=150)
    details_ar = models.TextField(help_text="استخدم علامة | للفصل بين النقاط")
    
    period = models.CharField(max_length=50) # 2025 - NOW
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.type}: {self.title_en}"

# 5. رسائل التواصل (لحفظ الرسائل التي يرسلها الزوار)
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"