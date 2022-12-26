from django.shortcuts import render,HttpResponse
from django.http import HttpResponseRedirect,JsonResponse
from toyapp.models import *
import os 
import random
import string
from django.conf import settings
from django.core.mail import send_mail



def index(request):
	return render(request,'index.html')
def contact(request):
	return render(request,'contact.html')
def demo(request):
	return render(request,'demo.html')
def about(request):
	return render(request,'about.html')
def register(request):
	if request.method == "POST":
		uname=request.POST['Your Name']
		uemail=request.POST['Your Email']
		upassword=request.POST['password']
		check=toyreg_tb.objects.filter(email=uemail)
		if check:
			return render(request,'index.html',)
		else:
			add=toyreg_tb(name=uname,email=uemail,password=upassword)
			add.save()
			x = ''.join(random.choices(uname + string.digits, k=8))
			y = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
			subject = 'welcome to toyshop'
			message = f'Hi {uname}, thank you for registering in toyshop . your user username: {uemail} and  password: {upassword}. Follow https://Wa.me/+18478527243 or https://www.tinder.com'
			email_from = settings.EMAIL_HOST_USER 
			recipient_list = [uemail, ] 
			send_mail( subject, message, email_from, recipient_list ) 
			return render(request,'header&footer.html',)
	else:
		return render(request,'/')
	return render()
def saveupdate(request):
	    if request.method == "POST":
	    	userid=request.GET['uid']
	    	uname=request.POST['Your Name']
	    	uemail=request.POST['Your Email']
	    	upassword=request.POST['password']
	    	add=toyreg_tb.objects.filter(id=userid).update(name=uname,email=uemail,password=upassword)
	    	return HttpResponseRedirect('/register/')
	    else:
	    	return render(request,'index.html')

	
def login(request):
		if request.method == "POST":
			uemail=request.POST['Your Email']
			upassword=request.POST['password']
			check=toyreg_tb.objects.filter(email=uemail,password=upassword)
			if check:
				for x in check:
					request.session['myid']=x.id
					request.session['myname']=x.name

				return render(request,'index.html',)

			else:
				return render(request,'index.html',)

		else:
			return render(request,'index.html')
def logout(request):
	if request.session.has_key('myid'):
		del request.session['myname']
		del request.session['myid']
	return HttpResponseRedirect('/')
def product(request):
	data= product_tb.objects.all()
	return render(request,'product.html',{"user":data})
def single(request):
	if request.session.has_key("myid"):
		pid=request.GET['uid']
		check=product_tb.objects.filter(id=pid)
		return render(request,'single.html',{"user":check})
	else:
		return render(request,'product.html')
	# else:
	# 	return HttpResponseRedirect('/login/')
def payment(request):
	if request.session.has_key("myid"):
		if request.method=='POST':
			uid=request.session['myid']
			uidd=toyreg_tb.objects.get(id=uid)
			amt=request.POST['tpay']
			data=pay_tb.objects.filter(uid=uidd,totalp=amt,pstatus='pending')
			if data:
				return render(request,'payment.hmtl')
			else:
				add=pay_tb(uid=uidd,totalp=amt,pstatus='paid')
				add.save()
				cart_tb.objects.filter(uid=uidd,status='pending').update(status='paid')
				return  HttpResponseRedirect('/')
		else:
			total=request.GET['tpay']
			uid=request.session['myid']
			data=toyreg_tb.objects.filter(id=uid)
			for x in data:
				name=x.name
			return render(request,'payment.html',{'amount':total,'name':name})
	else:
		return HttpResponseRedirect("//")	    		

def typography(request):
	return render(request,'typography.html')
def addcart(request):
	if request.session.has_key("myid"):
		if request.method=='POST':
			pid=request.GET['uid']
			data=product_tb.objects.filter(id=pid)
			for x in data:
				unitprice=int(x.price)
			uid=request.session['myid']
			uidd=toyreg_tb.objects.get(id=uid)
			pidd=product_tb.objects.get(id=pid)
				
			tprice=(1*unitprice)
			delv=unitprice+((unitprice*10)/100)
			check=cart_tb.objects.filter(pid=pidd,uid=uidd,status="pending")
			if check:
				prod=cart_tb.objects.filter(uid=uidd,pid=pidd,status="pending")
				
				return render(request,"demo.html",{"error":"already in cart","data":prod})
			else:
				add=cart_tb(pid=pidd,uid=uidd,pqty=1,totalprice=delv)
				add.save()
				return HttpResponseRedirect('/cart/')
		else:
			return render(request,"cart.html")
	else:
		return render(request,"product.html")
