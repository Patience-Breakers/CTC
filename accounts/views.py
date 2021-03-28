# Create your views here.
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
import re
from datetime import date
from bs4 import BeautifulSoup
import requests
# from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from .models import Student, Teacher, Course, Lecture, Watch_time
from .forms import StudentForm
# import collections
from .models import Teacher

def index(request):
    return render(request, 'index.html')

def blank(request):
    return render(request, 'blank.html')

def dashboard(request):
    return render(request, 'dashboard.html')


#crawler ka funciton
def crawler(request):
    if request.method == 'POST':
        query = request.POST['query']
        page = requests.get(f"https://www.google.com/search?q={query}&num={5}")
        soup = BeautifulSoup(page.content, "html.parser")
        links = soup.findAll("a")
        name = soup.find_all('h3')
        c = 0
        #print([n.getText() for n in name])
        results = []
        print(len(name), len(links))
        #print(list(zip(name,links)))
        for link in links:
            link_href = link.get('href')
            if "url?q=" in link_href and not "webcache" in link_href:

                res = link.get('href').split("?q=")[1].split("&sa=U")[0]
                results.append(res)
                c += 1
            if c > 5:
                break
        # page = requests.get(f"https://www.google.com/search?q={query}&num={5}")
        # soup = BeautifulSoup(page.content, "html.parser")
        # links = soup.findAll("a")
        # res = 0
        # results = {}
        # for link in links:
        #     per_res = {}
        #     link_href = link.get('href')
        #     if "url?q=" in link_href and not "webcache" in link_href:
        #         #per_res.update("Inner Text ={}.format(link.text))
        #         if link.get('title'):
        #           per_res.update({"Title ":link.get("title")})
        #         if link.parent.get("id"):
        #           per_res.update({"Name " :link.parent.get("id")})
        #         per_res.update({"Link":link.get('href').split("?q=")[1].split("&sa=U")[0]})
        #         res += 1
        #     results.update(per_res)
        #     if res > 5:
        #         break
        print(results)
        context = {'results': results}
        return render(request, 'crawlerResult.html', context)


def calendar(request):
    # return render(request, 'calendar.html')
    pass


def assignments(request):
    return render(request, 'assignments.html')


def grades(request):
    return render(request, 'grades.html')


def teachers(request):
    tech = Teacher.objects.all()
    return render(request, 'teachers.html', {'tech': tech})


def classnotes(request):
    return render(request, 'classnotes.html')


def allstudents(request):
    students = Student.objects.all()
    context = {
        'students': students,
    }
    return render(request, 'allstudents.html', context)


#open student aka dashboard
def openstudent(request, studentid):    
    student = Student.objects.get(pk=studentid)
    courses = student.courses.all()
    # lectids = []
    # for lect in lectures:
    #     lectids.append(lect.pk)
    # watchtimelist = []
    # for watch in mywatch_time:
    #     if watch.w_lect.pk in lectids:
    #         watchtimelist.append(watch)
    # completed=[]
    # for course in courses
    print(courses)
    mylist=[]
    for course in courses :      
        myteacher = Teacher.objects.get(course__pk=course.pk)
        lectures = Lecture.objects.filter(teacher__pk=myteacher.pk)
        lect_counter = 0
        watch_counter=0
        for lect in lectures:
          lect_counter+=1
          mywatch_time = Watch_time.objects.filter(student__pk=studentid).filter(
              w_lect__pk=lect.pk)
          for watch in mywatch_time:
            if watch.completed==True:
              watch_counter+=1
        mylist.append(int((watch_counter/lect_counter)*100))
    graphlist=[]
    sum=0
    for list in mylist:
        sum = sum+list
    for list in mylist:
      if sum!=0:
        graphlist.append((list/sum*100))      
      else :
        graphlist.append(0) 
    # completed=[]
    # for course in courses:
    myfile = zip(mylist, courses)
    context = {
        'student': student,
        'myfile' : myfile,
        'mylist' : mylist,
        'courses':courses,
        'course':courses[0].course_name,
        'graphlist' : graphlist,
    }
    return render(request, 'studentPage.html', context)


