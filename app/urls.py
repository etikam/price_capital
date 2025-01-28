from django.urls import path

from app import project_editing_view, views

name = "app"
urlpatterns = [
    path("", views.index, name="home"),
    path("project/submision/", views.project_submision, name="project-submision"),
    path("project/cabinet/home/", views.cabinet_home, name="cabinet-home"),
    path("project/cabinet/incoming/", views.incoming, name="cabinet-incoming"),
    path("project/cabinet/validated/", views.validated, name="cabinet-validated"),
    # path('project/cabinet/rejected/',views.rejected, name="cabinet-rejected"),
    path("project/cabinet/detail/<uuid:uid>/", project_editing_view.detail_project, name="project_cabinet_details"),
    path("project/cabinet/accepte/<uuid:uid>/", project_editing_view.accepte_project, name="cabinet-accepte-project"),
    path("project/cabinet/reject/<uuid:uid>/", project_editing_view.reject_project, name="cabinet-reject-project"),
    path("project/cabinet/publish/<uuid:uid>/", project_editing_view.publish_project, name="cabinet-publishp-roject"),
    path("project/<uuid:uid>/reformulate/", project_editing_view.reformulate_project, name="reformulate_project"),
    path("project/detail/<uuid:uid>/", views.detail_project, name="detail-project"),
    path("product/detail/<uuid:uid>/", views.detail_product, name="detail-product"),
    path("add-category/", project_editing_view.add_category, name="add_category"),
    path("mysapce/", views.user_space, name="my-space"),
    path("myspace/detail/<int:project_id>/", views.project_detail, name="my-project-detail"),
    path("cabinet/project/<int:project_id>/", views.cabinet_project_detail, name="cabinet-project-detail"),
    path("contact/", views.contact_view, name="contact"),
]
