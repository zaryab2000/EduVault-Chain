from django.urls import path,include
from . import views
urlpatterns = [
	path('', views.base, name='base'),
	path('students/',views.students, name='students'),
	path('modify/', views.modify, name='modify'),
	path('addStudent/', views.addStudent, name='addStudent'),
	path('addAttendance/<int:id>', views.addAttendance, name='addAttendance')

]
