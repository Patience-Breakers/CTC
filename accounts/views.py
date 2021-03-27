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


def dashboard(request):
    return render(request, 'dashboard.html')


#crawler ka funciton
def crawler(request):
    if request.method == 'POST':
        query = request.POST['query']
        results = 5
        page = requests.get(f"https://www.google.com/search?q={query}&num={5}")
        soup = BeautifulSoup(page.content, "html.parser")
        links = soup.findAll("a")
        res = 0
        results = {}
        for link in links:
            per_res = {}
            link_href = link.get('href')
            if "url?q=" in link_href and not "webcache" in link_href:
                #per_res.update("Inner Text ={}.format(link.text))
                if link.get('title'):
                  per_res.update({"Title ":link.get("title")})
                if link.parent.get("id"):
                  per_res.update({"Name " :link.parent.get("id")})
                per_res.update({"Link":link.get('href').split("?q=")[1].split("&sa=U")[0]})
                res += 1
            results.update(per_res)
            if res > 5:
                break
                
        results=list(results.values())   
        print(results) 
        context={
            'results':results[0]
          }
        return render(request,'crawlerResult.html',context)               


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
    context = {
        'student': student,
        'courses': courses,
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
    myteacher = Teacher.objects.get(course__pk = courseid)
    lectures = Lecture.objects.filter(teacher__pk=myteacher.pk)
    # mywatch_time = Watch_time.objects.filter(student__pk=studentid)
    
    mywatch_time = Watch_time.objects.filter(student__pk=studentid).filter(w_lect__pk=lectid)
    context = {
        'lectures': lectures,
        'studentid': studentid,
        'Watch_time': mywatch_time,
        'course': course,
    }
    return render(request, 'opencoursefromstudent.html', context)

def openLecturefromstudent(request, studentid, courseid, lectid):
  if request.method == 'POST':
    mywatch_time = Watch_time.objects.filter(student__pk=studentid).filter(w_lect__pk=lectid)
    pass
  else :
    myteacher = Teacher.objects.get(course__pk = courseid)
    lecture = Lecture.objects.filter(teacher__pk=myteacher.pk).get(pk=lectid)
    course = Course.objects.get(pk=courseid)
    student = Student.objects.get(pk=studentid)
    lecture = Lecture.objects.get(pk=lectid)
    mywatch_time = Watch_time.objects.filter(student__pk=studentid).filter(w_lect__pk=lectid)
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
    mywatch_time = Watch_time.objects.filter(student__pk=studentid).filter(w_lect__pk=lectid)

    mywatch_time[0].completed='True'
    mywatch_time[0].completed_date=date.today()
    # print("#####################",mywatch_time,"#####################")
    return redirect(openLecturefromstudent, studentid=studentid , courseid=courseid ,lectid=lectid+1)
    # course = Course.objects.get(pk=courseid)
    # student = Student.objects.get(pk=studentid)
    # lecture = Lecture.objects.get(pk=lectid)
    # myteacher = Teacher.objects.get(course__pk = courseid)
    # new_lecture = Lecture.objects.get(pk=lectid+1)
    # mywatch_time = Watch_time.objects.filter(student__pk=studentid).filter(w_lect__pk=lectid+1)
    # if new_lecture is not None:
    #   context = {
    #       'lecture': new_lecture,
    #       'student': student,
    #       'course': course,
    #       'Watch_time': mywatch_time,
    #   }
    #   return render(request, 'openLecturefromstudent.html', context)
    # return HttpResponse('students/<int:studentid>/courses/<int:courseid>/lecture/<int:lectid+1>')
    
    # pass



def openCourse(request, courseid):
    # album = Album.objects.filter(pk=albumid)
    lectures = Lecture.objects.filter(course_no__pk=courseid)
    context = {'lectures': lectures}
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
    context = {
        'courses': courses,
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
            return HttpResponseRedirect('/allstudents/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = StudentForm()
        return render(request, 'addstudent.html', {'form': form})