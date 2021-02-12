# Create your views here.
from django.views.generic import View, TemplateView, CreateView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, auth
from django.http import HttpResponse,JsonResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import logout
from django.contrib import messages
from django.db.models import Q
from ecomm.models import *
from time import time
from math import ceil
from .forms import *
import requests
import razorpay


# Social AUthentication...........................
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "index.html" 


# from django.http import JsonResponse
client = razorpay.Client(auth=("rzp_test_eXX8kZH8wT794y", "F9gyCXHiX8am8GTpjYjRN651"))
# Login requier=====================================================

class EcomRequir(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id=request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id = cart_id)
            if request.user.is_authenticated :
                cart_obj.customer = request.user
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)
    


# ==================================================================

def home(request):
    # response = requests.get('http://rrasmi070.pythonanywhere.com/product/web_api/').json()
    # print(response)
    prdt = Product.objects.all()
    # page = Paginator(prdt,4) # Show 4 contacts per page.

    # page_obj = paginator.get_page(page_number)
    cate=Category.objects.all()
    
    # count=0
    # f=0
    catego_id=request.GET.get("category")
    print(catego_id)
    if catego_id:
        prdt=Product.objects.filter(category_id=catego_id)
        
    
    # # print(v)
    # for d in response:
    #     id=response[f]['id']
    #     # print(id)
    #     Product_name=response[f]['Product_name']
    #     category=response[f]['category']
    #     # .replace(" ", "_")
    #     # print(category)
    #     Price=response[f]['Price']
    #     brand=response[f]['brand']
    #     Description=response[f]['Description']
    #     image=response[f]['image']
        
    #     pro = Product.objects.filter(id=id)
    #     # print(pro)
    #     if id != pro:
    #         w=Category.objects.get(category_name=category)
    #         Product(id=id,Product_name=Product_name,Price=Price,category=w,brand=brand,Description=Description,image=image).save()
    #         # print("saved")
    #     # if f==1:
    #     #     break
    #     f+=1

    
    # for i in response:
    #     cn=response[count]['category']
    #     # print(cn)
    #     if cate.count() == 0 :
    #         Category(category_name=cn).save()
            
    #     else:
    #         h=Category.objects.filter(category_name=cn)
    #         # print(h.count())
    #         if h.count()==0:
    #             Category(category_name=cn).save()
    #             # print('hiii')
    #         # else:
    #         #     print('sorry')
    #     count=count+1
    

    params = {'response':prdt,'cate':cate}
    
    return render(request, 'index.html', params)
# ================================================================

def filter(request):
    prdt = Product.objects.all()
    cate=Category.objects.all()
    catego_id=request.GET.get("category")
    print(catego_id)
    if catego_id:
        prdt=Product.objects.filter(category_id=catego_id).order_by("Price")
        print(prdt)
    params = {'response':prdt,'cate':cate}
    return render(request, 'cat_view.html', params)
    # render(request, 'cat_view.html')

# ================================================================
def cart(request):
    data2=Products.objects.all()
    print(data2)
    data = {'data3' : data2}
    return render(request, 'cart.html', data)

def signup(request):
    if request.method == "POST":
        first_name = request.POST['f_name']
        last_name = request.POST['l_name']
        username = request.POST['email']
        email = request.POST['email']
        psw1 = request.POST['psw']
        psw2 = request.POST['psw_repeat']
        if psw1 == psw2:
            User.objects.create_user(username=username, password=psw2, first_name=first_name, last_name=last_name, email=email).save()
    return render(request, 'index.html')

def login(request):
    if request.method == "POST":
        username = request.POST['user']
        psw = request.POST['password']

        user = auth.authenticate(username=username, password=psw)
        if user is not None:
            auth.login(request, user)
            return redirect('mycart')
        # else:
        #     messages.info(request, "Invalid credentials..!!!!!")


    return render(request, 'index.html')

def lgout(request):
    logout(request)
    print("Logout Success")
    return redirect('/')


class ProductDetailView(EcomRequir,TemplateView):
    template_name = "p_detail.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs["id"]
        product = Product.objects.get(id=id)
        context['product'] = product
        return context


class AddToCartView(EcomRequir,TemplateView):
    template_name = "cart_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs["id"]
        product = Product.objects.get(id=id)
        cart_id = self.request.session.get("cart_id", None)
        
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_cart = cart_obj.cartproduct_set.filter(product=product)
            
            # Items already exist in cart
            if this_product_cart.exists():
                cartproduct = this_product_cart.last()
                cartproduct.quantity +=1
                cartproduct.subtotal += product.Price
                cartproduct.save()
                cart_obj.total += product.Price
                cart_obj.save()
            # New items added in cart
            else:
                cartproduct = Cartproduct.objects.create(cart=cart_obj, product=product, rate=product.Price, quantity=1 , subtotal=product.Price)
                cart_obj.total += product.Price
                cart_obj.save()
        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = Cartproduct.objects.create(cart=cart_obj, product=product, rate=product.Price, quantity=1 , subtotal=product.Price)
            cart_obj.total += product.Price
            cart_obj.save()
            print("new project")

        return context



