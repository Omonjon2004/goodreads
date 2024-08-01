from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

from book.models import Users, BlockedUsers

class LoginAttemptMiddleware(MiddlewareMixin):
    def __call__(self, request):

        blocked_users = Users.objects.filter(login_try_count__gte=3)

        for user in blocked_users:
            BlockedUsers.objects.get_or_create(username=user.username)


        blocked_usernames = BlockedUsers.objects.values_list("username", flat=True)


        if request.user.is_authenticated and request.user.username in blocked_usernames:
            return HttpResponse("""
                <h3>Your account has been blocked due to suspicious activity. Please contact the admin.</h3>
                <h4><a href='https://t.me/@omonjon_3007' style='text-decoration: none;'>Admin support</a></h4>
            """, content_type="text/html")

        response = self.get_response(request)
        return response

