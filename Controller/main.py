from flask import Flask
from flask_cors import CORS
from Service.PokemonService import PokemonService


app = Flask(__name__)
CORS(app, origins='http://localhost:3000', allow_headers=['Content-Type'])

pokemon_service = PokemonService()


@app.route('/api/getpokemons', methods=['GET'])
def get_pokemons():
    return pokemon_service.get_pokemons(app)


@app.route('/api/verifypokemon/<int:pokemon_id>/<string:name>', methods=['GET'])
def verify_pokemon(pokemon_id, name):
    return pokemon_service.verify_pokemon(pokemon_id, name)


# api.add_resource(HelloWorld, "/helloworld")

if __name__ == "__main__":
    app.run(debug=True)