class MyCart(EcomRequir,TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context["cart"] = cart
        return context


class ManageCart(EcomRequir,TemplateView):
    def get(self, request, *args, **kwargs):
        id = self.kwargs["id"]
        action = request.GET.get("action")
        cp_obj = Cartproduct.objects.get(id=id)
        cart_obj = cp_obj.cart
        # cart_id = self.request.session.get("cart_id", None)
        # if cart_id:
        #     cart2 = Cart.objects.get(id=cart_id)
        #     if cart1 != cart2:
        #         return redirect("mycart")
        #     else:

        if action == "incr":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action == "decr":
            cp_obj.quantity -=1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()
                return redirect("mycart")
        elif action == "del":
            cart_obj.total -=cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("mycart")


class EmptyCart(EcomRequir,TemplateView):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            # OR
            # cart.cartproduct_set.delete()
        return redirect("mycart")



class OrderNow(CreateView):
    template_name = "order_now.html"
    form_class = OrderForm
    success_url = reverse_lazy("home_page")

    def dispatch(self, request, *args, **kwargs):
        
        if request.user.is_authenticated:
            print("user is  Logedin")
        else:
            return redirect("mycart")
        return super().dispatch(request, *args,**kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    # order form
    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        # client = razorpay.Client(auth=(key_id, key_secret))
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = "Order received"
            del self.request.session['cart_id']
            pm = form.cleaned_data.get("payment_method")
            order = form.save()
            if pm == "Make Payment":
                print('Order Created')
                return redirect(reverse("handlepayment")+"?ord_id=" + str(order.id))
        else:
            return redirect("home_page")
        
        return super().form_valid(form)



# PYMENT GATEWAY=================================================
# @csrf_exempt
class HandelRequestView(View):
    # template_name="success.html"
    def get(self, request, *args, **kwargs):
        ord_id = request.GET.get("ord_id")
        ord_pay = Order.objects.get(id=ord_id)
        print(ord_pay)
        amount = (ord_pay.total)*100
        currency = "INR"
        # receipt =
        # notes = {
        #     "email" : User.email,
        #     "name" : f'{User.first_name} {User.last_name}'
        # }
        reciept = f"youneed-{int(time())}"
        # print(reciept)
        # print(amount)
        order = client.order.create(
                {
                'receipt':reciept,
                # 'notes':notes,
                'amount':amount,
                'currency':currency
                }
            )
        

        context = {
            "order" : order,
            "ord_pay":ord_pay
        }
        return render(request, template_name="razor_payment.html", context=context)
# import re
@csrf_exempt
def VerificationView(request):
    # print(request.GET('id'))
    if request.method == "POST":
        data = request.POST
        # print(data)
        
        try:
            client.utility.verify_payment_signature(data)
            # print(data['razorpay_payment_id'])
            ord_id = request.GET.get('id')
            payment_details = Order.objects.get(id=ord_id)
            payment_details.razorpay_order_id=data['razorpay_order_id']
            payment_details.razorpay_payment_id=data['razorpay_payment_id']
            payment_details.razorpay_signature=data['razorpay_signature']
            payment_details.payment_status = True
            payment_details.save()
            print(payment_details.razorpay_order_id)
            
            return render(request,"success.html")
        except:
            ord_id = request.GET.get('id')
            payment_details = Order.objects.get(id=ord_id)
            payment_details.order_status = "Payment Failed..."
            payment_details.update()
            return HttpResponse("OOPS...!!!!Payment Failed")


# Customer Profile =================

class ProfileView(TemplateView):
    template_name = "profile.html"

    def dispatch(self, request, *args, **kwargs):
        
        if request.user.is_authenticated:
            print("user is  Logedin")
        else:
            return redirect("profile")

        return super().dispatch(request, *args,**kwargs)
    #-------------------------------------------
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user
        context[customer] = customer
        order = Order.objects.filter(cart__customer=customer)
        context["order"] = order
        return context

class SearchView(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get("search")
        print(search)
        contex = Product.objects.filter(Q (Product_name__icontains = search) | Q (brand__icontains = search) | Q (Description__icontains = search))
        context["contex"] = contex
        return context


# Seller models-----------------------------------------
class SellerView(CreateView):
    template_name = "seller.html"
    form_class = SellerForm
    success_url = reverse_lazy("seller")
    def form_valid(self, form):
        p=form.save()
        images = self.request.FILES.getlist("more_images")
        for i in images:
            Moreimage.objects.create(products=p , image=i)
        return super().form_valid(form)

class Dashboaer(TemplateView):
    template_name = "seller_order.html"
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        a=Order.objects.filter(order_status="Order received")
        print(a)
        context['pendingOrders'] = Order.objects.filter(order_status="Order received")
        return context

class OreddetailView(DetailView):
    template_name = "seller_orderdetails.html"
    model = Order
    context_object_name = "ord_obj"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["allstatus"] = ORDER_STATUS
        return context

class OrderStausView(View):
    def post(self,request,*args,**kwargs):
        ord_id = self.kwargs['pk']
        order_obj = Order.objects.get(id=ord_id)
        new_status = request.POST.get("status")
        order_obj.order_status = new_status
        order_obj.save()
        return redirect(reverse_lazy("admin_oder",kwargs={"pk":ord_id}))

# Seller urls, etc.....==============================================
def Seller_reg(request):
    return render(request, "sell_registration.html")

def Seller_Login(request):
    return HttpResponse("seller Login......")

def sell_signup(request):
    # if request.POST and request.FILES:
    #     f_name = request.POST['f_name']
    #     l_name = request.POST['l_name']
    #     email = request.POST['email']
    #     Phone = request.POST['Phone']
    #     dob = request.POST['dob']
    #     Doc_no = request.POST['Doc_no']
    #     IDproff = request.POST['IDproff']
    #     shop_reg = request.POST['shop_reg']
    #     shop_proff = request.POST['shop_proff']
    #     psw = request.POST['psw']
    #     psw_repeat = request.POST['psw_repeat']

    #     # if psw == psw_repeat:

    return redirect("seller_reg")