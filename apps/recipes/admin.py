
from django.contrib import admin
from apps.recipes import models as recipesModels

class AdminRecipe(admin.ModelAdmin):
    list_display = ("id","creator", "title",
                    "description","get_ingredients","instructions",
                    "prep_duration","cook_duration","step_by_step_picture",
                    "thumbnail",
                    )
    # Custom method to display ingredients
    def get_ingredients(self, obj):
        return ", ".join([ingredient.name for ingredient in obj.ingredients.all()])

admin.site.register(recipesModels.Recipe, AdminRecipe)

class IngredientAdmin(admin.ModelAdmin):
    list_display = ("id","name", "picture")
admin.site.register(recipesModels.Ingredient, IngredientAdmin)


class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ("id","viewer", "recipe")
admin.site.register(recipesModels.FavoriteRecipe, FavoriteRecipeAdmin)

    