def additem(request):
	proid=request.GET['cid']
	quantity= request.GET['pqty']
	data= cart_tb.objects.filter(id=proid)
	for x in data:
		unitprice=int(x.price)
	delv=unitprice+((unitprice*10)/100)
	acart=cart_tb.objects.filter(id=proid).update(pid=pidd,uid=uidd,totalprice=delv)
	return HttpResponseRedirect('/cart/')

             	


	
# Create your views here.
def cart(request):
	uid= request.session['myid']
	prod=cart_tb.objects.filter(uid=uid,status="pending")
	count=cart_tb.objects.filter(uid=uid,status="pending").count()
	total =0
	for x in prod:
		tprice =x.totalprice
		total= float(tprice)+total
		return render(request,'demo.html',{"data":prod,'count':count,'total':total})
def cartupdate(request):
	# if request.method== 'POST':
	cid=request.GET['cid']
	qty=request.POST['qty']
	add=cart_tb.objects.filter(id=cid)
	total=0
	for x in add:
		price=x.pid.price
	total=int(price)*int(qty)
	qid=cart_tb.objects.filter(id=cid).update(pqty=qty,totalprice=total)
	return HttpResponseRedirect('/cart/')
	# else:
	#    return render(request,'product.html')	


def checkout(request):
	if request.method == "POST":
		cname=request.POST['finame']
		cnumber=request.POST['number']
		clandm=request.POST['land']
		ctown=request.POST['town']
		total=request.GET['total']
		uid=request.session['myid']
		uidd=toyreg_tb.objects.get(id=uid)
		# view=check_tb.objects.filter(fname=cname,town=ctown)
		# if view:
			# print("if-----")
			# return render(request,'payment.html',{"error":"allredy submitted"})
		# else:
			# print("else-----")

		add=check_tb(fname=cname,pnumber=cnumber,landm=clandm,town=ctown,uid=uidd)
		add.save()
		return render(request,'payment.html',{"success":"submitted Successfully","total":total})
	else:
		total=request.GET['total']
		print(total,"--------**************")

		return render(request,'checkout.html',{"total":total})

	

	






################################################# ADMIN  ####################################################################################



def blank(request):
	return render(request,"admin/blank.html")
def buttons(request):
	return render(request,"admin/buttons.html")
def charts(request):
	return render(request,"admin/charts.html")
def grids(request):
	return render(request,"admin/grids.html")
def icons(request):
	return render(request,"admin/icons.html")
def inbox_details(request):
	return render(request,"admin/inbox-details.html")
def inbox(request):
	if request.method=='POST':
		pname=request.POST['Product Name']
		pprice=request.POST['price']
		pdescription=request.POST['description']
		pimages=request.FILES['Images']
		check=product_tb.objects.filter(proname=pname)
		if check:
			return render(request,'admin/inbox.html',)
		else:
			add=product_tb(proname=pname,price=pprice,prodescription=pdescription,proimage=pimages)
			add.save()
			return render(request,"admin/inbox.html")
	else:
		return render(request,"admin/inbox.html")
def edit(request):
	# pid=request.GET['tid']
	newedit=product_tb.objects.all()
	return render(request,'admin/inboxtable.html',{"user":newedit})
def delete(request):
	pid=request.GET['uid']
	data=product_tb.objects.filter(id=pid).delete()
	return HttpResponseRedirect('/inbox/')

	
