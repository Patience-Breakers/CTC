# Create your views here.
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
import re
from datetime import date
from bs4 import BeautifulSoup
import requests
# from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from .models import Student, Teacher, Course, Lecture, Watch_time,Todo
from .forms import StudentForm
# import collections
from .models import Teacher
from django.db import connection

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
    # tech = Teacher.objects.all()
    tech = Teacher.objects.raw('SELECT * FROM accounts_teacher')
    print(tech)
    return render(request, 'teachers.html', {'tech': tech})

def teacherlogin(request):
  if request.method == 'POST':
        teachername = request.POST['username']
        teacherpassword = request.POST['password']
        teacher = Teacher.objects.raw('SELECT * FROM accounts_teacher WHERE teacher_name =%s AND password=%s',[teachername,teacherpassword])
        # teacher= Teacher.objects.filter(teacher_name=teachername).filter(
        #     password=teacherpassword)
        print("done")

        if teacher is not None:
            print("done full")
            teacherid = teacher[0].pk
            
            str_pass = '/teacher/' + str(teacherid)
            return redirect(str_pass)
        else:
            return redirect('/')

  return render(request, 'teacherlogin.html')
  
def handlelogin(request):
    if request.method == 'POST':
        lusername = request.POST['username']
        lpassword = request.POST['password']
        student = Student.objects.raw('SELECT * FROM accounts_student WHERE username =%s AND password=%s',[lusername,lpassword])
        if student is not None:
            studentid = student[0].pk
            str_pass = '/students/' + str(studentid)
            return redirect(str_pass)
        else:
            return redirect('/')

    return render(request, 'login.html')

def openteacher(request, teacherid): 
    # course = Course.objects.get(pk=courseid)
    # myteacher = Teacher.objects.get(course__pk=courseid)
    # lectures = Lecture.objects.filter(teacher__pk=myteacher.pk)
    # teacher = Teacher.objects.get(pk=teacherid)
    myteacher = Teacher.objects.get(pk=teacherid)
    course = Course.objects.get(pk=myteacher.course.pk)
    print(course.course_name)
    context ={
      'course':course,
    }
    return render(request, 'teacherpage.html',context)

def classnotes(request):
    return render(request, 'classnotes.html')


def allstudents(request):
    students = Student.objects.raw('SELECT * FROM  accounts_student ')
    context = {
        'students': students,
    }
    return render(request, 'allstudents.html', context)

def task(request, studentid, taskid):
    #   task = Todo.objects.get(pk= taskid)
    task = Todo.objects.raw('SELECT * FROM accounts_todo WHERE id = %d', [taskid])
    task.delete()
    return redirect(openstudent, studentid=studentid)

#open student aka dashboard
def openstudent(request, studentid): 
    # student = Student.objects.get(pk=studentid)
    student = Student.objects.raw('SELECT * FROM accounts_student WHERE student_id=%s',[studentid])[0]
    print("###########################",student)
    courses = student.courses.all()
    # courses = student.courses.raw('SELECT * FROM accounts_course')
    mylist=[]
    for cour in courses :
        # myteacher = Teacher.objects.get(course__pk=cour.pk)
        myteacher = Teacher.objects.raw('SELECT * FROM accounts_teacher WHERE course_id=%s',[cour.course_id])[0]
        # lectures = Lecture.objects.filter(teacher__pk=myteacher.teacher_id)
        lectures = Lecture.objects.raw('SELECT * FROM accounts_lecture WHERE teacher_id=%s',[myteacher.teacher_id])
        lect_counter = 0
        watch_counter=0
        for lect in lectures :
          lect_counter+=1
          # mywatch_time = Watch_time.objects.filter(student__pk=studentid).filter(
          #     w_lect__pk=lect.pk)
          mywatch_time = Watch_time.objects.raw('SELECT * FROM accounts_watch_time WHERE student_id=%s AND w_lect_id=%s',[studentid,lect.lec_id])
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
    myfile = zip(mylist, courses)
    ###Kaliappan kar rha hai yeh
    # tasks = Todo.objects.filter(student__pk=studentid)
    tasks = Todo.objects.raw('SELECT * FROM accounts_todo WHERE student_id=%s',[studentid])
    context = {
        'student': student,
        'myfile' : myfile,
        'mylist' : mylist,
        'courses':courses,
        'course':courses[0].course_name,
        'course1':courses[1].course_name,
        'graphlist' : graphlist,
        'tasks' : tasks,
    }
    return render(request, 'studentPage.html', context)





