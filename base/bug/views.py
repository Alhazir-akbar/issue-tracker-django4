from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket, Attachment, Comment
from .forms import DispopotionTicketForm, EditTicketForm, ForwardTicketForm, KirimTiketDeveloper, SolvedTicketForm, TicketForm, CommentForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages

@login_required
def create_ticket(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.reporting_user = request.user
            ticket.status = "Proses"  
            support_group = Group.objects.get(name='Support')
            support_users = support_group.user_set.all()
            if support_users.exists():
                support_user = support_users.first()
                ticket.support_user = support_user  
            ticket.save()
            
            for file in request.FILES.getlist('attachment'):
                Attachment.objects.create(id_ticket=ticket, file=file)
            return redirect('view_ticket_list')  
    else:
        ticket_form = TicketForm()
    return render(request, 'dashboard/create_ticket.html', {'ticket_form': ticket_form})

def view_ticket_list(request):
    tickets = Ticket.objects.all() 
    return render(request, 'dashboard/view_ticket.html', {'tickets': tickets})

def view_ticket_detail(request, ticket_id, *args):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    user_profile = request.user.userprofile
    dispotition_ticket = "dispotition_ticket"    
    forward_ticket = "forward_ticket"    
    role = user_profile.role
    if role == 'reporting':
        title = "Halaman reporting"
    elif role == 'support':
        title = "Halaman support"
    elif role == 'developer':
        title = "Halaman developer"
    return render(request, 'status/view_ticket_detail.html', {'ticket': ticket, 'title':title, 'dispotition_ticket': dispotition_ticket, 'forward_ticket': forward_ticket})

def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        ticket_form = EditTicketForm(request.POST, request.FILES, instance=ticket)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.reporting_user = request.user
            ticket.status = "Proses"  
            support_group = Group.objects.get(name='Support')
            support_users = support_group.user_set.all()
            if support_users.exists():
                support_user = support_users.first()
                ticket.support_user = support_user  
            ticket.save()
            return redirect('view_ticket_list')
    else:
        ticket_form = EditTicketForm(instance=ticket)
    return render(request, 'dashboard/edit_ticket.html', {'ticket_form': ticket_form, 'ticket': ticket})

#Dikembalikan
def status_kembalikan(request):
    tiket_kembalikan = Ticket.objects.filter(status='ToSupport')
    return render(request, 'status/tiket_kembalikan.html', {'tiket_kembalikan': tiket_kembalikan})

#Diteruskan
def status_diteruskan(request):
    tiket_diteruskan = Ticket.objects.filter(status='ToDeveloper')
    return render(request, 'status/tiket_diteruskan.html', {'tiket_diteruskan': tiket_diteruskan})

#Diproses
def status_proses(request):
    tiket_proses = Ticket.objects.filter(status='Proses')
    return render(request, 'status/tiket_proses.html', {'tiket_proses': tiket_proses})

#Selsai
def status_selesai(request):
    tiket_selesai = Ticket.objects.filter(status='Selesai')
    return render(request, 'status/tiket_selesai.html', {'tiket_selesai': tiket_selesai})

def forward_ticket(request):
    if request.method == 'POST':
        form = ForwardTicketForm(request.POST)
        if form.is_valid():
            selected_ticket = form.cleaned_data['ticket']
            selected_developer = form.cleaned_data['developer']
            selected_ticket.developer = selected_developer
            selected_ticket.status = "ToDeveloper"
            selected_ticket.save()
     
            return redirect('dashboard')
    else:
        form = ForwardTicketForm()
    return render(request, 'dashboard/forward_ticket.html', {'form': form})

def solved_ticket(request):
    if request.method == 'POST':
        form = SolvedTicketForm(request.POST)
        if form.is_valid():
            selected_ticket = form.cleaned_data['ticket']
            selected_ticket.status = "Selsai"
            selected_ticket.save()
            return redirect('solved_ticket')
    else:
        form = SolvedTicketForm()
    return render(request, 'flow/solved_ticket.html', {'form': form})

def dispotition_ticket(request):
    if request.method == 'POST':
        form = DispopotionTicketForm(request.POST)
        if form.is_valid():
            selected_ticket = form.cleaned_data['ticket']
            selected_support = form.cleaned_data['support']
            selected_ticket.support = selected_support
            selected_ticket.status = "ToSupport"
            selected_ticket.save()
            return redirect('dashboard')
    else:
        form = DispopotionTicketForm()
    return render(request, 'dashboard/dispotition_ticket.html', {'form': form})




@login_required
def selsaikan_tiket(request, ticket_id):
    try:
        selected_ticket = Ticket.objects.get(id=ticket_id)
        selected_ticket.status = 'Selsai'
        selected_ticket.save()
        messages.success(request, 'Tiket berhasil dikirim ulang.')
    except Ticket.DoesNotExist:
        messages.error(request, 'Tiket dengan ID tersebut tidak ditemukan.')
    
    return redirect('status_kembalikan')  # Ganti 'status_kembalikan' dengan nama URL halaman tiket yang dikembalikan.

@login_required
def kirim_ulang_tiket(request, ticket_id):
    try:
        selected_ticket = Ticket.objects.get(id=ticket_id)
        selected_ticket.status = 'ToDeveloper'
        selected_ticket.save()
        messages.success(request, 'Tiket berhasil dikirim ulang.')
    except Ticket.DoesNotExist:
        messages.error(request, 'Tiket dengan ID tersebut tidak ditemukan.')
    
    return redirect('status_kembalikan')  # Ganti 'status_kembalikan' dengan nama URL halaman tiket yang dikembalikan.

def kirim_tiket_developer(request, ticket_id):
    if request.method == 'POST':
        form = KirimTiketDeveloper(request.POST)
        if form.is_valid():
            try:
                selected_ticket = Ticket.objects.get(id=ticket_id)
                selected_ticket.status = 'ToDeveloper'
                selected_developer = form.cleaned_data['developer']
                selected_ticket.developer = selected_developer
                selected_ticket.save()
                messages.success(request, 'Tiket berhasil dikirim ulang.')
            except Ticket.DoesNotExist:
                messages.error(request, 'Tiket dengan ID tersebut tidak ditemukan.')
            return redirect('status_kembalikan')
    else:
        form = KirimTiketDeveloper()
        return render(request, 'flow/forward_ticket.html', {'form': form})


# def kirim_tiket_developer(request, ticket_id):
#     if request.method == 'POST':
#         form = ForwardTicketForm(request.POST)
#         if form.is_valid():
#             selected_ticket = Ticket.objects.get(id=ticket_id)
#             selected_ticket.status = "Developer"
#             selected_developer = form.cleaned_data['developer']
#             selected_ticket.developer = selected_developer
#             selected_ticket.save()
     
#             return redirect('dashboard')
#     else:
#         form = ForwardTicketForm()
#     return render(request, 'flow/forward_ticket.html', {'form': form})