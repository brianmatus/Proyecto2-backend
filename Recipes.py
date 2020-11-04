class Recipe:
    def __init__(self, author, titulo, abstract, ingredients, procedure, time, imagen, comments, reactions):
        self.author = author
        self.title = titulo
        self.abstract = abstract
        self.ingredients = ingredients
        self.procedure = procedure
        self.time = time
        self.imagen = imagen
        self.comments = comments
        self.reactions = reactions

    def getRecipeAsList(self):
        return {
            "author": self.author,
            "title": self.title,
            "abstract": self.abstract,
            "ingredients": self.ingredients,
            "procedure": self.procedure,
            "time": self.time,
            "imagen": self.imagen,
            "comments": self.comments,
            "reactions": self.reactions
        }

    def addComment(self, author, body, date):
        self.comments.append( {
            "author": author,
            "body": body,
            "date": date
        })


class RecipesHandler:
    recipes = []

    r1 = Recipe("Autor1", "Titulo1", "Res1", "1ingr1,1ingr2", "proced1", "time1",
                "https://i.ytimg.com/vi/fVh-h6K-zfY/maxresdefault.jpg",
                [{"author": "Pitito", "body": "This is a nais receta mai frend", "date": "01/04/2020 15:40:09"}],
                {})
    r2 = Recipe("Autor2", "Titulo2", "Res2", "2ingr1,2ingr2", "proced2", "time2",
                "https://i.ytimg.com/vi/fVh-h6K-zfY/maxresdefault.jpg", {
                    "0": {"author": "Pitito5", "body": "This is a nais receta mai frend nais dik",
                          "date": "01/05/2020 15:40:09"}}, {})
    r3 = Recipe("Autor3", "Titulo3", "Res3", "3ingr1,3ingr2", "proced3", "time3",
                "https://i.ytimg.com/vi/fVh-h6K-zfY/maxresdefault.jpg",
                [{"author": "Pitito", "body": "This is beri bad, chish", "date": "05/04/2020 15:40:09"}], {})

    recipes.append(r1)
    recipes.append(r2)
    recipes.append(r3)

    def addRecipe(theRecipe):

        if (not RecipesHandler.getRecipeByAuthorAndTitle(theRecipe.title, theRecipe.author)):

            RecipesHandler.recipes.append(theRecipe)
            return True
        else:
            return False

    def removeRecipeByTitleAndAuthor(title, author):
        for recipe in RecipesHandler.recipes:
            if (recipe.title == title and recipe.author == author):
                RecipesHandler.recipes.remove(recipe)
                return True
        return False

    # 0: sucess
    # 2: new title already exist
    # 3: recipe doesn't exist
    def modifyRecipe(pastAuthor, pastTitle, newRecipe):

        theRecipe = RecipesHandler.getRecipeByAuthorAndTitle(newRecipe.title, newRecipe.author)
        if (theRecipe != None and newRecipe.title != pastTitle and newRecipe.author != pastAuthor):
            return 2

        for _recipe in RecipesHandler.recipes:
            if (_recipe.title == pastTitle and _recipe.author == pastAuthor):
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

    def getRecipeByAuthorAndTitle(author, title):
        print("OBTENIENDO CON AUTOR:" + author)
        print("OBTENIENDO CON TITULO:" + title)
        for recipe in RecipesHandler.recipes:
            if (recipe.title == title and recipe.author == author):
                return recipe

    def getRecipesAsList(recipes):
        list = {}
        i = 0
        for recipe in recipes:
            list[i] = recipe.getRecipeAsList()
            i = i + 1
        return list
