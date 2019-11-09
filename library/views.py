from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from . forms import UserRegisterForm,UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . models import Post,Admin,Book,Notice,IssueBook
from django.shortcuts import get_object_or_404
import datetime
from django.db.models import Q
from datetime import date
from datetime import timedelta
from django.db.models import F


def index(request):
    if request.session.get('name') is not None:
        obj = Admin.objects.get(Q(username=request.session.get('name')))
        return render(request, 'library/adminpage.html', {'name': obj.username})
    return render(request, 'library/index.html')

def login(request):
    if request.session.get('name') is not None:
        return render(request, 'library/adminpage.html')
    return render(request, 'library/login.html')

def base(request):
    return render(request, 'library/base.html')

def addbook(request):
    if request.session.get('name') is None:
        return render(request, 'library/index.html')
    bid = request.POST.get('bid')
    title = request.POST.get('title')
    author = request.POST.get('author')
    subject = request.POST.get('subject')
    content = request.POST.get('content')
    quantity = request.POST.get('quantity')
    try:
        obj1 = Book.objects.get(Q(bookid=bid))
        if obj1 is not None:
            return render(request, 'library/addbook.html', {'note': 'This Book is already exist'})
        else:
            ob = Book(
                bookid =bid,
                title = title,
                content = content,
                quantity = quantity,
                author = author,
                subject = subject
            )
            ob.save()
            return render(request, 'library/addbook.html', {'note': 'New Book Added Successfully.....'})
    except:
        if title and content and quantity and author and subject is not None:
            ob = Book(
                bookid=bid,
                title=title,
                content=content,
                quantity=quantity,
                author=author,
                subject=subject
            )
            ob.save()
            obj = Admin.objects.get(Q(username=request.session.get('name')))
            val = obj.count
            val = val + 10
            Admin.objects.filter(username=obj.username).update(count=val + 1)
            return render(request, 'library/addbook.html', {'note': 'New Book Added Successfully.....', 'val': val})
        else:
            return render(request, 'library/addbook.html')
    return render(request, 'library/addbook.html')


def newadmin(request):
    if request.session.get('name') is None:
        return render(request, 'library/index.html')
    user = request.POST.get('username1')
    pas = request.POST.get('pass')
    cpas = request.POST.get('cpass')
    if user and pas:
        try:
            obj = Admin.objects.get(Q(username=user))
            if obj is not None:
                return render(request, 'library/newadmin.html', {'note':'Admin already exist'})
            else:
                if pas == cpas:
                    ob =  Admin(
                        username = user,
                        password = pas
                    )
                    ob.save()
                    return render(request, 'library/newadmin.html', {'note':'New Admin Created Successfully.....'})
                else:
                    return render(request, 'library/newadmin.html', {'note':'Password Mismatch'})
        except:
            if pas == cpas:
                ob = Admin(
                    username=user,
                    password=pas
                )
                ob.save()
                return render(request, 'library/newadmin.html', {'note': 'New Admin Created Successfully.....'})
            else:
                return render(request, 'library/newadmin.html', {'note': 'Password Mismatch'})
            return render(request, 'library/newadmin.html')
    return render(request, 'library/newadmin.html')

def adminpage(request):
    if request.session.get('name') is not None:
        obj = Admin.objects.get(Q(username=request.session.get('name')))
        return render(request, 'library/adminpage.html', {'val':obj.count+10 , 'rval':obj.rcount+10, 'eval':obj.ecount+10, 'pval':obj.pcount+10})
    else:
        return render(request, 'library/adminlogin.html')

