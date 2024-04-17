from flask import Flask, jsonify
import random
import requests
import json
from urllib.parse import urljoin

from Pokemon import Pokemon
from PokemonResponseData import PokemonResponseData
from PokemonVerifyData import PokemonVerifyData

#from flask_restful import Api, Resource

app = Flask(__name__)

#api = Api(app)  # api = Flask(__name__)


#class HelloWorld(Resource):

BASE_URL = "https://pokeapi.co/api/v2/pokemon/"
answer_pokemon = Pokemon(None)


@app.route('/api/printtext', methods=['GET'])
def get_text():
    return {"data": "Hello world"}


@app.route('/api/getpokemons', methods=['GET'])
def get_pokemons():
    #return {"data": "Hello world"}
    first_random_number = random.randint(1, 50)
    second_random_number = random.randint(1, 50)
    third_random_number = random.randint(1, 50)
    fourth_random_number = random.randint(1, 50)

    pokemon_id = first_random_number

    pokemon_response = get_pokemon_data(pokemon_id)
    pokemon = build_pokemon_from_response(pokemon_id, pokemon_response)
    pokemon.set_is_answer(True)

    global answer_pokemon
    answer_pokemon = pokemon

    pokemons_response_data = PokemonResponseData(pokemon)

    build_and_add_all_pokemons_list(pokemons_response_data, pokemon, second_random_number, third_random_number,
                                    fourth_random_number)

    return jsonify(pokemons_response_data.to_dict())


@app.route('/api/verifypokemon/<int:pokemon_id>/<string:name>', methods=['GET'])
def verify_pokemon(pokemon_id, name):
    pokemon_verify_data = PokemonVerifyData(answer_pokemon.get_name(), answer_pokemon.get_original_image_uri())
    if answer_pokemon is not None:
        if answer_pokemon.get_id() == pokemon_id:
            pokemon_verify_data.set_is_answer_correct(True)
            pokemon_verify_data.set_display_message("Congratulations! Your guess is correct!")
        else:
            pokemon_verify_data.set_is_answer_correct(False)
            pokemon_verify_data.set_display_message("Sorry, Your guess is incorrect!")
    return jsonify(pokemon_verify_data.to_dict())


def create_http_request(pokemon_id):
    url = BASE_URL + str(pokemon_id)
    print(url)
    return url


def get_pokemon_data(pokemon_id):
    url = create_http_request(pokemon_id)
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for non-200 status codes
    except requests.exceptions.RequestException as e:
        print(f"Exception occurred: {e}")
        return None
    return response


def build_pokemon_from_response(pokemon_id, response):
    pokemon = Pokemon(pokemon_id)

    try:
        json_data = json.loads(response.text)
    except Exception as exception:
        print(f"Exception occurred: {exception}")
        return None

    if 'name' in json_data:
        pokemon.set_name(json_data['name'])

    if 'sprites' in json_data:
        artwork_url = json_data['sprites']['other']['official-artwork']['front_default']
        if artwork_url:
            pokemon.set_original_image_uri(urljoin(BASE_URL, artwork_url))

    return pokemon


def build_and_add_all_pokemons_list(pokemon_response_data, pokemon, second_random_number, third_random_number,
                                    fourth_random_number):
    pokemon_response = None

    # Add the initial pokemon to the list
    pokemon_response_data.add_pokemon(pokemon)

    # Get data for the second random number
    pokemon_response = get_pokemon_data(second_random_number)
    pokemon = build_pokemon_from_response(second_random_number, pokemon_response)
    pokemon_response_data.add_pokemon(pokemon)

    pokemon_response = get_pokemon_data(third_random_number)
    pokemon = build_pokemon_from_response(third_random_number, pokemon_response)
    pokemon_response_data.add_pokemon(pokemon)

    pokemon_response = get_pokemon_data(fourth_random_number)
    pokemon = build_pokemon_from_response(fourth_random_number, pokemon_response)
    pokemon_response_data.add_pokemon(pokemon)


#api.add_resource(HelloWorld, "/helloworld")

if __name__ == "__main__":
    app.run(debug=True)
