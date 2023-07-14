
from django.shortcuts import render, redirect , get_object_or_404
from .models import Product , Picture 
from .models import Seller_info
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

@login_required
def add_product(request):
    customer = request.user.customer
    if not Seller_info.verified:
        return HttpResponseForbidden("Access Denied. Please verify your account.")

    if request.method == 'POST':
        product_name = request.POST['product_name']
        product_description = request.POST['product_description']
        product_price = request.POST['product_price']
        pictures = request.FILES.getlist('pictures')

        # Create the product
        product = Product.objects.create(
            customer=request.user,
            product_name=product_name,
            product_description=product_description,
            product_price=product_price
        )

        # Create Picture instances and associate them with the product
        for picture in pictures:
            picture_instance = Picture.objects.create(product=product, image=picture)

        return redirect('home1')  # Replace 'home1' with the URL name of your home1 view

    return render(request, 'product_add.html')





@login_required
def become_seller(request):
    seller_info, created = Seller_info.objects.get_or_create(customer=request.user)

    if request.method == 'POST':
        official_name = request.POST['official_name']
        second_name = request.POST['second_name']
        documents = request.FILES['documents']
        description = request.POST['description']

        # Update Seller_info instance
        seller_info.first_name = official_name
        seller_info.second_name = second_name
        seller_info.documents = documents
        seller_info.description = description

        # Save the updated Seller_info instance
        seller_info.save()

        # Process the form data as needed (e.g., send email notifications, etc.)

        return redirect('home1')  # Replace 'home1' with the URL name of your home1 view

    return render(request, 'become_seller.html')






def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    pictures = Picture.objects.all()
    context = {
        'product': product , 
        'pictures' : pictures
    }
    return render(request, 'product_detail.html', context)










