from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView

from book.forms import RegisterForm, LoginForm, BookshelfForm, UserUpdateForm, UserDeleteForm
from book.models import Users, Book, Bookshelf


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        context = {
            "form": form
        }
        return render(request, "auth/register.html", context=context)

    def post(self, request):
        form = RegisterForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save()
            Bookshelf.objects.create(owner=user, name="Read")
            Bookshelf.objects.create(owner=user, name="Currently Reading")
            Bookshelf.objects.create(owner=user, name="Want To Read")
            return redirect("book:login")
        else:
            context = {
                "form": form
            }
            return render(request, "auth/register.html", context=context)


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        context = {
            "form": form
        }
        return render(request, "auth/login.html", context=context)

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                user.login_try_count =0
                user.save()
                messages.success(request, f"You are now logged in as {user.username}.")
                return redirect("home")
            else:
                try:
                    user = Users.objects.get(username=form.cleaned_data["username"])
                    user.login_try_count += 1
                    user.save()
                except Users.DoesNotExist:
                    pass
                messages.warning(request, "Invalid username or password.")
                return redirect("book:login")




class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "You are now logged out.")
        return redirect("home")



class UserDeleteView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserDeleteForm()
        return render(request, 'user/user_delete.html', {'form': form})

    def post(self, request):
        form = UserDeleteForm(request.POST)
        if form.is_valid():
            choice = form.cleaned_data.get('delete')
            if choice == 'Yes':
                user = request.user
                user.delete()
                return redirect(reverse_lazy('home'))
            else:
                return redirect(reverse_lazy('home'))
        return render(request, 'user/user_delete.html', {'form': form})

class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            "user": request.user
        }
        return render(request, "user/profile.html", context=context)


class UserUpdateProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = get_object_or_404(Users, username=request.user.username)
        form = UserUpdateForm(instance=user)
        context = {
            "form": form
        }
        return render(request, "user/user-profile-update.html", context=context)

    def post(self, request):
        form = UserUpdateForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "User profile successfuly updated")
            return redirect("book:profile")
        else:
            context = {
                "form": form
            }
            return render(request, "user/user-profile-update.html", context=context)


class MyBookView(View, LoginRequiredMixin):
    def get(self, request):
        shelves = Bookshelf.objects.filter(owner=request.user)
        context = {
            "shelves": shelves
        }
        return render(request, "book/my_book.html", context=context)


class BookshelfCreateView(CreateView, LoginRequiredMixin):
    queryset = Bookshelf.objects.all()
    template_name = "book/new-bookshelf.html"
    form_class = BookshelfForm
    success_url = reverse_lazy("book:my-book")
