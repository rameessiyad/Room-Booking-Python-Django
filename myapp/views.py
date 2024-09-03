from django.shortcuts import render,redirect
from myapp.models import vowner
from myapp.models import staff
from myapp.models import Userreg
from myapp.models import roomtype
from myapp.models import room, bsub, booking, temp, temp1
import pyttsx3

from datetime import datetime, timedelta, date
from django.db.models.functions import Coalesce
from django.db.models import Sum
from django.db.models import Max,Value
from django.db.models import F

# Create your views here.

def index(request):
    return render(request,"index.html")


def userregistration(request):
    if request.method=="POST":
        usname = request.POST.get('usname')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        idproof = request.FILES['idproof']
        photo = request.FILES['photo']
        uname = request.POST.get('uname')
        pword = request.POST.get('pword')
        us = Userreg(usname=usname, email=email, mobile=mobile, idproof=idproof, photo=photo, uname=uname, pword=pword)
        us.save()
        return redirect("/h/")
    return render(request,"userreg.html")

def staffregistration(request):
    if request.method=="POST":
        sname = request.POST.get('sname')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        photo = request.FILES['photo']
        uname = request.POST.get('uname')
        pword = request.POST.get('pword')
        ss = staff(sname=sname, email=email, mobile=mobile, photo=photo, uname=uname, pword=pword)
        ss.save()
        return redirect("/h/")
    return render(request, "staffreg.html")

def taxiregistration(request):
    if request.method=="POST":
        owname = request.POST.get('owname')
        mobile = request.POST.get('mobile')
        photo = request.FILES['photo']
        vname = request.POST.get('vname')
        vnumber = request.POST.get('vnumber')
        vphoto = request.FILES['vphoto']
        mincharge = request.POST.get('mincharge')
        rate = request.POST.get('rate')
        uname = request.POST.get('uname')
        pword = request.POST.get('pword')
        sa=vowner(owname=owname, mobile=mobile, photo=photo, vname=vname, vnumber=vnumber, vphoto=vphoto, mincharge=mincharge, rate=rate, uname=uname, pword=pword)
        sa.save()
        return redirect("/h/")
    return render(request, "taxireg.html")

def login(request):
    if request.method == "POST":
        u = request.POST.get('u')
        p = request.POST.get('p')
        found = 0
        vrec = vowner.objects.filter(uname = u, pword = p)
        if vrec.exists():
            found = 1
            for j in vrec:
                name=j.owname
                id=j.id
                phone=j.mobile
                status = j.status
        if found == 0:
            vrec = staff.objects.filter(uname = u, pword = p)
            if vrec.exists():
                found = 1
                for j in vrec:
                    name=j.sname
                    id=j.id
                    phone=j.mobile
                    status = j.status
        if found == 0:
            vrec = Userreg.objects.filter(uname = u, pword = p)
            if vrec.exists():
                found = 1
                for j in vrec:
                    name=j.usname
                    id=j.id
                    phone=j.mobile
                    status = j.status

        if found == 0:
            engine = pyttsx3.init()
            msg = "Sorry invalid user"
            engine.say(msg)
            engine.runAndWait()
        else :
            request.session['id'] = id
            request.session['name'] = name
            request.session['uname'] = u
            request.session['pword'] = p
            request.session['phone'] = phone
            request.session['status'] = status

            if status == "admin":
                return redirect("/sap/")
            elif status == "User":
                temp.objects.all().delete()
                temp1.objects.all().delete()
                return redirect("/sup/")
            elif status == "owner":
                return redirect("/sop/")
            elif status == "staff":
                return redirect("/ssp/")
            elif status == "NT" or status == "NS":
                engine = pyttsx3.init()
                msg = "Plese wait for approval"
                engine.say(msg)
                engine.runAndWait()
            else :
                engine = pyttsx3.init()
                msg = "Sorry, rejected"
                engine.say(msg)
                engine.runAndWait()



    return render(request, "login.html")



def showvehicleownerpage(request):
    return render(request, "taxipage.html")

def showstaffpage(request):
    book = booking.objects.count()
    rooms = room.objects.count()
    rmtypes = roomtype.objects.count()
    return render(request, "staffpage.html", {"book": book, "rooms": rooms, "rmtypes": rmtypes})

