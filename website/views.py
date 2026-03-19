from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import SiteSettings, Project, Skill, Experience, ContactMessage

def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        user_message = request.POST.get('message')

        # 1. حفظ الرسالة في قاعدة البيانات
        ContactMessage.objects.create(name=name, email=email, message=user_message)

        # فحص المسار لتحديد ثيم الإيميل
        is_office = 'office' in request.path

        if is_office:
            # --- تصميم Dunder Mifflin Memo ---
            subject = f"📎 OFFICE_MEMO: New Inquiry from {name}"
            html_message = f"""
            <div style="background-color: #fdfdfd; padding: 40px; font-family: 'Courier New', Courier, monospace; color: #2d2d2d; border: 2px solid #ddd; max-width: 600px; margin: auto; box-shadow: 10px 10px 0px #003366;">
                <div style="border-bottom: 4px solid #003366; padding-bottom: 10px; margin-bottom: 30px; text-align: center;">
                    <h1 style="margin: 0; color: #003366; font-size: 24px; font-weight: 900;">DUNDER MIFFLIN</h1>
                    <p style="margin: 0; font-size: 10px; text-transform: uppercase; color: #666;">Scranton Branch | Internal Correspondence</p>
                </div>
                <p><strong>TO:</strong> Regional Manager</p>
                <p><strong>FROM:</strong> {name} ({email})</p>
                <p><strong>RE:</strong> Business Opportunity / Inquiry</p>
                <hr style="border: 0.5px solid #ccc; margin: 20px 0;">
                <div style="min-height: 100px; line-height: 1.6;">{user_message}</div>
                <div style="margin-top: 40px; border-top: 4px solid #f9d71c; padding-top: 15px; font-size: 11px; color: #777;">
                    <p>"You miss 100% of the shots you don't take. - Wayne Gretzky" - Michael Scott</p>
                    <p style="text-align: center; letter-spacing: 2px;">BEARS. BEETS. BATTLESTAR GALACTICA.</p>
                </div>
            </div>
            """
        else:
            # --- تصميم السايبر الخارق (Hyper-Cyberpunk Design) ---
            subject = f"⚡ [NEURAL_OVERRIDE]: DATA_STREAM FROM {name.upper()}"
            html_message = f"""
            <div style="background-color: #020205; padding: 2px; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; max-width: 600px; margin: auto;">
                <div style="background: linear-gradient(135deg, #EB3678 0%, #FB773C 100%); padding: 1px;">
                    <div style="background-color: #050112; padding: 40px; border: 1px solid #1a1a2e;">
                        
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; border-bottom: 1px solid #30363d; padding-bottom: 15px;">
                            <div style="color: #EB3678; font-weight: 900; letter-spacing: 5px; font-size: 12px; font-family: 'Courier New', monospace;">
                                INCOMING_LINK_STABLISHED
                            </div>
                            <div style="color: #FB773C; font-size: 10px; font-family: 'Courier New', monospace;">
                                STATUS: <span style="color: #00ff41; text-shadow: 0 0 5px #00ff41;">SECURE</span>
                            </div>
                        </div>

                        <h2 style="color: #ffffff; text-transform: uppercase; font-size: 28px; margin-bottom: 5px; letter-spacing: -1px; font-weight: 900;">
                            Neural <span style="color: #EB3678;">Stream</span>
                        </h2>
                        <p style="color: #FB773C; font-size: 11px; margin-top: 0; font-family: 'Courier New', monospace; text-transform: uppercase;">>> Origin_Node: {name}</p>

                        <div style="background: rgba(235, 54, 120, 0.1); border-left: 4px solid #EB3678; padding: 20px; margin: 25px 0;">
                            <table style="width: 100%; border-collapse: collapse;">
                                <tr>
                                    <td style="color: #EB3678; font-size: 10px; font-family: 'Courier New', monospace; padding-bottom: 5px;">SOURCE_ID:</td>
                                    <td style="color: #ffffff; font-size: 14px; padding-bottom: 5px; font-weight: bold;">{name}</td>
                                </tr>
                                <tr>
                                    <td style="color: #EB3678; font-size: 10px; font-family: 'Courier New', monospace;">UPLINK_ADDR:</td>
                                    <td style="color: #FB773C; font-size: 14px; font-weight: bold;">{email}</td>
                                </tr>
                            </table>
                        </div>

                        <div style="margin-top: 30px;">
                            <p style="color: #ffffff; font-size: 12px; font-family: 'Courier New', monospace; margin-bottom: 10px;">[ MESSAGE_PAYLOAD ]</p>
                            <div style="background: #0d1117; padding: 25px; border-radius: 4px; border: 1px solid #30363d; line-height: 1.8; color: #c9d1d9; font-size: 15px; position: relative; overflow: hidden;">
                                <div style="position: absolute; top: 0; left: 0; width: 100%; height: 2px; background: linear-gradient(90deg, transparent, #EB3678, transparent);"></div>
                                {user_message}
                            </div>
                        </div>

                        <div style="margin-top: 40px; text-align: center;">
                            <div style="height: 1px; background: linear-gradient(90deg, transparent, #30363d, transparent); margin-bottom: 20px;"></div>
                            <p style="color: #EB3678; font-size: 10px; letter-spacing: 3px; font-family: 'Courier New', monospace; margin: 0;">ALHANOUF // NEURAL_ARCHITECT</p>
                            <p style="color: #555; font-size: 9px; margin-top: 5px;">TIMESTAMP: 2026_SESSION_CORE</p>
                        </div>
                    </div>
                </div>
            </div>
        
            """

        plain_message = f"Message from {name} ({email}): {user_message}"

        try:
            send_mail(
                subject,
                plain_message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                html_message=html_message,
                fail_silently=False,
            )
            messages.success(request, "SUCCESS: Transmission received." if not is_office else "MEMO_SENT: Message delivered to the annex.")
        except Exception as e:
            messages.error(request, "ERROR: Connection failed.")

    settings_data = SiteSettings.objects.first()
    projects = Project.objects.all().order_by('order')
    skills = {
        'Core Languages': Skill.objects.filter(category='Languages'),
        'Web Architecture': Skill.objects.filter(category='Web Architecture'),
        'Data Intelligence': Skill.objects.filter(category='Data Intelligence'),
        'Infrastructure & Tools': Skill.objects.filter(category='Infrastructure'),
    }
    work_experiences = Experience.objects.filter(type='work').order_by('order')
    education_experiences = Experience.objects.filter(type='edu').order_by('order')

    context = {
        'settings': settings_data,
        'projects': projects,
        'skills': skills,
        'work_exp': work_experiences,
        'edu_exp': education_experiences,
    }

    if 'office' in request.path:
        return render(request, 'index_office.html', context)
    
    return render(request, 'index.html', context)