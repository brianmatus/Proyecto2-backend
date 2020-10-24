# app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from Recipes import Recipe as Recipe
from Recipes import RecipesHandler as RecipesHandler

from Users import User as User
from Users import UsersHandler as UsersHandler

import json

app = Flask(__name__)
CORS(app)
                                #########################################
                                #################RECIPES#################
                                #########################################


@app.route('/search_recipes/', methods=['GET'])
#0:sucess
#1: Missing title
#2: No recipe found
def search_recipes():
    data = json.loads(request.data)
    title = data['title']
    exactMatch = ['exactMatch']

    response = {}

    if not title:
        response["RESULT"] = "No ha ingreso un titulo de receta a buscar"
        response["RETURNCODE"] = 1
    else:
        foundRecipes = RecipesHandler.searchRecipes(title, exactMatch)

        if len(foundRecipes) == 0:
            response["RESULT"] = "No se encontraror recetas con ese nombre"
            response["RETURNCODE"] = 2
        else:

            asList = RecipesHandler.getRecipesAsList(foundRecipes)
            print(jsonify(asList))
            response["RESULT"] = asList
            response["RETURNCODE"] = 0

    response = jsonify(response)
    #response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/add_recipe/',methods=['POST'])
def add_recipe():
    data = json.loads(request.data)
    author = data['author']
    title = data['title']
    abstract = data['abstract']
    ingredients = data['ingredients']
    steps = data['steps']
    time = data['time']
    image = data['image']

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

@app.route('/remove_recipe/',methods=['POST'])
def remove_recipe():
    data = json.loads(request.data)
    title = data['title']


    result = RecipesHandler.removeRecipeByTitle(title)

    if result:
        return jsonify({
            "RESULT": f"Receta {title} eliminada correctamente",
            "RETURNCODE" : "0",
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "RESULT": f"No hay receta con titulo {title}",
            "RETURNCODE" : "1",
            "METHOD" : "POST"
        })


@app.route('/modify_recipe/', methods=['POST'])
#0: sucess
#1: Missing data
#2: Recipe with new title already exists
#3: Recipe doesn't exist
def modify_recipe():
    data = json.loads(request.data)
    pastTitle = data['pastTitle']
    author = data['author']
    title = data['title']
    abstract = data['abstract']
    ingredients = data['ingredients']
    steps = data['steps']
    time = data['time']
    image = data['image']
    commentaries = data['image']
    reactions = data['reactions']

    newRecipe = Recipe(author,title,abstract,ingredients,steps,time,image,commentaries, reactions)

    result = RecipesHandler.modifyRecipe(pastTitle, newRecipe)

    if result == 0:
        return jsonify({
            "RESULT": f"Receta {pastTitle} modificado con exito",
            "RETURNCODE" : "0",
            "METHOD" : "POST"
                })
    elif result == 2:
        return jsonify({
            "RESULT": f"Una receta ya existe con el nuevo titulo {title}",
            "RETURNCODE" : "2",
            "METHOD" : "POST"
                })
    elif result == 3:

        return jsonify({
            "RESULT": f"No existe una receta con titulo {pastTitle}",
            "RETURNCODE" : "3",
            "METHOD" : "POST"
        })

                                #########################################
                                ##################USERS##################
                                #########################################

@app.route('/login/', methods=['POST'])
#0: sucess
#1: Usuario no encontrado
#2: Contrasena invalida
#3: No se proporciono clave
#4: No se proporciono usuario
def login():
    data = json.loads(request.data)
    username = data['username']
    password = data['password']
    print(username)
    print(password)
    response = {}

    if username:
        if password:
            result = UsersHandler.login(username,password)
            if result == 0:
                response =  jsonify({
                    "RESULT": f"Iniciado sesion correctamente con {username}, bienvenido",
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
        else:
             response = jsonify({
                    "RESULT": "No se brindo contrasena",
                    "RETURNCODE" : "3",
                    "METHOD" : "POST"
            })
    else:
        response = jsonify({
            "RESULT": "No se brindo usuario",
            "RETURNCODE" : "4",
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
#0: sucess
#1: User already exist
def register_user():
    data = json.loads(request.data)
    name = data['name']
    lastname = data['lastname']
    username = data['username']
    password = data['password']
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
#0: sucess
#1: user is master user
#2: no user found
def remove_user():
    data = json.loads(request.data)
    username = data['username']


    if (username == "admin"):
        return jsonify({
            "RESULT": f"No se puede borrar al usuario maestro",
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
#0: sucess
#1: Missing data
#2: User with new username already exists
#3: user doesnt exist
def modify_user():
    data = json.loads(request.data)
    pastUsername = data['pastUsername']
    name = data['name']
    lastname = data['lastname']
    username = data['username']
    password = data['password']

    if (pastUsername == None or name == None or lastname == None or username == None or password == None ):

        return jsonify({
            "RESULT": "No se brindo toda la informacion necesaria",
            "RETURNCODE" : "1",
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
#0:sucess
#1:Missing username
#2: No users found
def search_users():
    data = json.loads(request.data)
    username = data['username']
    exactMatch = data['exactMatch']


    if (username == None):
        return jsonify({
                "RESULT": f"No se brindo un username para buscar",
                "RETURNCODE" : "1",
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
#0: sucess
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
#0: sucess
#1: no user found
def recover_password():

    data = json.loads(request.data)
    username = data['username']

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
    UsersHandler.addUser(User("Usuario","Maestro","admin","admin"))
    app.run(threaded=True, port=5000)


