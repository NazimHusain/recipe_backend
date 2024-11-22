
from django.db import models
from django.contrib.auth.models import User
from apps.helpers import models as coreModels

class Ingredient(coreModels.AbstractDateTimeModel):
    name = models.CharField(max_length=100, verbose_name="Ingredient Name")
    picture = models.ForeignKey(
        coreModels.FileUpload,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ingredient_pictures",
        verbose_name="Ingredient Picture"
    )
    
    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"
        ordering = ['name']

    def __str__(self):
        return self.name
    

class Recipe(coreModels.AbstractDateTimeModel):
    creator = models.ForeignKey(
        "customuser.User", 
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name="Creator"
    )
    
    title = models.CharField(max_length=200, verbose_name="Recipe Title")
    description = models.TextField(verbose_name="Recipe Description")
    ingredients = models.ManyToManyField(
        Ingredient, 
        related_name='recipes',
        verbose_name="Ingredients"
    )
    instructions = models.TextField(verbose_name="Cooking Instructions")
    prep_duration = models.PositiveIntegerField(
        verbose_name="Preparation Duration (minutes)", 
        help_text="Time required for preparation in minutes"
    )
    cook_duration = models.PositiveIntegerField(
        verbose_name="Cooking Duration (minutes)", 
        help_text="Time required for cooking in minutes"
    )

    step_by_step_picture = models.ForeignKey(
        coreModels.FileUpload,
        on_delete=models.SET_NULL,
        related_name='steps_picture',
        null=True,
        blank=True,
        verbose_name="Step-by-Step Picture"
    )
    
    thumbnail = models.ForeignKey(
        coreModels.FileUpload,
        on_delete=models.SET_NULL,
        related_name='recipe_thumbnails',
        null=True,
        blank=True,
        verbose_name="Thumbnail Image"
    )

    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class FavoriteRecipe(coreModels.AbstractDateTimeModel):
    viewer = models.ForeignKey(
        "customuser.User", 
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
         verbose_name="Viewer"
    )
    recipe = models.ForeignKey(
        Recipe, 
        on_delete=models.CASCADE, 
        related_name='favorited_by',
        verbose_name="Favorite Recipe"
    )

    class Meta:
        verbose_name = "Favorite Recipe"
        verbose_name_plural = "Favorite Recipes"
        unique_together = ('viewer', 'recipe')
        ordering = ['viewer']

    def __str__(self):
        return f"{self.viewer.username} -> {self.recipe.title}"
