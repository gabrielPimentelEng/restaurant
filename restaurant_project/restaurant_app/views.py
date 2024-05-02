from django.shortcuts import render,redirect
from .models import MenuItem,Booking
# Create your views here.


def home_view(request):
    return render(request,'home.html')

def about_view(request):
    return render(request,'about.html')

def menu_view(request):
    menu_data = MenuItem.objects.all().order_by('name')
    main_data = {"menu": menu_data}
    return render(request,'menu.html',main_data)

def book_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        guest_number = request.POST.get('guest_number')
        comment = request.POST.get('comment')

        # Create Booking instance and save it to the database
        booking = Booking(
            first_name=first_name,
            last_name=last_name,
            guest_number=guest_number,
            comment=comment
        )
        booking.save()
        return redirect('book_submit')
    return render(request,'book.html')

def booking_confirmation(request):
    return render(request, 'booking_confirmation.html')


def item_detail(request,pk):
    if pk:   
        item = MenuItem.objects.get(pk=pk)    
    else:
        item = ""
    item_dict = {"item":item}
    return render(request,"menu_item.html",item_dict)

