from django.urls import path
from . import views

urlpatterns = [
    # path('', image_table_view, name='image_table'),
    # path('', views.select_macid, name='list_macid'),
    #  path('list_folders/<str:macid_id>/', views.select_date, name='list_folders'),
    path('', views.list_folders, name='list_folders'),
    path('check-date-folder/', views.check_date_folder, name='check_date_folder'),
    path('list-images/<str:folder_id>/', views.list_images, name='list_images'),  # Assuming this view already exists

    path("update-data/", views.update_data, name="update-data"),
    path("export-to-excel/", views.export_to_excel, name="export-to-excel"),
]
