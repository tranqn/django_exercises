from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect


def login_with_remember_me(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            # Remember me: extend session, otherwise expire on browser close
            if not request.POST.get("remember_me"):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(60 * 60 * 24 * 30)  # 30 days

            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})