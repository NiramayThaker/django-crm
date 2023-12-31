from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, AddRecodForm
from .models import Record
from django.db.models import Q


@login_required(login_url='login/')
# Create your views here.
def home(request):
	records = Record.objects.all()
	q = request.GET.get('Q')

	if q is not None:
		records = Record.objects.filter(
			Q(first_name__icontains=q),
			# Q(last_name__icontains=q),
			# Q(email__icontains=q),
		)

	context = {'records': records}
	return render(request, "home.html", context=context)


def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['pswd']
		user = authenticate(username=username, password=password)
		print(user)
		if user is not None:
			login(request, user)
			messages.success(request, "Login Successfull")
			return redirect('home')
		else:
			messages.error(request, "Couldn't log in")
			return redirect('home')

	return render(request, 'login.html')


def logout_user(request):
	logout(request)
	messages.success(request, "User logged out.!")
	return redirect('home')


def register_user(request):
	reg_form = RegistrationForm()
	if request.method == "POST":
		reg_form = RegistrationForm(request.POST)
		if reg_form.is_valid():
			user = reg_form.save()
			if user is not None:
				login(request, user)
				messages.success(request, "User registered successfully")
				return redirect('home')
			else:
				messages.success(request, "Can't registered user")
				return redirect('register')

	context = {'reg_form': reg_form}
	return render(request, "user_reg.html", context=context)


def customer_record(request, pk):
	cust_rec = Record.objects.get(id=pk)

	context = {"cust_rec": cust_rec}
	return render(request, 'customer_record.html', context=context)


def delete_record(request, pk):
	if request.user.is_superuser:
		delete_it = Record.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Record deleted successfully .!")
		return redirect('home')

	messages.success(request, "Can only be deleted by super user")
	return redirect("home")


def add_record(request):
	record_form = AddRecodForm(request.POST or None)

	if request.method == 'POST':		
		if record_form.is_valid():
			add = record_form.save()
			messages.success(request, "Record added")
			return redirect("home")

	context = {"record_form": record_form}
	return render(request, 'add_record.html', context=context)


def update_record(request, pk):
	curr_record = Record.objects.get(id=pk)
	form = AddRecodForm(request.POST or None, instance=curr_record)

	if form.is_valid():
		form.save()
		messages.success(request, "Record Updated")
		return redirect("home")
	
	return render(request, "update_record.html", {"form": form})