def handlelogin(request):
    # student = Student.objects.get(pk=studentid)
    #   courses = student.courses.all()
    #   context = {
    #       'student': student,
    #       'courses': courses,
    #   }
    #   return render(request, 'studentPage.html', context)
    if request.method == 'POST':
        lusername = request.POST['username']
        lpassword = request.POST['password']
        #   # students = authenticate(username=lusername,password=lpassword)
        student = Student.objects.filter(username=lusername).filter(
            password=lpassword)

        if student is not None:

            studentid = student[0].pk
            str_pass = '/students/' + str(studentid)
            return redirect(str_pass)
        else:
            return redirect('/')

    return render(request, 'login.html')


def handlelogout():
    pass


def openLectlistfromstudent(request, studentid, courseid):
    course = Course.objects.get(pk=courseid)
    myteacher = Teacher.objects.get(course__pk=courseid)
    lectures = Lecture.objects.filter(teacher__pk=myteacher.pk)
    mywatch_time = Watch_time.objects.filter(student__pk=studentid)
    lectids = []
    for lect in lectures:
        lectids.append(lect.pk)
    watchtimelist = []
    for watch in mywatch_time:
        if watch.w_lect.pk in lectids:
            watchtimelist.append(watch)

    # mywatch_time = Watch_time.objects.filter(student__pk=studentid).filter(w_lect__pk=lectid)
    mylist = zip(lectures, watchtimelist)
    context = {
        # 'lectures' :lectures,
        'mylist': mylist,
        'student' : Student.objects.get(pk=studentid),
        'studentid': studentid,
        'course': course,
    }

    for i in watchtimelist:
        print("#####################", i.completed,i.student, "#####################")

    # mylist = zip(bed_lists, newbedlist)
    #         context = {'mylist': mylist,}
    # return render(request, 'bedavalibility.html', context)
    # {% for a,b in mylist %}
    return render(request, 'opencoursefromstudent.html', context)


def openLecturefromstudent(request, studentid, courseid, lectid):
    if request.method == 'POST':
        rating = request.POST['rating']
        mywatch_time = Watch_time.objects.filter(student__pk=studentid).filter(
            w_lect__pk=lectid)
        for watch in mywatch_time:
            watch.Rating=rating
            watch.save()
            # redirect(openLecturefromstudent,
            #         studentid=studentid,
            #         courseid=courseid,
            #         lectid=new_lecture.pk)
        return redirect(openLecturefromstudent, studentid=studentid,courseid=courseid,
                    lectid=lectid)
    else:
        myteacher = Teacher.objects.get(course__pk=courseid)
        lecture = Lecture.objects.filter(teacher__pk=myteacher.pk).get(
            pk=lectid)
        course = Course.objects.get(pk=courseid)
        student = Student.objects.get(pk=studentid)
        lecture = Lecture.objects.get(pk=lectid)
        
        mywatch_time = Watch_time.objects.filter(student__pk=studentid).filter(
            w_lect__pk=lectid)
       

        # iscomplete = mywatch_time.completed
        # lecture =
        context = {
            'lecture': lecture,
            'student': student,
            'course': course,
            'Watch_time': mywatch_time,
        }
        return render(request, 'openLecturefromstudent.html', context)


