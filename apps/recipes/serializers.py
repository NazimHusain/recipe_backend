from rest_framework import serializers
from .models import Ingredient, Recipe, FavoriteRecipe

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'picture']

class RecipeSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = [
            'id', 'creator', 'title', 'description', 'ingredients', 
            'instructions', 'prep_duration', 'cook_duration', 
            'step_by_step_picture', 'thumbnail', 'created_at', 'updated_at'
        ]

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients_data:
            ingredient_obj, created = Ingredient.objects.get_or_create(**ingredient)
            recipe.ingredients.add(ingredient_obj)
        return recipe
    
    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', None)
    
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if ingredients_data is not None:
            instance.ingredients.clear()
            
            for ingredient in ingredients_data:
                ingredient_obj, created = Ingredient.objects.get_or_create(**ingredient)
                instance.ingredients.add(ingredient_obj)
        
        return instance
    
    
class FavoriteRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRecipe
        fields = ['id', 'viewer', 'recipe']



class FavoriteRecipeSerializer(serializers.ModelSerializer):
    recipe_title = serializers.ReadOnlyField(source='recipe.title')

    class Meta:
        model = FavoriteRecipe
        fields = ['id', 'viewer', 'recipe', 'recipe_title', 'created_at', 'updated_at']
        read_only_fields = ['id', 'viewer', 'recipe_title', 'created_at', 'updated_at']




