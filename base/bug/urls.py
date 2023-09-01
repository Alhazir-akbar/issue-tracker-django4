from django.urls import path
from .views import create_ticket,  dispotition_ticket, edit_ticket, forward_ticket, status_diteruskan, status_kembalikan, status_proses, status_selesai,view_ticket_detail,  view_ticket_list

urlpatterns = [
    path('create_ticket/', create_ticket, name='create_ticket'),
    path('edit_ticket/<int:ticket_id>/', edit_ticket, name='edit_ticket'),
    
    
    #path('edit_ticket/<int:ticket_id>/', edit_ticket, name='edit_ticket'),
    #path('forward_ticket/<int:ticket_id>/', forward_ticket, name='forward_ticket'),
    
    path('forward_ticket/', forward_ticket, name='forward_ticket'),
    path('dispotition_ticket/', dispotition_ticket, name='dispotition_ticket'),
    
    
    path('view_tickets/', view_ticket_list, name='view_ticket_list'),
    path('view_ticket/<int:ticket_id>/', view_ticket_detail, name='view_ticket_detail'),
    

    path('tiket/proses/', status_proses, name='status_proses'),
    path('tiket/diteruskan/', status_diteruskan, name='status_diteruskan'),
    path('tiket/selesai/', status_selesai, name='status_selesai'),
    path('tiket/kembalikan/', status_kembalikan, name='status_kembalikan'),
    

]