def nextlect(request, studentid, courseid, lectid):
    #  mywatch_time = Watch_time.objects.filter(student__pk=studentid).get(w_lect__pk=lectid)
    # mywatch_time = Watch_time.objects.filter(student__pk=studentid).filter(
        # w_lect__pk=lectid)

    # mywatch_time[0].completed = 'True'
    # mywatch_time[0].completed_date = date.today()
    # lecture = Lecture.objects.get(pk=lectid)
    # watchtimelist=[]
    # for watch in mywatch_time:
    #     if watch.w_lect.pk in lecture:
    #         watch.completed='True'
    #         watchtimelist.append(watch)
    # print("#####################",mywatch_time,"#####################")
    course = Course.objects.get(pk=courseid)
    myteacher = Teacher.objects.get(course__pk=courseid)
    lectures = Lecture.objects.filter(teacher__pk=myteacher.pk)
    # mywatch_time = Watch_time.objects.filter(student__pk=studentid)
    new_lecture = None
    flag = 0
    for lect in lectures:
      if lect.pk==lectid:
        flag=1
        continue
      if flag==1:          
        new_lecture = lect
        break
    # lectids = []
    # for lect in lectures:
    #     lectids.append(lect.pk)

    if new_lecture is not None:
      return redirect(openLecturefromstudent,
                    studentid=studentid,
                    courseid=courseid,
                    lectid=new_lecture.pk)
    else:
      return redirect(openLectlistfromstudent,
                    studentid=studentid,
                    courseid=courseid)
    # course = Course.objects.get(pk=courseid)
    # student = Student.objects.get(pk=studentid)
    # lecture = Lecture.objects.get(pk=lectid)
    # myteacher = Teacher.objects.get(course__pk = courseid)
    # new_lecture = Lecture.objects.get(pk=lectid+1)
    # mywatch_time = Watch_time.objects.filter(student__pk=studentid).filter(w_lect__pk=lectid+1)
    # 
    #   # context = {
    #   #     'lecture': new_lecture,
    #   #     'student': student,
    #   #     'course': course,
    #   #     'Watch_time': mywatch_time,
    #   # }
    #   return render(request, 'openLecturefromstudent.html', context)
    # return HttpResponse('students/<int:studentid>/courses/<int:courseid>/lecture/<int:lectid+1>')

    # pass

def complete(request, studentid, courseid, lectid):
    #  mywatch_time = Watch_time.objects.filter(student__pk=studentid).get(w_lect__pk=lectid)
    mywatch_time = Watch_time.objects.filter(student__pk=studentid).filter(
        w_lect__pk=lectid)

    # mywatch_time.completed = 'True'
    # mywatch_time.completed_date = date.today()
    for watch in mywatch_time:
      watch.completed='True'
      watch.completed_date=date.today()
      watch.save()
      # print("#####################",watch.student,watch.w_lect.lecture_name,watch.completed,watch.completed_date,"#####################")
    # mywatch_time.model.completed='True'
    # mywatch_time.model.completed_date=date.today()
    # lecture = Lecture.objects.get(pk=lectid)
    # watchtimelist=[]
    # for watch in mywatch_time:
    #     if watch.w_lect.pk in lecture:
    #         watch.completed='True'
    #         watchtimelist.append(watch)
    # print("#####################",mywatch_time,"#####################")
    return redirect(openLectlistfromstudent,
                    studentid=studentid,
                    courseid=courseid)


def openCourse(request, courseid):
    myteacher = Teacher.objects.get(course__pk = courseid)
    lectures = Lecture.objects.filter(teacher__pk=myteacher.pk)
    context = {'lectures': lectures,
                'teacher' : myteacher.teacher_name}
    return render(request, 'coursePage.html', context)


def teachercources(request, teacherid):
    # album = Album.objects.filter(pk=albumid)
    # courses = Course.objects.filter(teacher=teacherid)
    # context = {'courses': courses}
    # return render(request, 'coursePage.html', context)
    # album = Album.objects.filter(pk=albumid)
    pass

def viewallcourses(request):
    courses = Course.objects.all()
    mylist=[]
    for course in courses :      
        myteacher = Teacher.objects.get(course__pk=course.pk)
        lectures = Lecture.objects.filter(teacher__pk=myteacher.pk)
        lect_counter = 0
        watch_counter=0
        rating = 0
        for lect in lectures:
          lect_counter+=1
          mywatch_time = Watch_time.objects.filter(w_lect__pk=lect.pk)
          watch_counter=0
          for watch in mywatch_time:           
            if watch.completed==True:
              watch_counter+=1
              rating = rating  + watch.Rating
          if watch_counter!=0:
            rating= rating /watch_counter            
        if lect_counter!=0:
          rating = rating/lect_counter          
        mylist.append(int(rating)*'★')
    
    myfile = zip(mylist, courses)
    context = {
        'myfile': myfile,
    }
    return render(request, 'allcourses.html', context)


def studentprofile(request, studentid):
      student = Student.objects.get(pk=studentid)
      context = {
          'student': student,
      }
      return render(request, 'student_profile.html', context)


def addstudent(request):
    # if we get POST method, we will use this
    if request.method == 'POST':
        form = StudentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = StudentForm()
        return render(request, 'addstudent.html', {'form': form})
