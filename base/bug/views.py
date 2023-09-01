from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket, Attachment, Comment
from .forms import DispopotionTicketForm, EditTicketForm, ForwardTicketForm, TicketForm, CommentForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.mail import send_mail
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
            
            # for file in request.FILES.getlist('attachment'):
            #     Attachment.objects.create(id_ticket=ticket, file=file)
            return redirect('dashboard')  
    else:
        ticket_form = TicketForm()
    return render(request, 'dashboard/create_ticket.html', {'ticket_form': ticket_form})




def edit_ticket(request, ticket_id):
    # Dapatkan tiket yang akan diedit berdasarkan ID atau segera kembalikan 404 jika tidak ditemukan
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    if request.method == 'POST':
        # Dalam metode POST, periksa apakah formulir yang dikirimkan adalah valid
        ticket_form = EditTicketForm(request.POST, request.FILES, instance=ticket)
        if ticket_form.is_valid():
            # Simpan perubahan ke tiket
            ticket = ticket_form.save(commit=False)
            ticket.reporting_user = request.user
            ticket.status = "Proses"  
            support_group = Group.objects.get(name='Support')
            support_users = support_group.user_set.all()
            if support_users.exists():
                support_user = support_users.first()
                ticket.support_user = support_user  
            ticket.save()
            
            # Redirect ke halaman dashboard atau halaman tiket yang telah diedit
            return redirect('dashboard')
    else:
        # Jika metode bukan POST, tampilkan formulir dengan data tiket yang ada
        ticket_form = EditTicketForm(instance=ticket)
    
    return render(request, 'dashboard/edit_ticket.html', {'ticket_form': ticket_form, 'ticket': ticket})

def view_ticket_list(request):
    # Ambil daftar tiket yang ingin ditampilkan
    tickets = Ticket.objects.all()  # Ubah query sesuai kebutuhan Anda
    return render(request, 'dashboard/view_ticket.html', {'tickets': tickets})

def view_ticket_detail(request, ticket_id, *args):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    user_profile = request.user.userprofile
    
    link = "dispotition_ticket"    
    linkked = "forward_ticket"    
    
    role = user_profile.role
    if role == 'reporting':
        title = "Halaman reporting"
    elif role == 'support':
        title = "Halaman support"
        linkked = reverse('forward_ticket')
    elif role == 'developer':
        title = "Halaman developer"
        link = reverse('dispotition_ticket')
    return render(request, 'status/view_ticket_detail.html', {'ticket': ticket, 'title':title, 'link': link, 'linkked': linkked})

#Detail #duplikan chek dengan yang diatas
#Kembalikan
def status_kembalikan(request):
    tiket_kembalikan = Ticket.objects.filter(status='Kembalikan ke Support')
    return render(request, 'status/tiket_kembalikan.html', {'tiket_kembalikan': tiket_kembalikan})

#Diteruskan
def status_diteruskan(request):
    tiket_diteruskan = Ticket.objects.filter(status='Diteruskan ke Pengembang')
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
            
            # Menyimpan pengembang yang akan menangani tiket
            selected_ticket.developer = selected_developer
            selected_ticket.status = "Diteruskan ke Pengembang"
            selected_ticket.save()
            
            # Mengirim notifikasi atau email ke pengembang
            subject = f"Ticket #{selected_ticket.id} telah diteruskan kepada Anda"
            message = f"Sebuah tiket dengan judul '{selected_ticket.title}' telah diteruskan kepada Anda."
            from_email = "admin@example.com"  # Ganti dengan alamat email yang sesuai
            recipient_list = [selected_developer.email]  # Menggunakan email pengembang yang dipilih
            
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)
            
            return redirect('dashboard')
    else:
        form = ForwardTicketForm()
    
    return render(request, 'dashboard/forward_ticket.html', {'form': form})

 



def dispotition_ticket(request):
    if request.method == 'POST':
        form = DispopotionTicketForm(request.POST)
        
        if form.is_valid():
            selected_ticket = form.cleaned_data['ticket']
            selected_support = form.cleaned_data['support']
            
            # Menyimpan pengembang yang akan menangani tiket
            selected_ticket.support = selected_support
            selected_ticket.status = "Kembalikan Ke Support"
            selected_ticket.save()
            
            # Mengirim notifikasi atau email ke pengembang
            subject = f"Ticket #{selected_ticket.id} telah diteruskan kepada Anda"
            message = f"Sebuah tiket dengan judul '{selected_ticket.title}' telah diteruskan kepada Anda."
            from_email = "admin@example.com"  # Ganti dengan alamat email yang sesuai
            recipient_list = [selected_support.email]  # Menggunakan email pengembang yang dipilih
            
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)
            
            return redirect('dashboard')
    else:
        form = DispopotionTicketForm()
    return render(request, 'dashboard/dispotition_ticket.html', {'form': form})
# def dispotition_ticket(request):
#     if request.method == 'POST':
#         form = DispopotionTicketForm(request.POST)
#         if form.is_valid():
#             selected_ticket = form.cleaned_data['ticket']
#             selected_support = form.cleaned_data['support']
            
#             # Menyimpan pengembang yang akan menangani tiket
#             selected_ticket.support = selected_support
#             selected_ticket.status = "Kembalikan Ke Support"
#             selected_ticket.save()
            
#             # Mengirim notifikasi atau email ke pengembang
#             subject = f"Ticket #{selected_ticket.id} telah diteruskan kepada Anda"
#             message = f"Sebuah tiket dengan judul '{selected_ticket.title}' telah diteruskan kepada Anda."
#             from_email = "admin@example.com"  # Ganti dengan alamat email yang sesuai
#             recipient_list = [selected_support.email]  # Menggunakan email pengembang yang dipilih
            
#             send_mail(subject, message, from_email, recipient_list, fail_silently=True)
            
#             return redirect('dashboard')
#     else:
#         form = DispopotionTicketForm()
#     return render(request, 'dashboard/dispotition_ticket.html', {'form': form})

#MARI KITA COBA


