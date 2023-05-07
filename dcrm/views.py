from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record


# Create your views here.
def index(request):
    records = Record.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('index')
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('index')
    else:
        return render(request, 'index.html', {'records':records})

def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out")
    return redirect('index')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.info(request, "You have successfully registered")
            return redirect('index')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})
    

def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.info(request, "You have to be logged to see this page...")
        return redirect('index')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.info(request, "You have sucessfully deleted the record. ")
        return redirect('index')
    else:
        messages.info(request, "You have to be logged to see this page...")
        return redirect('index')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.info(request, "You added a new record sucessfuly")
                return redirect('index')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.info(request, "You added a new record sucessfuly")
        return redirect('index')
    
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id= pk)
        form = AddRecordForm(request.POST or None, instance = current_record)
        
        if form.is_valid():
            form.save()
            messages.info(request, "Your record has been updated")
            return render(request, 'index.html')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.info(request, "Your must be logged in")
        return redirect('home')