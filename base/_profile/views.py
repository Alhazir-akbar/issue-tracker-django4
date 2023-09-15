from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.shortcuts import render, redirect

from .models import UserProfile  
from .forms import CustomUserCreationForm

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
    template_name = 'dashboard/dashboard.html'
 
    return render(request, template_name, {'role':role})