def handlelogout():
    pass


def openLectlistfromstudent(request, studentid, courseid):
    # course = Course.objects.get(pk=courseid)
    course = Course.objects.raw('SELECT * FROM accounts_course WHERE course_id=%s',[courseid])[0]
    myteacher = Teacher.objects.get(course__pk=courseid)
    # myteacher = Teacher.objects.raw('SELECT')
    lectures = Lecture.objects.filter(teacher__pk=myteacher.pk)
    mywatch_time = Watch_time.objects.filter(student__pk=studentid)
    lectids = []
    for lect in lectures:
        lectids.append(lect.pk)
    watchtimelist = []
    for watch in mywatch_time:
        if watch.w_lect.pk in lectids:
            watchtimelist.append(watch)

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
    return render(request, 'opencoursefromstudent.html', context)


def openLecturefromstudent(request, studentid, courseid, lectid):
    if request.method == 'POST':
        rating = request.POST['rating']
        # mywatch_time = Watch_time.objects.filter(student__pk=studentid).filter(
        #     w_lect__pk=lectid)
        mywatch_time = Watch_time.objects.raw('SELECT * FROM accounts_watch_time WHERE student_id=%s AND w_lect_id=%s',[studentid,lectid])
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
        # course = Course.objects.get(pk=courseid)
        course = Course.objects.raw('SELECT * FROM accounts_course WHERE course_id=%s',[courseid])[0]
        # student = Student.objects.get(pk=studentid)
        student = Student.objects.raw('SELECT * FROM accounts_student WHERE student_id=%s',[studentid])[0]
        # lecture = Lecture.objects.get(pk=lectid)
        lecture = Lecture.objects.raw('SELECT * FROM accounts_lecture WHERE lec_id=%s',[lectid])[0]
        
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

    course = Course.objects.get(pk=courseid)
    course = Course
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

def complete(request, studentid, courseid, lectid):
    mywatch_time = Watch_time.objects.filter(student__pk=studentid).filter(
        w_lect__pk=lectid)

    for watch in mywatch_time:
      watch.completed='True'
      watch.completed_date=date.today()
      watch.save()
   
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
      # student = Student.objects.get(pk=studentid)
      student = Student.objects.raw('SELECT * FROM accounts_student WHERE student_id=%s',[studentid])[0]
      context = {
          'student': student,
      }
      return render(request, 'student_profile.html', context)



def addstudent(request):
    # if we get POST method, we will use this
    if request.method == 'POST':
        form = StudentForm(request.POST)
        print("hello\n\n\n---\n\n\n\n\n---------------\n\n\n\n\n\n---\n\n")
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = StudentForm()
        return render(request, 'addstudent.html', {'form': form})


# def addstudent(request):
#     # if we get POST method, we will use this
#     if request.method == 'POST':
#         form = StudentForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             form.save()
#             stu = Student()
#             stu.name = form.cleaned_data('name')
#             stu.username = form.cleaned_data('username')
#             stu.password = form.cleaned_data('password')
#             stu.email = form.cleaned_data('email')
#             stu.phone_no = form.cleaned_data('phone_no')
#             stu.image = form.cleaned_data('image')
#             stu.dob = form.cleaned_data('dob')
#             stu.CATEGORY = form.cleaned_data('CATEGORY')
#             stu.stud_category = form.cleaned_data('stud_category')
#             courses_id = form.cleaned_data('courses')
#             for course_id in courses_id:
#               cou=Course.objects.get(pk=course_id)
#               stu.courses.add(cou)
#             print(stu.name)
#             stu.save()
#             return HttpResponseRedirect('/')
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = StudentForm()
#         return render(request, 'addstudent.html', {'form': form})