def adminlogin(request):
    if request.session.get('name') is not None:
        obj = Admin.objects.get(Q(username=request.session.get('name')))
        val = obj.count+10
        return render(request, 'library/adminpage.html', {'val':obj.count , 'rval':obj.rcount+10, 'eval':obj.ecount+10, 'pval':obj.pcount+10})
    user = request.POST.get('username1')
    pas = request.POST.get('pass')
    if user and pas:
        try:
            obj = Admin.objects.get(Q(username=user))
            if obj is not None:
                if obj.password == pas:
                    request.session['name'] = user
                    return render(request, 'library/adminpage.html', {'val':obj.count , 'rval':obj.rcount+10, 'eval':obj.ecount+10, 'pval':obj.pcount+10})
                else:
                    notification = {'user': user,
                                    'note': 'Password incorrect',
                                    }
                    return render(request, 'library/adminlogin.html', notification)
            else:
                return render(request, 'library/adminlogin.html')
        except:
            return render(request, 'library/adminlogin.html', {'note': 'Admin Not Valid'})
    else:
        return render(request, 'library/adminlogin.html')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance= request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context ={
            'u_form': u_form,
            'p_form': p_form
        }
        return render(request, 'library/profile.html', context)



def wel(request):
    if request.user.is_authenticated:
        today = date.today() - timedelta(days=7)
        ob = IssueBook.objects.filter(Q(issuedate__lte=today), Q(user=request.user))
        obj=IssueBook.objects.filter(Q(user=request.user))
        obj1 = Notice.objects.filter(Q(user=request.user))
        fval=len(ob)*10
        rval=len(obj)*10
        pval=len(obj1)*10
        return render(request, 'library/wel.html',{'rval':rval,'pval':pval,'fval':fval})
    return render(request, 'library/index.html')

def adminlogout(request):
    request.session.clear()
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('index')
    else:
        form =UserRegisterForm()
    return render(request, 'library/register.html', {'form': form})


def contact(request):
    return render(request, 'library/contact.html')

def gallery(request):
    return render(request, 'library/gallery.html')

def about(request):
    return render(request, 'library/about.html')

def services(request):
    return render(request, 'library/services.html')

def removebook(request):
    if request.session.get('name') is None:
        return render(request, 'library/index.html')
    bid = request.POST.get('title')
    author = request.POST.get('author')
    if bid and author:
        try:
            obj1 = Book.objects.get(Q(bookid=bid), Q(author=author))
            if obj1 is not None:
                obj = Admin.objects.get(Q(username=request.session.get('name')))
                val = obj.rcount
                Admin.objects.filter(username=obj.username).update(rcount=val + 1)
                obj1.delete()
                return render(request, 'library/removebook.html', {'note':'delete a book successfully......'})
        except:
            return render(request, 'library/removebook.html',  {'note':'Not Found'})
    return render(request, 'library/removebook.html')

def editbook(request):
    if request.session.get('name') is None:
        return render(request, 'library/index.html')
    bid = request.POST.get('title')
    author = request.POST.get('author')
    test = request.POST.get('edit_first')
    if test == 'edit_fst':
        if bid and author:
            try:
                obj1 = Book.objects.get(Q(bookid=bid), Q(author=author))
                if obj1 is not None:
                    return render(request, 'library/editbook.html', {'obj1': obj1})
            except:
                return render(request, 'library/editbook.html', {'note': 'Not Found'})
    else:
        if request.POST.get('content') and request.POST.get('quantity') and request.POST.get('subject') is not None:
            content =request.POST.get('content')
            quantity = request.POST.get('quantity')
            subject = request.POST.get('subject')
            Book.objects.filter(bookid=bid).update(content=content, author=author, quantity=quantity, subject=subject)
            obj = Admin.objects.get(Q(username=request.session.get('name')))
            val = obj.ecount
            Admin.objects.filter(username=obj.username).update(ecount=val + 1)
            return render(request, 'library/editbook.html', {'note': 'Updation Successfully.....'})
            return render(request, 'library/editbook.html')
        return render(request, 'library/editbook.html')



