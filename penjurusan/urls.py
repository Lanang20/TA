from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("daftar/", views.daftar, name="daftar"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("login_view/", views.login_view, name="login_view"),
    path("profile_view/", views.profile_view, name="profile_view"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("send_contact_email/", views.send_contact_email, name="send_contact_email"),
    path("jurusan_view/", views.jurusan_view, name="jurusan_view"),
    path("tes/", views.tes, name="tes"),
    path("mulai_tes/", views.mulai_tes, name="mulai_tes"),
    path("hasil_tes/", views.hasil_tes, name="hasil_tes"),
    path("selesai_tes/", views.selesai_tes, name="selesai_tes"),
    path("generatePDF/", views.generatePDF, name="generatePDF"),
    path("tentang_tes/", views.tentang_tes, name="tentang_tes"),
    path("logout_view/", views.logout_view, name="logout_view"),
    path("thankyou_view/", views.thankyou_view, name="thankyou_view"),
    path("logout_session/", views.logout_session, name="logout_session"),
]