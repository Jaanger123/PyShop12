from django.core.mail import send_mail


def send_welcome_email(email):
	url = 'http://localhost:8000/'
	message = f'Thank you for registering in our site: {url}'
	send_mail(
		'PyShop12 Welcome!!!',
		message,
		'pyshopadmin@gmail.com',
		[email],
		fail_silently=False
	)
