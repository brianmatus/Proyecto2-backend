# app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from Recipes import Recipe as Recipe
from Recipes import RecipesHandler as RecipesHandler

from Users import User as User
from Users import UsersHandler as UsersHandler

from datetime import datetime

import json

app = Flask(__name__)
CORS(app)
                                #########################################
                                #################RECIPES#################
                                #########################################


@app.route('/search_recipes/', methods=['GET','POST'])
#0:success
#-1: Missing title
#1: No recipe found
def search_recipes():
    data = json.loads(request.data)
    title = data.get('title', "*")
    exactMatch = data.get('exactMatch', "false")

    response = {}
    if (not title or title == ""):
        return jsonify({
            "RESULT": "No ha brindado toda la informacion necesaria",
            "RETURNCODE" : "-1",
            "METHOD" : "POST"
        })

    foundRecipes = RecipesHandler.searchRecipes(title, exactMatch)
    if len(foundRecipes) == 0:
        response["RESULT"] = "No se encontraron recetas con ese nombre"
        response["RETURNCODE"] = 1
    else:

        asList = RecipesHandler.getRecipesAsList(foundRecipes)
        print(jsonify(asList))
        response["RESULT"] = asList
        response["RETURNCODE"] = 0

    response = jsonify(response)
    return response

@app.route('/add_recipe/',methods=['POST'])
#0: success
#-1: Missing data
#1: title already exist
def add_recipe():
    data = json.loads(request.data)
    author = data.get('author', None)
    title = data.get('title', None)
    abstract = data.get('abstract', None)
    ingredients = data.get('ingredients', None)
    steps = data.get('steps', None)
    time = data.get('time', None)
    image = data.get('image', None)


    list = [author,title,abstract,ingredients,steps,time,image]
    for element in list:
        if (not element or element == ""):
            return jsonify({
            "RESULT": "No ha brindado toda la informacion necesaria",
            "RETURNCODE" : "-1",
            "METHOD" : "POST"
            })

    result = RecipesHandler.addRecipe(Recipe(author,title,abstract,ingredients,steps,time,image,[], []))

    if result:
        return jsonify({
            "RESULT": f"Receta {title} publicada correctamente",
            "RETURNCODE" : "0",
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "RESULT": f"Una receta con titulo {title} ya se encuentra publicada",
            "RETURNCODE" : "1",
            "METHOD" : "POST"
        })



@app.route('/getRecipeByUID/',methods=['POST'])
#0: success
#-1: Missing data
#1: no UID found
def getRecipeByUID():
    data = json.loads(request.data)
    uid = data.get('uid', None)

    if (uid == None or uid == ""):
        return jsonify({
            "RESULT": "No ha brindado toda la informacion necesaria",
            "RETURNCODE" : "-1",
            "METHOD" : "POST"
            })

    recipe = RecipesHandler.getRecipeByUID(uid)
    if (recipe == None):
        return jsonify({
            "RESULT": f"No se encontro ninguna receta con uid {uid}",
            "RETURNCODE" : "1",
            "METHOD" : "POST"
        })

    return jsonify({
            "RESULT": RecipesHandler.getRecipesAsList([recipe]),
            "RETURNCODE" : "0",
            "METHOD" : "POST"
        })

@app.route('/remove_recipe/', methods=['POST'])
def remove_recipe():
    data = json.loads(request.data)
    title = data.get('title', None)
    author = data.get('author', None)

    if (not title or title == "" or not author or author == ""):
        return jsonify({
            "RESULT": "No ha brindado toda la informacion necesaria",
            "RETURNCODE" : "-1",
            "METHOD" : "POST"
        })


    result = RecipesHandler.removeRecipeByTitleAndAuthor(title, author)

    if result:
        return jsonify({
            "RESULT": f"Receta {title} eliminada correctamente",
            "RETURNCODE" : "0",
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "RESULT": f"No hay receta con titulo {title} y author {author}",
            "RETURNCODE" : "1",
            "METHOD" : "POST"
        })


