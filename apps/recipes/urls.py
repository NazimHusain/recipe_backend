


from django.urls import path
from apps.recipes.views import RecipeListCreateAPIView, RecipeDetailAPIView,  FavoriteRecipeAPIView,RecipeDownloadPDFAPIView

urlpatterns = [
    path('recipe/', RecipeListCreateAPIView.as_view(), name='recipe-list-create'),
    path('recipe/<int:pk>/', RecipeDetailAPIView.as_view(), name='recipe-detail'),
    path('recipe/<int:pk>/download/', RecipeDownloadPDFAPIView.as_view(), name='recipe-download-pdf'),
    path('favorites/', FavoriteRecipeAPIView.as_view(), name='favorite-list-create'),
]
