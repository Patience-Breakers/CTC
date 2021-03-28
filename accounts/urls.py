from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('blank', views.blank, name="home"),
    path('login', views.handlelogin, name="handlelogin"),
    path('logout', views.handlelogout, name="handlelogout"),
    path("dashboard/", views.dashboard, name='dashboard'),
    path("calendar/", views.calendar, name='calendar'),
    path("assignments/", views.assignments, name='assignments'),
    path("grades/", views.grades, name='grades'),
    path("teachers/", views.teachers, name='teachers'),
    path("classnotes/", views.classnotes, name='classnotes'),
    path("search", views.crawler, name='crawler'),

    path('addstudent',views.addstudent,name="addstudent"),

    path("allcourses/", views.viewallcourses, name='allcourses'),
    path('openCourse/<int:courseid>/', views.openCourse, name='openCourse'),

    path("allstudents/", views.allstudents, name='allstudents'),
    path('students/<int:studentid>/', views.openstudent, name='openstudent'),
    # path('teacher/<int:teacherid>/', views.teachercources, name='teachercources'),
    path('studentprofile/<int:studentid>/',views.studentprofile,name='studentprofile'),
   
    # students courses
    path('students/<int:studentid>/courses/<int:courseid>/',
         views.openLectlistfromstudent, name='openLectlistfromstudent'),
    path('students/<int:studentid>/done/<int:taskid>/',
         views.task, name='task'),
    path('students/<int:studentid>/courses/<int:courseid>/lecture/<int:lectid>/',
         views.openLecturefromstudent, name='openLecturefromstudent'),
    path('students/<int:studentid>/courses/<int:courseid>/lecture/<int:lectid>/next/',
         views.nextlect, name='nextlect'),
    path('students/<int:studentid>/courses/<int:courseid>/lecture/<int:lectid>/complete/',
         views.complete, name='complete'),
    # path('students/<int:studentid>/courses/<int:courseid>/lecture/<int:lectid>/next/',
    #      views.nextlect, name='nextlect'),

    # path('students/<int:studentid>/courses/<int:courseid>/',
    #     views.openCoursefromstudent, name='openCoursefromstudent'),

    # path('studentscourses/<int:studentid>/courses/<int:courseid>/',
    #      views.openCoursefromstudent, name='openCoursefromstudent'),
    # path('studentscourses/<int:studentid>/courses/<int:courseid>/lectures/<int:lectid>',
    #      views.openLecturefromstudent, name='openLecturefromstudent'),



    # path('openCourse/<int:albumid>/', views.openAlbum, name='openAlbum'),
    # path('openAlbum/<int:albumid>/', views.openAlbum, name='openAlbum'),
    # path('songsPlay/<int:myid>/', views.songsPlay, name='songsPlay'),
    # path('artistPage/<int:artistid>/', views.openArtist, name='songsPlay'),

]