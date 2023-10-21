from app.settings import Settings

LANGUAGES: dict[str, dict[str, str]] = {
    "RU": {
        "not_admin": "<b>Извините, у вас нет доступа!</b>",
        "welcome": "Добро пожаловать в <b>Subscriby</b>, <i>{0}</i>!",
        "enter_days_for_kpi": "Введите дни периода (>1)",
        "enter_days_for_publish": "Введите дни подписки (<i>как долго будет работать</i>)",
        "api_error": "Не удалось вызвать API!",
        "invalid_number": "Неправильное число!",
        "kpi_period_header": "<b><i>[{0}]: </i></b>\n",
        "btn_create": "🛒 Выдать ключ",
        "btn_revoke": "🔸 Отозвать ключ",
        "btn_kpi": "📈 KPI аналитика",
        "enter_key_to_revoke": "Введите ключ который хотите отозвать",
        "kpi_base": """
📈 <b><u>KPI аналитика</u></b>:\n
<b>Статистика:</b>\n
Отозвано: {0}%
Истекло: {1}%
Валидно: {2}%
Среднее за период: {6}\n
<b>За всё время:</b>\n
{3}
<b>За период в {4}:</b>\n
{5}
""",
        "kpi_chunk": """\tВсего: {0}
\tВалидно: {1}
\tАктивно: {2}
\tИстекли: {3}
\tОтозваны: {4}
""",
        "subscription_created": """
✅ Ключ <code>{0}</code> выдан!
🗓 Валиден до: {1}
💉 Полезная нагрузка: {2}
""",
        "subscription_revoked": """
⏸ Ключ <code>{0}</code> отозван!
💉 Полезная нагрузка: {1}
""",
    },
    "EN": {
        "not_admin": "<b>Sorry, you are not an admin!</b>",
        "welcome": "Welcome to the <b>Subscriby</b>, <i>{0}</i>!",
        "enter_days_for_kpi": "Please enter days for KPI period (>1)",
        "enter_days_for_publish": "Please enter days for subscription (<i>how long it will work</i>)",
        "api_error": "Unable to call API!",
        "invalid_number": "Invalid number!",
        "kpi_period_header": "<b><i>[{0}]: </i></b>\n",
        "btn_create": "🛒 Create new",
        "btn_revoke": "🔸 Revoke old",
        "btn_kpi": "📈 KPI analytics",
        "enter_key_to_revoke": "Enter key which you wish to revoke",
        "kpi_base": """
📈 <b><u>KPI analytics</u></b>:\n
<b>Statistics:</b>\n
Revoked: {0}%
Expired: {1}%
Valid: {2}%\n
Mean for period: {6}\n
<b>For all:</b>\n
{3}
<b>For {4} days:</b>\n
{5}
""",
        "kpi_chunk": """\tAll: {0}
\tValid: {1}
\tActive: {2}
\tExpired: {3}
\tRevoked: {4}
""",
        "subscription_created": """
✅ Key <code>{0}</code> created!
🗓 Valid until: {1}
💉 Injected payload: {2}
""",
        "subscription_revoked": """
⏸ Key <code>{0}</code> revoked!
💉 Injected payload: {1}
""",
    },
}

T = LANGUAGES[Settings().subscriby_telegram_language]
