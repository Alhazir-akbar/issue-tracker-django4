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
        fields = ['title', 'description', 'priority']

class ForwardTicketForm(forms.Form):
    ticket = forms.ModelChoiceField(
        queryset=Ticket.objects.filter(status='Proses'),  
        label='Pilih Tiket yang Akan Diteruskan Status Saat Ini Proses',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    developer = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='Developer'),  
        label='Pilih Developer',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
class KirimTiketDeveloper(forms.Form):
    developer = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='Developer'),  
        label='Pilih Developer',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

# class ResendTicketForm(forms.Form):
#     ticket = forms.ModelChoiceField(
#         queryset=Ticket.objects.filter(status='ToSupport'),  
#         label='Pilih Tiket yang Akan Dikirim Kembali ke Developer',
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )


    
class DispopotionTicketForm(forms.Form):
    ticket = forms.ModelChoiceField(
        queryset=Ticket.objects.filter(status='ToDeveloper'),  
        label='Pilih Tiket yang Akan Diteruskan Status Saat Ini ToDeveloper ',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    support = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='Support'),  
        label='Pilih Support',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class SolvedTicketForm(forms.Form):
    ticket = forms.ModelChoiceField(
        queryset=Ticket.objects.filter(status='ToDeveloper'),  
        label='Pilih Tiket yang Akan Diteruskan Status Saat Ini ToDeveloper',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

        
