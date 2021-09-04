from django.urls import path

from . import views

urlpatterns = [
    path("", views.Home.as_view(), name="newhome"),
    path("appointments", views.Appointments.as_view(), name="appointments"),
    path("newappointment", views.NewAppointment.as_view(), name="newappointment"),
    path("getdep/<int:pk>", views.getdep, name="getdep"),
    path("records", views.Records.as_view(), name="records"),
    path("get/<int:pk>", views.get_record_from_pk, name="get"),
    path("myresults", views.MyResults.as_view(), name="myresults"),
    path("download/<int:pk>", views.download, name="download"),
    path("upload", views.Upload.as_view(), name="upload"),
    path("display/<int:pk>", views.DisplayResult.as_view(), name="display"),
    path("myaccount", views.MyAccount.as_view(), name="myaccount"),
]
