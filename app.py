# app.py
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

@app.route('/getreceta/', methods=['GET'])
def respond():
    name = request.args.get("nombre", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    if not name:
        response["ERROR"] = "No ha ingreso un nombre de receta a buscar"
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    else:
        response["MESSAGE"] = f"Estamos buscando tu receta '{name}', ten paciencia"
        #Buscar en el array recetas aqui en python
        #etc

    # Return the response in json format
    return jsonify(response)

@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

# A welcome message to test our server
@app.route('/')
def index():
    return render_template("example.html")

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
