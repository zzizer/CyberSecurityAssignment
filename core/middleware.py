   from django.contrib.auth import get_user_model
   from django.utils import timezone

   User = get_user_model()

   class FailedLoginMiddleware:
       def __init__(self, get_response):
           self.get_response = get_response

       def __call__(self, request):
           if request.method == 'POST' and 'login' in request.path:
               email = request.POST['email']
               password = request.POST['password']
               user = User.objects.filter(email=email).first()
               if user and user.failed_login_attempts >= 3:
                   user.is_active = False
                   user.is_verified = False
                   user.save()
                   return render(request, 'account_locked.html')
               elif user and user.failed_login_attempts < 3:
                   user.failed_login_attempts += 1
                   user.save()
           response = self.get_response(request)
           return response