class Recipe:
    def __init__ (self, autor, titulo, resumen, ingredientes, procedimiento, tiempo, imagen, comentarios, reacciones):
        self.autor = autor
        self.title = titulo
        self.resumen = resumen
        self.ingredientes = ingredientes
        self.procedimiento = procedimiento
        self.tiempo = tiempo
        self.imagen = imagen
        self.comentarios = comentarios
        self.reacciones = reacciones

    def getRecipeAsList(self):
        list = {}
        list["autor"] = self.autor
        list["titulo"] = self.title
        list["resumen"] = self.resumen
        list["ingredientes"] = self.ingredientes
        list["procedimiento"] = self.procedimiento
        list["tiempo"] = self.tiempo
        list["imagen"] = self.imagen
        list["comentarios"] = self.comentarios
        list["reacciones"] = self.reacciones
        return list

class RecipesHandler:

    recipes = []

    r1 = Recipe("Autor1","Titulo1","Res1","1ingr1,1ingr2","proced1","tiempo1","imagen1","json-coment1","json-reac1")
    r2 = Recipe("Autor2","Titulo2","Res2","2ingr1,2ingr2","proced2","tiempo2","imagen2","json-coment2","json-reac2")
    r3 = Recipe("Autor3","Titulo3","Res3","3ingr1,3ingr2","proced3","tiempo3","imagen3","json-coment3","json-reac3")

    recipes.append(r1)
    recipes.append(r2)
    recipes.append(r3)
    

    def addRecipe(theRecipe):

        if (not RecipesHandler.getRecipeByTitle(theRecipe.title)):

            RecipesHandler.recipes.append(theRecipe)
            return True
        else:
            return False

    def removeRecipeByTitle(title):
        for recipe in RecipesHandler.recipes:
            if (recipe.title == title):
                RecipesHandler.recipes.remove(recipe)
                return True
        return False


    #0: sucess
	#2: new title already exist
	#3: recipe doesn't exist
    def modifyRecipe(pastTitle, newRecipe):


        theRecipe = RecipesHandler.getRecipeByTitle(newRecipe.title)
        if (theRecipe != None and newRecipe.title != pastTitle):
            return 2

        for _recipe in RecipesHandler.recipes:
            if(_recipe.title == pastTitle):
                RecipesHandler.recipes.remove(_recipe)
                RecipesHandler.recipes.append(newRecipe)
                return 0
        return 3



    def searchRecipes(key, exactMatch):
        foundRecipes = [] 


        if (key == "*"):
            return RecipesHandler.recipes


        for recipe in RecipesHandler.recipes:
            if (exactMatch == "true"):
                if (key == recipe.title):
                    foundRecipes.append(recipe)
            else:
                if (key in recipe.title):
                    foundRecipes.append(recipe)
        return foundRecipes


    def getRecipeByTitle(title):
        for recipe in RecipesHandler.recipes:
            if (recipe.title == title):
                return recipe

    def getRecipesAsList(recipes):
        list = {}
        i = 0
        for recipe in recipes:
            list[i] = recipe.getRecipeAsList()
            i = i + 1
        return list
            