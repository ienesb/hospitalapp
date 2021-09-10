from django.urls import path

from . import views

urlpatterns = [
    path("", views.Home.as_view(), name="newhome"),
    path("appointments", views.Appointments.as_view(), name="appointments"),
    path("removeappointment/<int:pk>", views.removeappointment, name="removeappointment"),
    path("newappointment", views.NewAppointment.as_view(), name="newappointment"),
    path("editappointment/<int:pk>", views.EditAppointment.as_view(), name="editappointment"),
    path("newappointment/<int:pk>", views.NewAppointment.as_view(), name="makeanappointment"),
    path("getdep/<int:pk>", views.getdep, name="getdep"),
    path("getresult/<int:pk>", views.getresult, name="getresult"),
    path("records", views.Records.as_view(), name="records"),
    path("get/<int:pk>", views.get_record_from_pk, name="get"),
    path("addrating", views.addrating, name="addrating"),
    path("myresults", views.MyResults.as_view(), name="myresults"),
    path("download/<int:pk>", views.download, name="download"),
    path("upload", views.Upload.as_view(), name="upload"),
    path("upload/<int:pk>", views.Upload.as_view(), name="uploadpk"),
    path("editresult/<int:pk>", views.EditResult.as_view(), name="editresult"),
    path("display/<int:pk>", views.DisplayResult.as_view(), name="display"),
    path("myaccount", views.MyAccount.as_view(), name="myaccount"),
    path("doctorlist", views.DoctorList.as_view(), name="doctorlist"),
    path("mypatientlist", views.MyPatientList.as_view(), name="mypatientlist"),
]
