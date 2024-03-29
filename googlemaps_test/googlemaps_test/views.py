from django.shortcuts import render
import pyrebase
from django.contrib import auth
import firebase_admin
from firebase_admin import credentials


config = {
  "apiKey": "AIzaSyCXUHehoI2eEBpdi-qsZBl9RNqmvvxOE6s",
    "authDomain": "covid19-3c098.firebaseapp.com",
    "databaseURL": "https://covid19-3c098.firebaseio.com",
    "projectId": "covid19-3c098",
    "storageBucket": "covid19-3c098.appspot.com",
    "messagingSenderId": "382651925275",
    "appId": "1:382651925275:web:34664edb887b98755549be",
    "measurementId": "G-768V96RMJ5",
  "serviceAccount": "C://users//bhavs//desktop//django projects//googlemaps_test//googlemaps_test//covid19-3c098-firebase-adminsdk-7aplu-ba7fee86a8.json"
}
firebase= pyrebase.initialize_app(config)
authe=firebase.auth()
database=firebase.database()

cred = credentials.Certificate("C://users//bhavs//desktop//django projects//googlemaps_test//googlemaps_test//covid19-3c098-firebase-adminsdk-7aplu-ba7fee86a8.json")
base=firebase_admin.initialize_app(cred)

def home(request):
    return render(request,'user/base.html')

def signIn(request):
	return render(request,'signIn.html')

def postsign(request):
	email=request.POST.get('email')
	passw = request.POST.get("pass")
	try:
		user = authe.sign_in_with_email_and_password(email,passw)
	except:
		message = "invalid cerediantials"
		return render(request,"signIn.html",{"msg":message})
	print(user['idToken'])
	session_id=user['idToken']
	request.session['uid']=str(session_id)
	return render(request, "welcome.html",{"e":email})

def logout(request):
    auth.logout(request)
    return render(request,'signIn.html')

def signUp(request):
	return render(request,"signup.html")

def postsignup(request):

    name=request.POST.get('name')
    email=request.POST.get('email')
    passw=request.POST.get('pass')
    user=authe.create_user_with_email_and_password(email,passw)
    uid = user['localId']
    data={"name":name,"status":"1"}
    database.child("users").child(uid).child("details").set(data)
    try:
        user=authe.create_user_with_email_and_password(email,passw)
    except:
        message="Unable to create account try again"
        return render(request,"signup.html",{"messg":message})
    uid = user['localId']
    data={"name":name,"status":"1"}
    database.child("users").child(uid).child("details").set(data)
    return render(request,"signIn.html")

def create(request):

    return render(request,'create.html')


def post_create(request):

    import time
    from datetime import datetime, timezone
    import pytz

    tz= pytz.timezone('Asia/Kolkata')
    time_now= datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    print("mili"+str(millis))
    work = request.POST.get('work')
    progress =request.POST.get('progress')
    url = request.POST.get('url')
    idtoken= request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    print("info"+str(a))
    data = {
        "work":work,
        'progress':progress,
        'url':url
    }
    database.child('users').child(a).child('reports').child(millis).set(data)
    name = database.child('users').child(a).child('details').child('name').get().val()
    return render(request,'welcome.html', {'e':name})

def check(request):
    import datetime
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    timestamps = database.child('users').child(a).child('reports').shallow().get().val()
    lis_time=[]
    for i in timestamps:

        lis_time.append(i)

    lis_time.sort(reverse=True)

    print(lis_time)
    work = []

    for i in lis_time:

        wor=database.child('users').child(a).child('reports').child(i).child('work').get().val()
        work.append(wor)
    print(work)

    date=[]
    for i in lis_time:
        i = float(i)
        dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
        date.append(dat)

    print(date)

    comb_lis = zip(lis_time,date,work)
    name = database.child('users').child(a).child('details').child('name').get().val()

    return render(request,'check.html',{'comb_lis':comb_lis,'e':name})

def post_check(request):

    import datetime

    time = request.GET.get('z')

    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    work =database.child('users').child(a).child('reports').child(time).child('work').get().val()
    progress =database.child('users').child(a).child('reports').child(time).child('progress').get().val()
    img_url = database.child('users').child(a).child('reports').child(time).child('url').get().val()
    print(img_url)
    i = float(time)
    dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
    name = database.child('users').child(a).child('details').child('name').get().val()

    return render(request,'post_check.html',{'w':work,'p':progress,'d':dat,'e':name,'i':img_url})