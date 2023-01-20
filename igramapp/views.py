from django.shortcuts import render,redirect,HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView,FormView,TemplateView,ListView,DetailView,UpdateView
from igramapp.models import MyUser,Post,Comments,Saved
from igramapp.forms import RegistrationForm,LoginForm,PostForm,ProfileUpdateForm,ChangePasswordForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth import views
# Create your views here.
def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"u must login")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

class ChangePasswordView(views.PasswordChangeView):
    model=MyUser
    form_class=ChangePasswordForm
    template_name = "changepassword.html"
    success_url=reverse_lazy('home')




class RegistrationView(CreateView):
    model=MyUser
    form_class=RegistrationForm
    template_name="registration.html"
    success_url=reverse_lazy('signin')

class LoginView(FormView):
    form_class=LoginForm
    template_name="login.html"
    def post(self, request, *args, **kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user=authenticate(request,username=username,password=pwd)
            if user:
                login(request,user=user)
                messages.success="login successful"
                return redirect('home')
            else:
                messages.error="login failed"
                return redirect('signin')
@method_decorator(signin_required,name="dispatch")
class HomeView(ListView):
    model=Post
    context_object_name='posts'
    template_name="home.html"
    
    def get_queryset(self):
        return reversed(Post.objects.all().exclude(user=self.request.user))



@method_decorator(signin_required,name="dispatch")
class UserDashboardView(ListView):
    model=Post
    context_object_name="myposts"
    template_name='userdashboard.html'
    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

# localhost :8000/home/posts/<int:id>/add_like
@signin_required
def add_like(request, *args, **kwargs):
    pid=kwargs.get("id")
    post=Post.objects.get(id=pid)
    post.like.add(request.user)
    return redirect('home')

@method_decorator(signin_required,name="dispatch")
class PostAddView(CreateView):
    model=Post
    form_class=PostForm
    template_name='addpost.html'
    success_url=reverse_lazy('home')
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)




def signout(request, *args, **kwargs):
    logout(request)
    return redirect('signin')

    
@method_decorator(signin_required,name="dispatch")
class PostDetailView(DetailView):
    model=Post
    template_name="postdetail.html"
    pk_url_kwarg="id"
    context_object_name="post"

@signin_required
def add_comment(request, *args, **kwargs):
    if request.method == 'POST':
        comment=request.POST.get('comment')
        pid=kwargs.get("id")
        post=Post.objects.get(id=pid)
        Comments.objects.create(user=request.user,post=post,comment=comment)
        return redirect('home')

@signin_required        
def get_comments(request, *args, **kwargs):
    pid=kwargs.get("id")
    post=Post.objects.get(id=pid)
    qs=Comments.objects.filter(post=post)
    return render(request,'home.html',context={"comments":qs})
      
#localhost:8000/home/<int:id>/remove_cmt
@signin_required   
def remove_comment(request,*args,**kwargs):
    cmt_id=kwargs.get("id")
    comment=Comments.objects.get(id=cmt_id)
    comment.delete()
    return redirect('home')


@signin_required   
def save_post(request, *args, **kwargs):
    pid=kwargs.get("id")
    post=Post.objects.get(id=pid)
    qss=Saved.objects.filter(user=request.user)
    qs=Saved.objects.create(user=request.user,saved_post=post)
    return redirect('home')
            
@method_decorator(signin_required,name="dispatch")
class SavedPosts(ListView):
    model=Saved
    template_name='saved.html'
    context_object_name='savedposts'
    def get_queryset(self):
        sposts= Saved.objects.filter(user=self.request.user)
        return sposts
    

@method_decorator(signin_required,name="dispatch")
class SavedPostDetailView(DetailView):
    model=Saved
    template_name="savedpostdetail.html"
    pk_url_kwarg="id"
    context_object_name="savedpost"

#localhost:8000/home/<int:id>useraccount
@method_decorator(signin_required,name="dispatch")
class UserAccountView(DetailView):
    pk_url_kwarg='id'
    model=MyUser
    template_name="useraccount.html"
    context_object_name="user"

#localhost:8000/home/<int:id>/follow/
# def follow_view(request, *args, **kwargs):
#     uid=kwargs.get('id')
#     usr=MyUser.objects.get(id=uid)
#     Follow.objects.create(user=usr).follow.add(request.user)
#     return redirect('home')
@signin_required
def saved_post_delete_view(request,*args,**kwargs):
    s_pid=kwargs.get('id')
    saved_post=Saved.objects.get(id=s_pid)
    saved_post.delete()
    return redirect('saved-posts')


@signin_required
def post_delete_view(request,*args,**kwargs):
    pid=kwargs.get("id")
    post=Post.objects.get(id=pid)
    post.delete()
    return redirect('userdashboard')

@method_decorator(signin_required,name="dispatch")
class EditProfileView(UpdateView):
    model=MyUser
    pk_url_kwarg='id'
    form_class=ProfileUpdateForm
    template_name='editprofile.html'
    success_url=reverse_lazy('userdashboard')
    