from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User, UserManager
from .models import Message, Comment
import bcrypt

def index(request):
    return render(request, "wall_app/index.html")

def wall(request):
    if "logged_user" not in request.session:
        return redirect ("/")
    context={
        "user" : User.objects.get(id=request.session["logged_user"]),
        "messages" : Message.objects.all(),
        "comments" : Comment.objects.all(),
    }
    return render(request, "wall_app/wall.html", context)

def registration(request):
    errors = User.objects.register_validation(request.POST)
    if len(errors) > 0:
        for key, values in errors.items():
            messages.error(request, values)
        return redirect("/")
    new_user=User.objects.create(
        first_name=request.POST["first_name"],
        last_name=request.POST["last_name"],
        email=request.POST["email"],
        password=bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
    )
    request.session["logged_user"] = new_user.id 
    return redirect("/wall")

def login(request):
    errors = User.objects.login_validation(request.POST)
    if len(errors) > 0:
        for key, values in errors.items():
            messages.error(request, values)
        return redirect ("/")
        
    user = User.objects.get(email=request.POST["email"])
    request.session["logged_user"] = user.id
    return redirect("/wall")

def log_out(request):
    request.session.clear()
    return redirect ("/")

def postMassage(request):
    posting_user = User.objects.get(id=request.session["logged_user"])
    post = Message.objects.create(message=request.POST["add_post"], user=posting_user)
    return redirect("/wall")

def add_Comment(request):
    comment_user = User.objects.get(id=request.session["logged_user"])
    post = Message.objects.get(id=request.POST["post_id"])
    comment = Comment.objects.create(comment=request.POST["add_comment"], message=post, user=comment_user)
    return redirect("/wall")

def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return redirect("/wall")