def notice(request):
    if request.session.get('name') is None:
        return render(request, 'library/index.html')
    title = request.POST.get('title')
    content = request.POST.get('content')
    if title and content is not None:
        obj = Post(
            title=title,
            content = content,
            date_posted=date.today(),
            author=request.session.get('name')
        )
        obj.save()
        obj = Admin.objects.get(Q(username=request.session.get('name')))
        val = obj.pcount
        Admin.objects.filter(username=obj.username).update(pcount=val + 1)
        return render(request,'library/notice.html', {'note':'Notice added Successfully.....'})
    return render(request, 'library/notice.html')

def studentaddbook(request):
    if not request.user.is_authenticated :
        return render(request,'library/index.html')
    sbtn = request.POST.get('result')
    item = request.POST.get('searchbook')
    objp = Post.objects.all()
    if request.method=='POST':
        try:
            if sbtn == 'tit':
                obj12 = Book.objects.filter(Q(title__icontains=item))
                if len(obj12)>0:
                    return render(request, 'library/studentaddbook.html', {'obj12': obj12, 'objp':objp})
                else:
                    return render(request, 'library/studentaddbook.html', {'note1': 'Not Found Sunch Type of Book', 'objp':objp})
            elif sbtn == 'auth':
                obj12 = Book.objects.filter(author__icontains=item)
                if len(obj12)>0:
                    print("kahua")
                    return render(request, 'library/studentaddbook.html', {'obj12': obj12, 'objp':objp})
                else:
                    return render(request, 'library/studentaddbook.html', {'note1': 'Not Found Sunch Type of Book', 'objp':objp})
            elif sbtn == 'sub':
                obj12 = Book.objects.filter(subject__icontains=item)
                if len(obj12)>0:
                    return render(request, 'library/studentaddbook.html', {'obj12': obj12, 'objp':objp})
                else:
                    return render(request, 'library/studentaddbook.html', {'note1': 'Not Found Sunch Type of Book', 'objp':objp})
        except:
            return render(request, 'library/studentaddbook.html',{'objp':objp})
    return render(request, 'library/studentaddbook.html',{'objp':objp})

def bookissue(request):
    if not request.user.is_authenticated :
        return render(request,'library/index.html')
    if request.method=='POST':
        uname=request.POST.get('uname')
        bookid=request.POST.get('id')
        sub = request.POST.get('subject')
        title = request.POST.get('title')
        author = request.POST.get('author')
        if bookid and sub and title and author is not None:
            try:
                obj = IssueBook.objects.filter(Q(user=uname) , Q(bookid=bookid))
                if len(obj)>0:
                    return render(request, 'library/studentaddbook.html',{'note':'Already Issued'})
                else:
                    ob=IssueBook(
                        bookid=bookid,
                        user=uname,
                        title=title,
                        author=author,
                        subject=sub,
                        issuedate=date.today()
                    )
                    ob.save()
                    obj1 = Book.objects.get(Q(bookid=bookid))
                    q=int(obj1.quantity)
                    if q==1:
                        obj1.delete()
                        return render(request, 'library/studentaddbook.html',{'note': 'Book Issued Successfullly.....'})
                    else:
                        Book.objects.filter(bookid=bookid).update(quantity=int(obj1.quantity)-1)
                        return render(request, 'library/studentaddbook.html', {'note': 'Book Issued Successfullly.....'})
            except:
                ob = IssueBook(
                    bookid=bookid,
                    user=uname,
                    title=title,
                    author=author,
                    subject=sub
                )
                ob.save()
                return render(request, 'library/studentaddbook.html', {'note': 'Book Issued Successfullly.....'})
        return render(request, 'library/studentaddbook.html')

def issuedbook(request):
    if not request.user.is_authenticated :
        return render(request,'library/index.html')
    uname=request.POST.get('uname')
    objp = Post.objects.all()
    if request.method=='POST':
        if uname is not None:
            try:
                today=date.today()- timedelta(days=7)
                ob=IssueBook.objects.filter(Q(issuedate__lte=today),Q(user=uname))
                obj12 =IssueBook.objects.filter(Q(issuedate__gt=today),Q(user=uname))
                if len(obj12)>0 or len(ob)>0:
                    return render(request, 'library/issuedbook.html', {'obj12':obj12, 'objp':objp, 'ob':ob})
                else:
                    return render(request, 'library/issuedbook.html', {'note':'No Any Book Issued','ob':ob})
            except:
                return render(request, 'library/issuedbook.html',{'ob':ob})
        return render(request, 'library/issuedbook.html')
    return render(request, 'library/issuedbook.html')

