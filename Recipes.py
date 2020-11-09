import uuid

class Recipe:
    def __init__(self, author, titulo, abstract, ingredients, procedure, time, image, comments, reactions):
        self.author = author
        self.title = titulo
        self.abstract = abstract
        self.ingredients = ingredients
        self.procedure = procedure
        self.time = time
        self.image = image
        self.comments = comments
        self.reactions = reactions
        self.uid = uuid.uuid1().hex

    def getRecipeAsList(self):
        return {
            "author": self.author,
            "title": self.title,
            "abstract": self.abstract,
            "ingredients": self.ingredients,
            "procedure": self.procedure,
            "time": self.time,
            "image": self.image,
            "comments": self.comments,
            "reactions": self.reactions,
            "uid": self.uid
        }

    def addComment(self, author, author_type, body, date):
        self.comments.append( {
            "author": author,
            "author_type": author_type,
            "body": body,
            "date": date
        })

class RecipesHandler:
    recipes = []

    r1 = Recipe("Autor1", "Titulo1", "Res1", "1ingr1,1ingr2", "proced1", "time1","https://i.ytimg.com/vi/fVh-h6K-zfY/maxresdefault.jpg",
                [
                {"author": "Pitito", "author_type":"user", "body": "This is a nais receta mai frend", "date": "01/04/2020 15:40:09"},
                {"author": "Pitito2","author_type":"admin", "body": "This rend", "date": "01/04/2020 15:50:09"}
                ],
                {})


    recipes.append(r1)

    @staticmethod
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
    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def getRecipeByAuthorAndTitle(author, title):
        print("OBTENIENDO CON AUTOR:" + author)
        print("OBTENIENDO CON TITULO:" + title)
        for recipe in RecipesHandler.recipes:
            if (recipe.title == title and recipe.author == author):
                return recipe

    @staticmethod
    def getRecipesAsList(recipes):
        list = {}
        i = 0
        for recipe in recipes:
            list[i] = recipe.getRecipeAsList()
            i = i + 1
        return list

    @staticmethod
    def getRecipeByUID(uid):
        print("Searching for uid " + uid)
        for recipe in RecipesHandler.recipes:
            if recipe.uid == uid:
                return recipe
        return None