def toysave(request):
	if request.method =="POST":
		pname=request.POST['Product Name']
		pprice=request.POST['price']
		pdescription=request.POST['description']
		pid=request.GET['tid']
		img=request.POST['img']
		if img =="yes":
			pimages=request.FILES['Images']
			old=product_tb.objects.filter(id=pid)
			new=product_tb.objects.get(id=pid)
			for x in old:
				proimage=x.proimage.url
				pathtoimage=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+proimage
				if os.path.exists(pathtoimage):
					os.remove(pathtoimage)
					print('Successfully deleted')
			new.proimage=pimages
			new.save()
		add=product_tb.objects.filter(id=pid).update(proname=pname,price=pprice,prodescription=pdescription)
			
		return HttpResponseRedirect('/edit/')
	else:
		pid=request.GET['tid']
		newedit=product_tb.objects.filter(id=pid)
		return render(request,'admin/inboxupdate.html',{"user":newedit})

def admin_index(request):
	return render(request,"admin/index.html")
def admin_login(request):
	    if request.method == "POST":
	    	aemail=request.POST['email']
	    	apassword=request.POST['password']
	    	check=admreg_tb.objects.filter(admemail=aemail,admpassword=apassword)
	    	if check:
	    		for x in check:
	    			request.session['myid']=x.id
	    			request.session['myname']=x.admname
	    			return render(request,'admin/index.html',)
	    	else:
	    		return render(request,'admin/login.html',)
	    else:
	    	return render(request,"admin/login.html")
def admin_logout(request):
	if request.session.has_key('myid'):
		del request.session['myname']
		del request.session['myid']
		return HttpResponseRedirect('/')
def forgetpassword(request):
	if request.method =="POST":
		aemail=request.POST["email"]
		check=admreg_tb.objects.filter(admemail=aemail)
		if check:
			return render(request,'admin/resetpassword.html',{"data":check})
		else:
			return render(request,'admin/signup.html')
	else:
		return render(request,'admin/forgetpassword.html')
def reset(request):
	if request.method =="POST":
		uid=request.POST["uid"]
		apassword=request.POST['newpassword']
		cnpassword=request.POST['cnpassword']
		if apassword == cnpassword:
			newpass=admreg_tb.objects.filter(id=uid).update(admpassword=apassword)
			return HttpResponseRedirect('/adminlogin/')
		else:
			return render(request,'admin/resetpassword.html',{"error":"password doesnot match"})
	else:
		return render(request,'admin/resetpassword.html',{"user":newpass})




def maps(request):
	return render(request,"admin/maps.html")
def portlet(request):
	return render(request,"admin/portlet.html")
def price(request):
	return render(request,"admin/price.html")
def admin_product(request):
	return render(request,"admin/product.html")
def signup(request):
	data= admreg_tb.objects.all()
	if request.method == "POST":
		aname=request.POST["uname"]
		aemail=request.POST["email"]
		apassword=request.POST["password"]
		check=admreg_tb.objects.filter(admemail=aemail)
		if check:
			return render(request,'admin/index.html',)
		else:
			add=admreg_tb(admname=aname,admemail=aemail,admpassword=apassword)
			add.save()
			x = ''.join(random.choices(aname + string.digits, k=8))
			y = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
			subject = 'welcome to shoppy admin'
			message = f'Hi {aname}, thank you for registering in shoppy admin . your user username: {aemail} and  password: {apassword}. Follow https://Wa.me/+18478527243 or https://www.tinder.com'
			email_from = settings.EMAIL_HOST_USER 
			recipient_list = [aemail, ] 
			send_mail( subject, message, email_from, recipient_list ) 
			return render(request,'admin/signup.html')
	else:
		return render(request,'admin/ajaxnew.html',{"data":data})
def view(request):
	print("hello")
	a=request.GET.get('p')
	b=admreg_tb.objects.all().filter(id=a)
	for x in b:
		v=x.admname
		w=x.admemail
		
	dat={"aa":v,"bb":w}
	print(dat)
	return JsonResponse(dat)

	
def typography(request):
	return render(request,"admin/typography.html")
def admregtable(request):
	view=admreg_tb.objects.all()
	return render(request,'admin/admregtable.html',{"user":view})
from reportlab.pdfgen import canvas 
from django.views.generic import View
from toypro.utils import render_to_pdf

def pdf(request):	
	uid=request.GET['uid']	
	users= admreg_tb.objects.filter(id=uid)
	pdf=render_to_pdf('admin/view.html',{'data':users})
	return HttpResponse(pdf,content_type='application/pdf')
  
  