def returnbook(request):
    if not request.user.is_authenticated :
        return render(request,'library/index.html')
    uname = request.POST.get('uname')
    bookid=request.POST.get('id')
    title=request.POST.get('title')
    author=request.POST.get('author')
    subject=request.POST.get('subject')
    if request.method=='POST':
        if uname and bookid is not None:
            try:
                obj12 = IssueBook.objects.filter(Q(user=uname),Q(bookid=bookid))
                obj12.delete()
                try:
                    obj1 = Book.objects.get(Q(bookid=bookid))
                    Book.objects.filter(bookid=bookid).update(quantity=obj1.quantity + 1)
                except:
                    ob = Book(
                        bookid=bookid,
                        title=title,
                        content='This is Nice Book',
                        quantity=1,
                        author=author,
                        subject=subject
                    )
                    ob.save()
                obj13 = IssueBook.objects.filter(Q(user=uname))
                if len(obj13) > 0:
                    return render(request, 'library/issuedbook.html',{'obj12': obj13, 'note': 'Your Book Successfully Returned...'})
                else:
                    return render(request, 'library/issuedbook.html', {'note': 'No Any Book Issued'})
            except:
                return render(request, 'library/issuedbook.html')
        return render(request, 'library/issuedbook.html')
    return render(request, 'library/issuedbook.html')

def requestbook(request):
    if not request.user.is_authenticated :
        return render(request,'library/index.html')
    objp = Post.objects.all()
    if request.method=='POST':
        uname=request.POST.get('uname')
        title =request.POST.get('title')
        content=request.POST.get('content')
        today = date.today()
        if uname and title and content is not None:
            obj=Notice(
                content=content,
                title=title,
                date_posted=today,
                user=uname
            )
            obj.save()
            return render(request, 'library/requestbook.html',{'note':'Your Request Has Posted....', 'objp':objp})
    return render(request, 'library/requestbook.html',{'objp':objp})

def booklist(request):
    if request.session.get('name') is not None:
        sbtn = request.POST.get('result')
        item = request.POST.get('searchbook')
        if sbtn and item is not None:
            try:
                if sbtn == 'tit':
                    obj= Book.objects.filter(Q(title__icontains=item))
                    if len(obj) > 0:
                        return render(request, 'library/booklist.html', {'obj': obj})
                    else:
                        return render(request, 'library/booklist.html', {'note1': 'Not Found Sunch Type of Book'})
                elif sbtn == 'auth':
                    obj = Book.objects.filter(author__icontains=item)
                    if len(obj) > 0:
                        return render(request, 'library/booklist.html', {'obj': obj})
                    else:
                        return render(request, 'library/booklist.html', {'note1': 'Not Found Sunch Type of Book'})
                elif sbtn == 'sub':
                    obj = Book.objects.filter(subject__icontains=item)
                    if len(obj) > 0:
                        return render(request, 'library/booklist.html', {'obj': obj})
                    else:
                        return render(request, 'library/booklist.html', {'note1': 'Not Found Sunch Type of Book'})
            except:
                obj = Book.objects.all()
                return render(request, 'library/booklist.html', {'obj': obj})
        obj=Book.objects.all();
        return render(request, 'library/booklist.html',{'obj':obj})
    return render(request, 'library/index.html')

