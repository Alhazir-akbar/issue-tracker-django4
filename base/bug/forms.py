from django import forms
from .models import Ticket, Comment, Attachment, User
from django.contrib.auth.models import Group

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority']
       

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']
        
        
class EditTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority', 'status']

class ForwardTicketForm(forms.Form):
    ticket = forms.ModelChoiceField(
        queryset=Ticket.objects.filter(status='Proses'),  # Hanya tiket dengan status "Proses" yang bisa diteruskan
        label='Pilih Tiket yang Akan Diteruskan',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    developer = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='Developer'),  # Menampilkan pengguna dengan peran Developer
        label='Pilih Pengembang',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
class DispopotionTicketForm(forms.Form):
    ticket = forms.ModelChoiceField(
        queryset=Ticket.objects.filter(status='Diteruskan ke Pengembang'),  
        label='Pilih Tiket yang Akan asdas',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    support = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='Support'),  
        label='Pilih Support',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority', 'status']
        
        
