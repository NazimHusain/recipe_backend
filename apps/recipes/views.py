from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import FileResponse
from .models import Recipe, Ingredient, FavoriteRecipe
from .serializers import RecipeSerializer, FavoriteRecipeSerializer
from reportlab.pdfgen import canvas
import io
from rest_framework.exceptions import PermissionDenied
from django.http import HttpResponse
from io import BytesIO
import pandas as pd
from datetime import datetime

class RecipeListCreateAPIView(APIView):
  
    def get(self, request,version):
        """List Recipe"""
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request,version): 
        """create recipe"""
        if request.user.role.slug != "creator":
            raise PermissionDenied("You are not authorized to create recipes.")
       
        creator = request.user
        request.data["creator"] = creator.id
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeDetailAPIView(APIView):
  
    def get_object(self, pk):
        try:
            return Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            return None

    def get(self, request, pk,version):
        """Details Recipe"""
        recipe = self.get_object(pk)
        if recipe:
            serializer = RecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, version: str):
        """Update Recipe"""
        recipe = self.get_object(pk)
        if recipe.creator != request.user:
            raise PermissionDenied("You are not authorized to modify this recipe.")
     
        serializer = RecipeSerializer(recipe, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      

    def delete(self, request, pk, version):
        """Delete Recipe"""
        recipe = self.get_object(pk)
        if recipe.creator != request.user:
            raise PermissionDenied("You are not authorized to delete this recipe.")
        recipe.delete()
        return Response({"detail": "Recipe deleted"}, status=status.HTTP_204_NO_CONTENT)

 
class RecipeDownloadPDFAPIView(APIView):
    permission_classes = ()

    def get(self, request, pk, version):
        try:
            recipe = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            return Response({"detail": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)
        
        data = {
            "Field": ["Title", "Description", "Preparation Time", "Cooking Time", "Instructions"],
            "Value": [
                recipe.title,
                recipe.description,
                f"{recipe.prep_duration} minutes",
                f"{recipe.cook_duration} minutes",
                recipe.instructions
            ],
        }
        
        data_frame = pd.DataFrame(data)
        with BytesIO() as b:
            writer = pd.ExcelWriter(b, engine="xlsxwriter")
            data_frame.to_excel(writer, sheet_name="Sheet1", index=False, startcol=0, startrow=3)
        
            worksheet = writer.sheets["Sheet1"]
            workbook = writer.book
            header_style = workbook.add_format(
                        {
                            "bold": True,
                            "font_size": 14,
                            "align": "center",
                            "valign": "vcenter",
                            "fg_color": "#12284B",
                            "font_color": "#FFFFFF",
                        }
                )
        
            try:
                generated_on = f"Report Generated on {datetime.now()}"
            except Exception as e:
                return e
            sheetHeading1= f'Recipe Name: {recipe.title}'

            worksheet.merge_range("A1:C1", sheetHeading1, header_style)
            
            worksheet.merge_range("A2:C2", generated_on, header_style)
            worksheet.set_column("A:C", 30)
            writer.close()
            filename = f"{recipe.title}-{datetime.now()}.xlsx"
            response = HttpResponse(
                b.getvalue(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = "attachment; filename=%s" % filename
            return response
                



class FavoriteRecipeAPIView(APIView):
    def get(self, request, version: str):
        favorites = FavoriteRecipe.objects.filter(viewer=request.user)
        serializer = FavoriteRecipeSerializer(favorites, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, version):
        """Add a recipe to the viewer's favorites."""
        recipe_id = request.data.get('recipe_id')
        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            return Response({"error": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)

        favorite, created = FavoriteRecipe.objects.get_or_create(viewer=request.user, recipe=recipe)
        if not created:
            return Response({"message": "Recipe is already in favorites"}, status=status.HTTP_200_OK)

        return Response({"message": "Recipe added to favorites"}, status=status.HTTP_201_CREATED)

    def delete(self, request, version):
        """Remove a recipe from the user's favorites."""
        recipe_id = request.data.get('recipe_id')
        try:
            favorite = FavoriteRecipe.objects.get(viewer=request.user, recipe_id=recipe_id)
            favorite.delete()
            return Response({"message": "Recipe removed from favorites"}, status=status.HTTP_200_OK)
        except FavoriteRecipe.DoesNotExist:
            return Response({"error": "Favorite recipe not found"}, status=status.HTTP_404_NOT_FOUND)