@app.route('/modify_recipe/', methods=['POST'])
#0: success
#-1: Missing data
#2: Recipe with new title already exists
#3: Recipe doesn't exist
def modify_recipe():
    data = json.loads(request.data)
    pastAuthor = data.get('pastAuthor', None)
    pastTitle = data.get('pastTitle', None)
    author = data.get('author', None)
    title = data.get('title', None)
    abstract = data.get('abstract', None)
    ingredients = data.get('ingredients', None)
    steps = data.get('steps', None)
    time = data.get('time', None)
    image = data.get('image', None)
    comments = data.get('comments', None)
    reactions = data.get('reactions', None)

    list = [pastAuthor, pastTitle, author, title, abstract, ingredients, steps, time, image, comments, reactions]
    for element in list:
        if (not element or element == ""):
            return jsonify({
                "RESULT": "No ha brindado toda la informacion necesaria",
                "RETURNCODE" : "-1",
                "METHOD" : "POST"
            })

    newRecipe = Recipe(author,title,abstract,ingredients,steps,time,image,comments, reactions)

    result = RecipesHandler.modifyRecipe(pastAuthor, pastTitle, newRecipe)

    if result == 0:
        return jsonify({
            "RESULT": f"Receta {pastTitle} modificado con exito",
            "RETURNCODE" : "0",
            "METHOD" : "POST"
                })
    elif result == 2:
        return jsonify({
            "RESULT": f"Una receta ya existe con el nuevo titulo {title} y autor {author}",
            "RETURNCODE" : "2",
            "METHOD" : "POST"
                })
    elif result == 3:

        return jsonify({
            "RESULT": f"No existe una receta con titulo {pastTitle} y autor {pastAuthor}",
            "RETURNCODE" : "3",
            "METHOD" : "POST"
        })





@app.route("/addComment/", methods=['POST'])
#0: success
#-1: Missing data
#1: Author-Recipe not found
def addComment():

    data = json.loads(request.data)

    author = data.get('author', None)
    body = data.get('body', None)

    recipeAuthor = data.get('recipeAuthor', None)
    recipeTitle = data.get('recipeTitle', None)


    list = [author,body,recipeAuthor,recipeTitle]
    for element in list:
        if (not element or element == ""):
            return jsonify({
                "RESULT": "No ha brindado toda la informacion necesaria",
                "RETURNCODE" : "-1",
                "METHOD" : "POST"
            })

    recipe = RecipesHandler.getRecipeByAuthorAndTitle(recipeAuthor, recipeTitle)
    if (recipe == None):
        return jsonify({
                "RESULT": "No existe esa combinacion autor-receta",
                "RETURNCODE" : "1",
                "METHOD" : "POST"
            })

    date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    recipe.addComment(author, body, date)

    return jsonify({
            "RESULT": "Comentario realizado correctamente",
            "RETURNCODE" : "0",
            "METHOD" : "POST"
        })

###########################################################################################################################
###############################################USERS#######################################################################
###########################################################################################################################

@app.route('/login/', methods=['POST'])
#0: success
#-1: Missing data
#1: Usuario no encontrado
#2: Contrasena invalida
def login():
    data = json.loads(request.data)
    username = data.get('username', None)
    password = data.get('password', None)
    response = {}

    if (not username or username == "" or not password or password == "") :
        return jsonify({
            "RESULT": "No ha brindado toda la informacion necesaria",
            "RETURNCODE" : "-1",
            "METHOD" : "POST"
        })


    result = UsersHandler.login(username,password)
    if result == 0:
        response =  jsonify({
            "RESULT": f"Iniciado sesion correctamente con {username}, bienvenido",
            "USERTYPE":UsersHandler.loggedUser.type,
            "RETURNCODE" : "0",
            "METHOD" : "POST"
        })
    elif result == 1:
        response = jsonify({
            "RESULT": f"No se ha encontrado ningun usuario con username {username}",
            "RETURNCODE" : "1",
            "METHOD" : "POST"
        })
    elif result == 2:
        response = jsonify({
            "RESULT": f"La contrasena ingresada para {username} no coincide con la registrada en el sistema",
            "RETURNCODE" : "2",
            "METHOD" : "POST"
        })
            
    #response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/logout/',methods=['POST'])
def logout():

    UsersHandler.loggedUser = None
    return jsonify({
        "RESULT": "Cerrado sesion con exito",
        "RETURNCODE" : "0",
        "METHOD" : "POST"
     })


@app.route('/register_user/', methods=['POST'])
#0: success
#-1: Missing data
#1: User already exist
def register_user():
    data = json.loads(request.data)
    name = data.get('name', None)
    lastname = data.get('lastname', None)
    username = data.get('username', None)
    password = data.get('password', None)

    list = [name,lastname,username,password]
    for element in list:
        if (not element or element == ""):
            return jsonify({
                "RESULT": "No ha brindado toda la informacion necesaria",
                "RETURNCODE" : "-1",
                "METHOD" : "POST"
            })

    newUser = User(name,lastname,username,password)

    result = UsersHandler.addUser(newUser)

    if result:
        return jsonify({
            "RESULT": f"Usuario {username} Registrado con exito",
            "RETURNCODE" : "0",
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "RESULT": f"Ya existe un usario con username {username}",
            "RETURNCODE" : "1",
            "METHOD" : "POST"
        })


