
from django.urls import path
from apps.helpers import views


urlpatterns = [
    path("dropdownmaster/", views.DropDownMasterListing.as_view()),
    path("dropdownmaster/<str:slug>/", views.DropDownValuesListingView.as_view()),
    path("fileupload/", views.FileUpload.as_view()),
]