def removebynumber(request):
    if request.method=='POST':
        uname=request.session.get('name')
        bookid=request.POST.get('bookids')
        num=request.POST.get('num')
        try:
            obj1 = Book.objects.get(Q(bookid=bookid))
            val=obj1.quantity
            Book.objects.filter(bookid=bookid).update(quantity=int(val) + int(num))
            obj = Admin.objects.get(Q(username=request.session.get('name')))
            msg = str(str(num) + '  Book Added Successfully....')
            return render(request, 'library/adminpage.html',{'val': obj.count + 10, 'rval': obj.rcount + 10, 'eval': obj.ecount + 10,'pval': obj.pcount + 10,'note':msg})
        except:
            return render(request, 'library/adminpage.html')
    return render(request, 'library/adminpage.html')


def deletebynumber(request):
    if request.method == 'POST':
        bookid = request.POST.get('bookidd')
        num = int(request.POST.get('numd'))
        try:
            print("1")
            print(bookid)
            obj1 = Book.objects.get(Q(bookid=bookid))
            val = int(obj1.quantity)
            if num>val:
                print("2")
                obj = Admin.objects.get(Q(username=request.session.get('name')))
                return render(request, 'library/adminpage.html',{'val': obj.count + 10, 'rval': obj.rcount + 10, 'eval': obj.ecount + 10, 'pval': obj.pcount + 10, 'note': 'You cannot Remove.... '})
            elif num == val:
                print("3")
                obj12 = Admin.objects.get(Q(username=request.session.get('name')))
                val1=int(obj12.rcount)
                print("3a")
                Admin.objects.filter(Q(username=request.session.get('name'))).update(rcount=val1 + 1)
                obj = Admin.objects.get(Q(username=request.session.get('name')))
                obj1.delete()
                return render(request, 'library/adminpage.html',{'val': int(obj.count) + 10, 'rval': int(obj.rcount) + 10, 'eval': int(obj.ecount) + 10, 'pval': int(obj.pcount) + 10,'note': 'Removed Book From Library.... '})
            else:
                Book.objects.filter(bookid=bookid).update(quantity=int(val) - int(num))
                obj = Admin.objects.get(Q(username=request.session.get('name')))
                msg= str(str(num) + '  Book Removed Successfully....')
                return render(request, 'library/adminpage.html',{'val': obj.count + 10, 'rval': obj.rcount + 10, 'eval': obj.ecount + 10, 'pval': obj.pcount + 10, 'note': msg})
        except:
            print("4")
            return render(request, 'library/adminpage.html')
    return render(request, 'library/adminpage.html')

def deletepost(request):
    try:
        obj=Post.objects.filter(Q(author=request.session.get('name')))
        if len(obj)>0:
            return render(request, 'library/deletepost.html', {'obj':obj})
        else:
            return render(request, 'library/deletepost.html', {'note': 'No Any Notice Has Been Post Yet....'})
    except:
        return render(request, 'library/deletepost.html', {'note':'No Any Notice Has Been Post Yet....'})

def deletepostbypopup(request):
    if not request.user.is_authenticated :
        return render(request,'library/index.html')
    if request.method=='POST':
        title=request.POST.get('notice')
        try:
            obj = Post.objects.filter(Q(author=request.session.get('name')),Q(title=title))
            obj.delete()
            obj2 = Admin.objects.get(Q(username=request.session.get('name')))
            val=int(obj2.pcount)
            Admin.objects.filter(username=request.session.get('name')).update(pcount=val - 1)
            try:
                obj1 = Post.objects.filter(Q(author=request.session.get('name')))
                if obj1 is not None:
                    return render(request, 'library/deletepost.html', {'obj': obj1,'note':'Your Post Successfully Removed'})
            except:
                return render(request, 'library/deletepost.html', {'note': 'No Any Notice Has Been Post Yet....'})
        except:
            return render(request, 'library/deletepost.html')
    return render(request,'library/deletepost.html')



def verifyrequest(request):
    try:
        obj=Notice.objects.filter(Q(verify=False))
        if len(obj)>0:
            print("hijsdfhf")
            return render(request, 'library/verifyrequest.html',{'obj': obj })
        else:
            return render(request, 'library/verifyrequest.html', {'note': 'No Any Request Has Been Post Yet....'})
    except:
        return render(request, 'library/verifyrequest.html',{'note':'No Any Request Has Been Post Yet....'})
    return render(request, 'library/verifyrequest.html',{'note':'No Any Request Has Been Post Yet....'})


