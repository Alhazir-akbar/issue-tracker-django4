from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from bug.models import Ticket
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile  # Import model UserProfile di sini

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register/Registrasi.html'

    def form_valid(self, form):
        user = form.save()
        user_profile = UserProfile.objects.create(user=user, role=form.cleaned_data['role'])
        login(self.request, user)
        return redirect('login')


@login_required
def dashboard(request):
    user_profile = request.user.userprofile
    role = user_profile.role
    if role == 'reporting':
        template_name = 'dashboard/dashboard_reporting.html'
    elif role == 'support':
        template_name = 'dashboard/dashboard_support.html'
    elif role == 'developer':
        template_name = 'dashboard/dashboard_developer.html'
    return render(request, template_name)






