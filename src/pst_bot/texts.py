# TODO: Use json or etc. =)
# TODO: i18n! By middleware =)

# #Тексты команд
# Текст при команде /start
# °_°
cmd_start_text = '\n/help - Помощь\n'
cmd_start_hi_text = 'Привет, %s!'

# Текст при команде /help
cmd_help_text = (
	'\n'
	'Список команд:'
	'\n'
	'/start - Начать диалог'
	'\n'
	'/help - Получить справку'
	'\n'
	'/report [текст] - Репорт админу'
	'\n'
	'\n'
	'...'
	'\n'
)

# Текст при команде /report
rate_wait = 'Следующий репорт можно отправить через 1 час'
cmd_report_success_text = (
	'Репорт отправлен!'
	'\n'
	+
	rate_wait
) # user
cmd_report_mintxt_text = (
	'мин. 16 символов'
	'\n'
	+
	rate_wait
) # user

# #Кнопки
...
btn_text_back = 'Назад'

# Тексты кнопок
select_resolution_text = 'Выберите разрешение:'
unknown_video_service_text = (
	'Пока у нас нет возможности загружать от сюда'
	'\n'
	'/help - Для просмотра списка сайтов и формата ссылок'
)
cancelled_text = 'Отменено!'
text_undo = 'Отменить'

# #Текст обратной связи
feedback_text = 'Пока здесь нет текста :D'


# #Часть админа
startup_notify_admins_text = 'Oh sh*t, here we go again..'
shutdown_notify_admins_text = 'П*зда!'
user_report_notify_admins_text = 'Новый репорт!'

throttled_msg_text = 'Завали тыкалку!'
