
from django.shortcuts import render  , redirect
from django.http import HttpResponse 
from django.template import loader
from .models import Items,ItemDetails, Cart
from .forms import CreateUserForm ,LoginUserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

def indexcomputer(request):
 template=loader.get_template('indexcomputer.html') 
 return HttpResponse(template.render())

def hometools(request):
 template=loader.get_template('hometools.html') 
 computer=ItemDetails.objects.select_related('itemsid')

 print(computer.query)
 return HttpResponse(template.render({'computer':computer}))

def detailsorder(request ,id):
 template=loader.get_template('detailsorder.html') 
 computer=ItemDetails.objects.select_related('itemsid').filter(itemsid=id)
 print(computer.query)
 context={
  'computer':computer 
 }
 return HttpResponse(template.render(context))


@csrf_exempt
def auth_register(request):
 template=loader.get_template('auth_register.html') 
 form=CreateUserForm()
 if request.method=='POST':
      form=CreateUserForm(request.POST)
      if form.is_valid():
           form.save()
           return redirect('auth_login')
 context={'registerform':form}
 return HttpResponse(template.render(context=context))
@csrf_exempt
def auth_login(request):
  template=loader.get_template('auth_login.html') 
  form=LoginUserForm()
  if request.method=='POST':
      form=LoginUserForm(data=request.POST)
      if form.is_valid():
           username=form.cleaned_data('username')
           password=form.cleaned_data('password')

           user=authenticate(username=username,password=password)
           if user:
              if user.is_active:
                 login(request,user)
                 return render(request,'indexcomputer.html')
  context={'form':form} 
  return render(request,'auth_login.html',context)

@login_required( login_url='/auth_login/')
def auth_logout(request):
     if request.method=="POST" :
          logout(request)
          return redirect("/")


@login_required(login_url='/auth_login/')
def checkoutco(request):
       template=loader.get_template('checkoutco.html')
       current_user = request.user.id
       cart=Cart.objects.all().filter(Id_user=current_user).first()
       product=Items.objects.all().filter(id=cart.Id_product).first()
       context={
            'cart':cart,
            'productname':product,
             'request':request
            
       }
       return HttpResponse(template.render(context=context)) 

@login_required(login_url='/auth_login/')
@csrf_exempt
def add_to_cart_to_computer(requset,product_id):
     currentuser=requset.user
     discount=2
     state=False
     computer=ItemDetails.objects.select_related('itemsid').filter(itemsid=product_id)
    
     for item in computer:
           net=item.total-discount
          
           cart = Cart(
             Id_product=item.itemsid.id,
             Id_user=currentuser.id,
             price=item.price,
             qty=item.qty,
             tax=item.tax,
             total=item.total,
             discount=discount,
             net=net,
             status=state
          )
     
     currentuser=requset.user.id
     count=Cart.objects.filter(Id_user=currentuser).count()
     print(count)
     cart.save()
     requset.session['countcart']=count
     return redirect("/hometools")


def statement(request):
    invoice_number = "INV-001"
    invoice_date = "2024-03-10"
    items = [
        {"name": "Item 1", "quantity": 2, "price": 10},
        {"name": "Item 2", "quantity": 1, "price": 20},
        # Add more items as needed
    ]
    total_amount = sum(item["quantity"] * item["price"] for item in items)

    context = {
        'invoice_number': invoice_number,
        'invoice_date': invoice_date,
        'items': items,
        'total_amount': total_amount
    }

    return render(request, 'statement.html', context)



     