def showuserpage(request):
    rec = roomtype.objects.all()
    return render(request, "userpage.html",{"rec":rec})

def showadminpage(request):
    rooms = room.objects.count()
    staffs = staff.objects.filter(status = 'staff').count()
    rmtype = roomtype.objects.count()
    return render(request, "admin.html", {"rooms": rooms, "staffs": staffs, "rmtype": rmtype})

def staffapproval(request):
    srec = staff.objects.filter(status = 'NS')
    return render(request, "staffapproval.html", {"srec":srec})

def staffapprove(request,id):
    staff.objects.filter(id=id).update(status='staff')
    return redirect("/sapp")



def staffreject(request,id):
    staff.objects.filter(id=id).update(status='rejected')
    return redirect("/sapp")

def taxiapproval(request):
    trec = vowner.objects.filter(status = 'NT')
    return render(request, "taxiapprovals.html", {"trec":trec})

def taxiapprove(request,id):
    vowner.objects.filter(id=id).update(status='taxi')
    return redirect("/tapp")

def taxirejct(request,id):
    vowner.objects.filter(id=id).update(status='reject')
    return redirect("/tapp")

def addroom(request):
    rec = roomtype.objects.all()

    if request.method == "POST":
        rno = request.POST.get('rno')
        rt = request.POST.get('rt')
        sr = room(rno=rno, rt=rt)
        sr.save()
        return redirect("/addroom/")
    return render(request, "addroom.html", {"rec":rec})

def addroomtype(request):
    if request.method == "POST":
        rmtype = request.POST.get('rmtype')
        nobeds = request.POST.get('nobeds')
        photo = request.FILES['photo']
        rate = request.POST.get('rate')
        rt = roomtype(rmtype=rmtype, nobeds=nobeds, photo=photo, rate=rate)
        rt.save()
        return redirect("/rtype/")
    return render(request, "roomcategory.html")

def editroomtype(request,id):
    rec=roomtype.objects.filter(id=id)
    for j in rec:
        rmtype=j.rmtype
        nobeds=j.nobeds
        rate=j.rate
    if request.method == "POST":
        rmtype = request.POST.get('rmtype')
        nobeds = request.POST.get('nobeds')
        rate = request.POST.get('rate')
        roomtype.objects.filter(id=id).update(rmtype=rmtype, nobeds=nobeds, rate=rate)

        return redirect("/vroom/")
    return render(request, "editroomtype.html",{"rmtype":rmtype,"nobeds":nobeds,"rate":rate})

def deleteroom(request,id):
    rec=roomtype.objects.filter(id=id)
    for j in rec:
        rmtype=j.rmtype
    srec=room.objects.filter(rt=rmtype)
    if srec.exists():
        engine = pyttsx3.init()
        msg = "Room exists in that room type"
        engine.say(msg)
        engine.runAndWait()
        pass
    else:
        roomtype.objects.filter(id=id).delete()
    return redirect("/vroom/")

def viewrooms(request):
    srec = roomtype.objects.all()
    return render(request, "viewrooms.html", {"srec":srec})

def listrooms(request):
    srec = room.objects.all()
    return render(request, "listrooms.html",{"srec": srec})

def edroom(request,id):
    srec = room.objects.filter(id=id)
    rec = roomtype.objects.all()
    for j in srec:
        rno=j.rno
        rt=j.rt
    if request.method == "POST":
        rno = request.POST.get('rno')
        rt = request.POST.get('rt')
        room.objects.filter(id=id).update(rno=rno, rt=rt)

        return redirect("/veiwroom/")
    return render(request, "editroom.html", {"rno": rno, "rt": rt, "rec":rec})

def delroom(request,id):
    return redirect('/veiwroom/')

def roomtables(request):

    return render(request, "roomtable.html",)


