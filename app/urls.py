from django.urls import path
from app import views, project_editing_view
from app.project_editing_view import reformulate_project
name="app"
urlpatterns = [
    path('', views.index, name="home"),
    path('project/submision/',views.project_submision, name="project-submision"),
    path('project/cabinet/home/',views.cabinet_home, name="cabinet-home"),
    path('project/cabinet/incoming/',views.incoming, name="cabinet-incoming"),
    path('project/cabinet/validated/',views.validated, name="cabinet-validated"),
    path('project/cabinet/rejected/',views.rejected, name="cabinet-rejected"),
    path('project/cabinet/detail/<uid>/', project_editing_view.detail_project, name="project_cabinet_details"),
    path('project/cabinet/accepte/<uid>/', project_editing_view.accepte_project, name="cabinet-accepte-project"),
    path('project/cabinet/reject/<uid>/', project_editing_view.reject_project, name="cabinet-reject-project"),
    path('project/cabinet/publish/<uid>/', project_editing_view.publish_project, name="cabinet-publishp-roject"),
    path("project/<uuid:uid>/reformulate/", reformulate_project, name="reformulate_project"),


]