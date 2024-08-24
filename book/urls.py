from django.urls import path

from book.views import RegisterView, LoginView, MyBookView, BookshelfCreateView, LogoutView, UserProfileView, \
    UserUpdateProfileView, BookListView, BookDetailView

app_name = "book"
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("edit-profile/", UserUpdateProfileView.as_view(), name="update-profile"),
    path("my_book/", MyBookView.as_view(), name="my-book"),
    path("books/", BookListView.as_view(), name="book-list"),
    path("book/<id>/", BookDetailView.as_view(), name="book-detail"),
    path("new-bookshelf/", BookshelfCreateView.as_view(), name="new-bookshelf"),
]
