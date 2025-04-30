from apps.users.models import User

EMAIL_TEMPLATE = """
<div style="font-family: Arial, sans-serif; padding: 20px;">
    <h2 style="color: #333;">Добро пожаловать, {first_name}!</h2>
    <p>Ваш код подтверждения: <strong style="font-size: 20px;">{code}</strong></p>
    <p>Введите этот код в приложении, чтобы завершить регистрацию.</p>
    <br>
    <p>С уважением,<br>Ваша команда</p>
</div>
"""

RESEND_FORM = """
    <p>Здравствуйте, {first_name}!</p>
    <p>Вы запросили сброс пароля. Для продолжения перейдите по следующей ссылке:</p>
    <p>
        <a href="" style="background-color: #4CAF50; color: white; padding: 14px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 4px;">
            Сменить пароль
        </a>
    </p>
    <p>Если вы не запрашивали сброс пароля, просто игнорируйте это письмо.</p>
"""