@app.route('/remove_user/',methods=['POST'])\
#0: success
#-1: Missing data
#1: user is master user
#2: no user found
def remove_user():
    data = json.loads(request.data)
    username = data.get('username', None)



    if (not username or username == ""):
        return jsonify({
            "RESULT": "No ha brindado toda la informacion necesaria",
            "RETURNCODE" : "-1",
            "METHOD" : "POST"
        })



    if (username == "admin"):
        return jsonify({
            "RESULT": "No se puede borrar al usuario maestro",
            "RETURNCODE" : "1",
            "METHOD" : "POST"
        })


    result = UsersHandler.removeUserByUsername(username)

    if result:
        return jsonify({
            "RESULT": f"Usuario {username} eliminado correctamente",
            "RETURNCODE" : "0",
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "RESULT": f"No hay usuario con username {username}",
            "RETURNCODE" : "2",
            "METHOD" : "POST"
        })




@app.route('/modify_user/', methods=['POST'])
#0: success
#-1: Missing data
#2: User with new username already exists
#3: user doesnt exist
def modify_user():
    data = json.loads(request.data)
    pastUsername = data.get('pastUsername', None)
    name = data.get('name', None)
    lastname = data.get('lastname', None)
    username = data.get('username', None)
    password = data.get('password', None)

    list = [pastUsername,name,lastname,username,password]
    for element in list:
        if (not element or element == ""):
            return jsonify({
                "RESULT": "No ha brindado toda la informacion necesaria",
                "RETURNCODE" : "-1",
                "METHOD" : "POST"
            })


    newUser = User(name,lastname,username,password)

    result = UsersHandler.modifyUser(pastUsername, newUser)
    if result == 0:
        return jsonify({
            "RESULT": f"Usuario {pastUsername} modificado con exito",
            "RETURNCODE" : "0",
            "METHOD" : "POST"
                })
    elif result == 2:
        return jsonify({
            "RESULT": f"Un usuario ya existe con el nuevo username {username}",
            "RETURNCODE" : "2",
            "METHOD" : "POST"
                })
    elif result == 3:

        return jsonify({
            "RESULT": f"No existe un usario con username {pastUsername}",
            "RETURNCODE" : "3",
            "METHOD" : "POST"
        })


@app.route('/search_users/',methods=['GET'])
#0:success
#1:Missing username
#2: No users found
def search_users():
    data = json.loads(request.data)
    username = data['username']
    exactMatch = data['exactMatch']


    if (username == None):
        return jsonify({
                "RESULT": f"No se brindo un username para buscar",
                "RETURNCODE" : "-1",
                "METHOD" : "POST"
            })


    foundUsers = UsersHandler.searchUsers(username, exactMatch)

    if (len(foundUsers) == 0 ):
        return jsonify({
            "RESULT": f"No se encontro ningun usuario con los criterios dados",
            "RETURNCODE" : "2",
            "METHOD" : "POST"
        })


    asList = UsersHandler.getUsersAsList(foundUsers)
    print(jsonify(asList))
    return jsonify({
        "RESULT": asList,
        "RETURNCODE" : "0",
        "METHOD" : "POST"
    })



@app.route('/get_logged_user/',methods=['GET'])
#0: success
#1: no user
def get_logged_user():
    user = UsersHandler.loggedUser
    if (user == None):
        return jsonify({
            "RESULT": f"Ningun usuario ha iniciado sesion",
            "RETURNCODE" : "1",
            "METHOD" : "POST"
        })
    else:
        asList = user.getUserAsList()
        return jsonify({
            "RESULT": asList,
            "RETURNCODE" : "0",
            "METHOD" : "POST"
        })
        
    

@app.route('/recover_password/',methods=['POST'])
#0: success
#1: no user found
def recover_password():

    data = json.loads(request.data)
    username = data.get('username', None)

    if (not username or username == ""):
        return jsonify({
            "RESULT": "No ha brindado toda la informacion necesaria",
            "RETURNCODE" : "-1",
            "METHOD" : "POST"
        })

    user = UsersHandler.getUserByUsername(username)

    if (user == None):
        return jsonify({
            "RESULT": f"No existe ningun usuario con username {username}",
            "RETURNCODE" : "1",
            "METHOD" : "POST"
        })

    else:
        return jsonify({
            "RESULT": user.password,
            "RETURNCODE" : "0",
            "METHOD" : "POST"
        })
    

@app.route('/')
def index():
    return jsonify({
            "MESSAGE": "BackEnd Python CUK",
            "RETURNCODE" : "0",
            "METHOD" : "POST"
        })

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    UsersHandler.addUser(User("Usuario","Maestro","admin","admin","admin"))
    app.run(threaded=True, port=5000)