def studentrequest(request):
    if request.method=='POST':
        btn=request.POST.get('req')
        title=request.POST.get('title')
        std=request.POST.get('author')
        if btn=='rr':
            Notice.objects.filter(Q(user=std),Q(title=title)).update(verify=True,status=False)
            return render(request, 'library/verifyrequest.html',{'note':'Request Has been Rejected...'})
        if btn=='ar':
            Notice.objects.filter(Q(user=std), Q(title=title)).update(verify=True, status=True)
            return render(request, 'library/verifyrequest.html', {'note': 'Request Has been Approved...'})
    return render(request, 'library/verifyrequest.html')

def statusrequest(request):
    if not request.user.is_authenticated :
        return render(request,'library/index.html')
    user=request.user
    objp = Post.objects.all()
    try:
        obj = Notice.objects.filter(Q(user=user),Q(status=True),Q(verify=True))
        print(len(obj))
        obj1 = Notice.objects.filter(Q(user=user),Q(status=False),Q(verify=True))
        print(len(obj1))
        if len(obj)>0 and  len(obj1)>0:
            print("hiisdd")
            return render(request,'library/statusrequest.html',{'obj':obj,'obj1':obj1, 'objp':objp})
        else:
            if len(obj)==0 and len(obj1)>0:
                return render(request, 'library/statusrequest.html', {'obj1': obj1, 'objp':objp})
            if len(obj1)==0 and len(obj)>0:
                return render(request, 'library/statusrequest.html', {'obj': obj, 'objp':objp})
    except:
        return render(request, 'library/statusrequest.html', {'note': 'No Any request has Posted...', 'objp':objp})
    return render(request, 'library/statusrequest.html', {'note': 'No Any request has Posted...', 'objp':objp})
def deleterequest(request):
    if not request.user.is_authenticated :
        return render(request,'library/index.html')
    if request.method=='POST':
        user = request.user
        title=request.POST.get('title')
        try:
            obj3 = Notice.objects.filter(Q(user=user), Q(title=title))
            obj3.delete()
            obj = Notice.objects.filter(Q(user=user), Q(status=True), Q(verify=True))
            obj1 = Notice.objects.filter(Q(user=user), Q(status=False), Q(verify=True))
            if obj is not None and obj1 is not None:
                print("1")
                return render(request, 'library/statusrequest.html', {'obj': obj, 'obj1': obj1, 'note':'Request Deleted Successfully...'})
            else:
                print("2")
                if obj is None and obj1 is not None:
                    print("3")
                    return render(request, 'library/statusrequest.html', {'obj1': obj1,'note':'Request Deleted Successfully...'})
                if obj1 is None and obj is not None:
                    print("4")
                    return render(request, 'library/statusrequest.html', {'obj': obj,'note':'Request Deleted Successfully...'})
                return render(request, 'library/statusrequest.html')
        except:
            return render(request, 'library/statusrequest.html', {'note': 'No Any request has Posted...'})
    return render(request, 'library/statusrequest.html')


def payfine(request):
    if not request.user.is_authenticated :
        return render(request,'library/index.html')
    user=request.user
    objp = Post.objects.all()
    try:
        today = date.today() - timedelta(days=7)
        ob = IssueBook.objects.filter(Q(issuedate__lte=today), Q(user=user))
        if len(ob)>0:
            total =10
            total=total*len(ob)
            return render(request,'library/payfine.html',{'objp':objp, 'ob':ob, 'total':total})
        else:
            return render(request, 'library/payfine.html', {'objp': objp, 'note':'No Any Fine In Your Id'})
    except:
        return render(request, 'library/payfine.html', {'objp': objp, 'note': 'No Any Fine In Your Id'})


