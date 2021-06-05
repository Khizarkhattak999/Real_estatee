from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contacts

# Create your views here.
def contacts(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

    #Checking if already user has made an inquiry
    if request.user.is_authenticated:
        user_id = request.user.id
        has_contacted = Contacts.objects.all().filter(listing_id=listing_id,user_id=user_id)
        if has_contacted:
            messages.error(request,'you have already made an inquiry')
            return redirect('/listings/'+listing_id)


    contacts = Contacts(listing_id=listing_id,listing=listing,name=name,email=email,phone=phone,message=message,user_id=user_id)

    contacts.save()
    # send mail
    send_mail(
        'Property Listing Inquiry',
        'There has been inquiry' + listing +'Sign in to admin panel to check the inquiry',
        'khizarkhattak848@gmail.com',
        [realtor_email,'khizarkhattak999@gmail.com'],
        fail_silently=False
    )

    
    messages.success(request,'You request has been submitted,Realtor will get back to you soon..')

    return redirect('/listings/' + listing_id)