def bookingform(request,id):
    if request.method == "POST":
        indate = request.POST.get('indate')
        outdate = request.POST.get('outdate')
        rmtype = request.POST.get('rtype')
        nop = request.POST.get('nop')
        request.session['indate'] = indate
        request.session['outdate'] = outdate
        request.session['nop'] = nop
        date_format = "%Y-%m-%d"
        a = datetime.strptime(str(outdate),date_format)
        b = datetime.strptime(str(indate), date_format)
        delta = a-b
        diff = int(delta.days)

        request.session['days'] = diff

        count = bsub.objects.filter(bdate__range = (b,a), rtype = rmtype).count()
        if count>0:
            brec = bsub.objects.filter(bdate__range=(b,a), rtype=rmtype)
            arr = []

            for j in brec:
                arr.append(j.rno)

            rrec = room.objects.exclude(rno__in = arr) & room.objects.filter(rt = rmtype)

        else:
            rrec = room.objects.filter(rt=rmtype)
        temp.objects.all().delete()
        temp1.objects.all().delete()

        for j in rrec:
            sa = temp(rno = j.rno)
            sa.save()


        return render(request, "roomtable.html",{"rrec": rrec})



    rec = roomtype.objects.filter(id=id)
    for j in rec:
        rmtype = j.rmtype
    request.session['roomid'] = id
    request.session['roomtype'] = rmtype
    return render(request, "bookingform.html",{"rmtype":rmtype})

def pickroom(request,rno):
    ta = temp1(rno = rno)
    ta.save()
    temp.objects.filter(rno = rno).delete()
    rrec = temp.objects.all()
    trec1 = temp1.objects.all()
    return render(request, "roomtable.html", {"rrec": rrec, "trec1": trec1})

def deleteroom(request,rno):
    ta = temp(rno = rno)
    ta.save()
    temp1.objects.filter(rno = rno).delete()
    rrec = temp.objects.all()
    trec1 = temp1.objects.all()
    return render(request, "roomtable.html", {"trec1": trec1, "rrec": rrec})

def pay(request):
    bdate = date.today()
    name = request.session['name']
    nop = request.session['nop']
    rmtype = request.session['roomtype']
    indate = request.session['indate']
    outdate = request.session['outdate']
    id = request.session['roomid']
    uid = request.session['id']
    rent=0
    rec = roomtype.objects.filter(id = id)

    for j in rec:
        rent = j.rate
    days = request.session['days']
    rms=[]
    trec = temp1.objects.all()
    no=0
    for j in trec:
       rms.append( j.rno)
       no=no+1
    tc = rent * no * days

    if request.method == "POST":
            card = request.POST.get('card')
            max_bno = booking.objects.aggregate(max_bno=Coalesce(Max('bno'), Value(0)))['max_bno']
            bno = int(max_bno) + 1
            bs = booking(bno=bno, bdate=bdate, custid=uid, custname=name, nop=nop, rtype=rmtype, datef=indate, dateto=outdate , nod=days, totamt=tc, cardno=card)
            bs.save()
            trec = temp1.objects.all()
            date_format = "%Y-%m-%d"
            a = datetime.strptime(str(indate), date_format)
            for j in trec:
                rno = j.rno
                for m in range(0,days + 1):
                    bdate = a + timedelta(m)
                    sa = bsub(bno=bno, bdate=bdate, rtype=rmtype, rno=rno)
                    sa.save()
            temp.objects.all().delete()
            temp1.objects.all().delete()
            return redirect('/sup/')
    return render(request, "payment.html",{"bdate":bdate, "name": name,"uid":uid, "nop": nop, "rmtype": rmtype, "indate": indate, "outdate": outdate, "rent":rent, "rms":rms, "tc":tc, "days":days })

def mybookings(request):
    uid = request.session['id']
    brec = booking.objects.filter(custid=uid)
    return render(request, "mybookings.html", {"brec": brec})


def viewmore(request,bno):
    brec = bsub.objects.filter(bno=bno)
    return render(request, "viewmore.html",{"brec":brec})

def delroom(request,bno):
    booking.objects.filter(bno=bno).delete()
    bsub.objects.filter(bno=bno).delete()

    return redirect('/mybk/')

def allrooms(request):
    trec = room.objects.all()
    return render(request, "allrooms.html", {"trec": trec})

def roombookings(request):
    trec = booking.objects.all()
    return render(request, "roombookings.html", {"trec": trec})

