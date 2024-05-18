from typing import Any
from django.forms import BaseModelForm
from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login,authenticate,logout,update_session_auth_hash
from django.contrib import messages
from .models import Products,Comments
from django.contrib.auth.decorators import login_required
from .forms import UserSignupForm,LoginForm,WebsiteLoginForm,User_product_data,User_comment
from django.views.generic.edit import UpdateView,DeleteView
from django.views.generic import TemplateView

# Create your views here.

def home_page(request):
  if request.user.is_authenticated:
   fm = Products.objects.all()
   return  render(request,'base.html',{'products':fm})
  else:
    return HttpResponseRedirect('/signup/')



def signup_form(request):
  if request.method == 'POST':
    form = UserSignupForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,'Your account has been crated successfully !')
      return HttpResponseRedirect('/signup/')
  else:
    form = UserSignupForm()
  return render(request,'signup.html',{'form':form})




def login_form(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = LoginForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Welcome to Your Profile')
                    return HttpResponseRedirect('/home/')
            # Form is invalid or authentication failed
        else:
            fm = LoginForm()
        return render(request, 'login_form.html', {'form': fm})
    else:
        return HttpResponseRedirect('/home/')


def logout_form(request):
     logout(request)
     return HttpResponseRedirect('/home/')

def Website_Login_Form(request):
  if request.method == 'POST':
    fm = WebsiteLoginForm(request=request,data=request.POST)
    if fm.is_valid():
      uname = fm.cleaned_data['username']
      upass = fm.cleaned_data['password']
      user = authenticate(username=uname,password=upass)
      if user is not None:
        login(request,user)
        messages.success(request,'Welcom to Your Profile')
        return HttpResponseRedirect('/userweb/')
  else:
    fm = WebsiteLoginForm()
  return render(request,'user_startup_page.html',{'form':fm})

@login_required
def user_product(request):
  if request.method == 'POST':
    fm = User_product_data(request.POST, request.FILES)
    if fm.is_valid():
       product = fm.save(commit=False)
       product.user = request.user  # Set the user to the current user
       product.save()
       messages.success(request,'Your data Saved Successfully')
       return HttpResponseRedirect('/userweb/')
  else:
    fm = User_product_data()
  return render(request,'user_website.html',{'form':fm})


@login_required
def show_product(request):
  fm = Products.objects.filter(user=request.user)
  return render(request,'product.html',{'fm':fm})


class UpdateUser_product(UpdateView):
  template_name = 'update_product.html'
  model = Products
  fields = ['title','description','image','price']

  success_url = '/yourproduct/'


class DeleteUser_product(DeleteView):
  template_name = 'delete_product.html'
  model = Products
  success_url = '/yourproduct/'


class boot_product(TemplateView):
  template_name = 'boot_product.html'

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context =  super().get_context_data(**kwargs)
    tname = self.kwargs.get('name')
    product = Products.objects.filter(title = tname)
    products = Products.objects.filter(title=tname).first()

    context['bproduct']= product
    return context



def User_comments(request, id):
    product = Products.objects.get(pk=id)
    all_comment = Comments.objects.filter(product_id=product)
    products = Products.objects.filter(pk=id).first()

    if request.method == 'POST':
        cmt = User_comment(request.POST)
        if cmt.is_valid():
            comment = cmt.save(commit=False)
            comment.product_id = product
            if request.user.is_authenticated:
                if request.user != product.user:
                    comment.user = request.user
                    comment.save()
                    messages.success(request, 'Comment submitted successfully')
                    return redirect('comment',id=comment.product_id.id)
                else:
                    messages.error(request, "A user cannot comment on their own product")
            else:
                messages.error(request, "Only logged-in users can add comments")
                return HttpResponseRedirect('/weblogin/')
    else:
        cmt = User_comment()

    return render(request, 'comment.html', {'comment': cmt, 'all_comment': all_comment, 'prdct': product, 'req_user': request.user.id, 'p_user': products.user.id})

class YourCommentUpdate(UpdateView):
  template_name = 'update_comment.html'
  model = Comments
  form_class = User_comment
  context_object_name = 'comt'

  def get_success_url(self) -> str:
    updated_comment_id = self.object.pk
    comment_object = Comments.objects.get(id = updated_comment_id)
    return reverse('comment',kwargs={'id':comment_object.product_id.id})

  def form_valid(self, form: BaseModelForm) -> HttpResponse:
     messages.success(self.request,'comment update successfully')
     return super().form_valid(form)


class YourCommentDelete(DeleteView):
  template_name = 'delete_comment.html'
  model = Comments
  success_url = '/home/'
  def get_success_url(self) -> str:
    updated_comment_id = self.object.pk
    object_id = Comments.objects.get(id=updated_comment_id)
    return reverse('comment',kwargs={'id':object_id.product_id.id})

  def form_valid(self,form):
    messages.success(self.request,'Your comment deleted succefully')
    return super().form_valid(form)

  # cart function

def add_cart(request,id):
    total = request.session.get('total',0)
    count = request.session.get('count',0)
    cart = request.session.get('cart',[])
    count += 1
    request.session['count'] = count
    price = Products.objects.get(id=id).price
    total += price
    cart.append(id)
    request.session['cart'] = cart
    grand_total = request.session['total'] = total
    request.session['count'] = count
    print(grand_total)
    messages.success(request,'your item add to cart succesfully')
    return HttpResponseRedirect('/home/')

def view_cart(request):
  cart = request.session.get('cart',[])
  cart_product= Products.objects.filter(pk__in=cart)
  total_price = request.session.get('total',0)
  return render(request,'cart_product.html',{'cart_products':cart_product,'total_price':total_price})


def delete_cart_items(request,id):
  cart = request.session.get('cart',[])
  total = request.session.get('total',0)
  count = request.session.get('count',0)

  price = Products.objects.get(id=id).price
  total -= price
  count -= 1
  request.session['total'] = total
  request.session['count'] = count
  if id in cart:
    cart.remove(id)
  request.session['cart']=cart
  return HttpResponseRedirect('/viewcart/')