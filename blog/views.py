from typing import Any
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView
from .forms import CommentForm, RegisterForm
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data
    



#def starting_page(request):
    #Wlates_posts = Post.objects.all().order_by("-date")[:3]
    #Wreturn render(request, "blog/index.html", {
        #"posts": lates_posts
    #W})

class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"




#Wdef posts(request):
    #Wall_posts = Post.objects.all().order_by("-date")
    #return render(request, "blog/all-posts.html", {
       #W "posts": all_posts
    #})

class SinglePostView(View):

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        stored_post = request.session.get("stored_post")
        if stored_post is not None:
            is_saved_for_later = post.id in stored_post
        context = {
            "post": post,
            "tags": post.tag.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later" : is_saved_for_later
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):  
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save() 
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
        stored_post = request.session.get("stored_post")
        if stored_post is not None:
            is_saved_for_later = post.id in stored_post
        context = {
            "post": post,
            "tags": post.tag.all(),
            "comment_form": comment_form,
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later" : is_saved_for_later
        }
        return render(request, "blog/post-detail.html", context)
   




#Wdef post_detail(request, slug):
    #Wrest_post = get_object_or_404(Post, slug=slug)
    #Wreturn render(request, "blog/post-detail.html", {
        #W"post": rest_post,
        #"tags": rest_post.tag.all()
    #})

class ReadLaterView(View):
    def get(self, request):
        stored_post = request.session.get("stored_post")
        context = {}
        if stored_post is None or len(stored_post) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_post)
            context["posts"] = posts
            context["has_posts"] = True
        return render(request, "blog/stored-posts.html", context)    


    def post(self, request):
        stored_post = request.session.get("stored_post")
        if stored_post is None:
            stored_post = []
        post_id = int(request.POST["post_id"])    
        if post_id not in stored_post:    
            stored_post.append(post_id)   
        else:
            stored_post.remove(post_id)
        request.session["stored_post"] = stored_post

        return HttpResponseRedirect("/")        


def register(request):
    if request.method == "POST":
        forms = RegisterForm(request.POST)
        if forms.is_valid():
            forms.save()
            username = forms.cleaned_data.get("username")
            messages.success(request, f"Welcome {username}")
            return HttpResponseRedirect("/login")
    else:    
        forms = RegisterForm()
    return render(request, "blog/register.html", {
        "forms": forms
    })

@login_required
def profile(request):
    return render(request, "blog/profile.html")

