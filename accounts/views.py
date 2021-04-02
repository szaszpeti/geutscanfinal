from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
import pandas as pd

from datetime import datetime, time, date

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


# Create your views here.
from .models import *
from .forms import *
from .filters import InspectionFilter
from .decorators import unauthenticated_user, allowed_users, admin_only


def post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
    else:
        form = PostForm()

    try:
        posts = Post.objects.all()
    except Post.DoesNotExist:
        posts = None

    return render(request, 'accounts/post.html', { 'posts': posts, 'form': form })

@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')


            messages.success(request, 'Account was created for ' + username)

            return redirect('login')


    context = {'form':form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    inspections = Inspection.objects.all()
    technicians = Technician.objects.all()

    total_technicians = technicians.count()
    print(total_technicians)

    total_inspections = inspections.count()
    # delivered = orders.filter(status='Delivered').count()
    # pending = orders.filter(status='Pending').count()
    myFilter = InspectionFilter(request.GET, queryset=inspections)
    inspections = myFilter.qs

    context = {'inspections':inspections, 'technicians':technicians,
    'total_inspections':total_inspections, 'myFilter':myFilter}

    return render(request, 'accounts/dashboard.html', context)


# def userPage(request):
#     orders = request.user.customer.order_set.all()

#     total_orders = orders.count()
#     delivered = orders.filter(status='Delivered').count()
#     pending = orders.filter(status='Pending').count()

#     print('ORDERS:', orders)

#     context = {'orders':orders, 'total_orders':total_orders,
#     'delivered':delivered,'pending':pending}
#     return render(request, 'accounts/user.html', context)


def accountSettings(request):
    technician = request.user.technician
    form = TechnicianForm(instance=technician)

    if request.method == 'POST':
        form = TechnicianForm(request.POST, request.FILES,instance=technician)
        if form.is_valid():
            form.save()


    context = {'form':form}
    return render(request, 'accounts/account_settings.html', context)




@login_required(login_url='login')
def inspections(request):
    inspections = Inspection.objects.all()

    return render(request, 'accounts/inspections.html', {'inspections':inspections})

@login_required(login_url='login')
def technician(request, pk_test):
    technician = Technician.objects.get(id=pk_test)

    inspections = technician.inspection_set.all()
    inspection_count = inspections.count()

    myFilter = InspectionFilter(request.GET, queryset=inspections)
    inspections = myFilter.qs

    context = {'technician':technician, 'inspections':inspections, 'inspection_count':inspection_count,
    'myFilter':myFilter}
    return render(request, 'accounts/technician.html',context)

@login_required(login_url='login')
def detailInspection(request, pk):
    inspection = Inspection.objects.get(id=pk)
    photos = InspectionImage.objects.filter(inspection=inspection)

    #counting the hours spent on work
    time_start = datetime.combine(date.min, inspection.time_start_1) - datetime.min
    time_end = datetime.combine(date.min, inspection.time_end_6) - datetime.min
    print("TIMEEEEE", time_start)

    hours = (time_end - time_start).seconds/3600


    context = {'inspection':inspection, 'photos':photos, 'hours':hours}

    return render(request, 'accounts/inspection_detail.html', context)

@login_required(login_url='login')
def detailPandas(request, pk):
    qs = Inspection.objects.all().values()
    data = pd.DataFrame(qs)


    inspection = Inspection.objects.get(id=pk)

    context = {'inspection':inspection, 'data':data.to_html()}

    return render(request, 'accounts/pandas_detail.html', context)

@login_required(login_url='login')
def createInspection(request):
	form = InspectionForm()
    # InspectionFormSet = inlineformset_factory(Technician, Inspection, fields='__all__')
    # technician = Technician.objects.get(id=pk)
    # print('TECHNICIAN:' , technician)
    # formset = InspectionFormSet(queryset=Inspection.objects.none(),instance=technician)
    # #form = OrderForm(initial={'customer':customer})

	if request.method == 'POST':
        #print('Printing POST:', request.POST)
		form = InspectionForm(request.POST)
        #formset = InspectionFormSet(request.POST, instance=technician)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/inspection_form.html', context)


def addPhoto(request, pk):
    inspection = Inspection.objects.get(id=pk)

    if request.method == 'POST':
        images = request.FILES.getlist('images')

        for image in images:
            photo = InspectionImage.objects.create(
                inspection=inspection,
                images=image,
            )

        return redirect('/')

    context = {'inspections': inspection}
    return render(request, 'accounts/addphoto.html', context)


def inspectionRenderPdf(request, pk):
    inspection = Inspection.objects.get(id=pk)
    photos = InspectionImage.objects.filter(inspection=inspection)

    template_path = 'accounts/pdf2.html'
    context = {'inspection': inspection, 'photos':photos}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #if download:
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    #if display:
    response['Content-Disposition'] = 'filename="report.pdf"'


    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



def renderPdfView(request):
    template_path = 'accounts/pdf1.html'
    context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #if download:
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    #if display:
    response['Content-Disposition'] = 'filename="report.pdf"'


    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


@login_required(login_url='login')
def updateInspection(request, pk):
    inspection = Inspection.objects.get(id=pk)
    form = InspectionForm(instance=inspection)
    print('INSPECTION:', inspection)
    if request.method == 'POST':

        form = InspectionForm(request.POST, instance=inspection)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/inspection_form.html', context)

@login_required(login_url='login')
def deleteInspection(request, pk):
    inspection = Inspection.objects.get(id=pk)
    if request.method == "POST":
        inspection.delete()
        return redirect('/')

    context = {'item':inspection}
    return render(request, 'accounts/delete.html', context)
