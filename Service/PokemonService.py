from flask import jsonify
import random
import requests
import json
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO
import os

from Model.Pokemon import Pokemon
from Model.PokemonResponseData import PokemonResponseData
from Model.PokemonVerifyData import PokemonVerifyData

BASE_URL = "https://pokeapi.co/api/v2/pokemon/"
IMAGE_FOLDER = 'images'
answer_pokemon = Pokemon(None)


class PokemonService:

    def get_pokemons(self, app):

        random_numbers = random.sample(range(1, 51), 4)

        # Assign the random integers to four variables
        first_random_number, second_random_number, third_random_number, fourth_random_number = random_numbers

        pokemon_id = first_random_number  #assigning the first random id to be our pokemon (correct one)

        pokemon_response = self.get_pokemon_data(pokemon_id)  #obtaining the data of first pokemon
        pokemon = self.build_pokemon_from_response(pokemon_id, pokemon_response,
                                                   app)  #building the pokemon object from the data
        pokemon.set_is_answer(True)  #making the pokemon the answer for the question

        global answer_pokemon  #keeping it in a variable to use for the next end point (verification)
        answer_pokemon = pokemon

        pokemons_response_data = PokemonResponseData(pokemon)

        self.build_and_add_all_pokemons_list(pokemons_response_data, pokemon, second_random_number, third_random_number,
                                             fourth_random_number, app)  #build a list of all the pokemons

        return jsonify(pokemons_response_data.to_dict())

    def verify_pokemon(self, pokemon_id, name):
        pokemon_verify_data = PokemonVerifyData(answer_pokemon.get_name(), answer_pokemon.get_original_image_uri())
        if answer_pokemon is not None:
            if answer_pokemon.get_id() == pokemon_id:
                pokemon_verify_data.set_is_answer_correct(True)
                pokemon_verify_data.set_display_message("Congratulations! Your guess is correct!")
            else:
                pokemon_verify_data.set_is_answer_correct(False)
                pokemon_verify_data.set_display_message("Sorry, Your guess is incorrect!")
        return jsonify(pokemon_verify_data.to_dict())

    def get_pokemon_data(self, pokemon_id):
        url = self.create_http_request(pokemon_id)
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for non-200 status codes
        except requests.exceptions.RequestException as e:
            print(f"Exception occurred: {e}")
            return None
        return response

    def build_pokemon_from_response(self, pokemon_id, response, app):
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
                silhouette_image = self.convert_image_to_silhouette(pokemon.get_original_image_uri(), app)
                silhouette_image_uri = self.save_silhouette_image(pokemon.get_id(), silhouette_image, app)
                pokemon.set_silhouette_image_uri(silhouette_image_uri)
        return pokemon

    def build_and_add_all_pokemons_list(self, pokemon_response_data, pokemon, second_random_number, third_random_number,
                                        fourth_random_number, app):
        pokemon_response = None
        random_numbers = random.sample(range(4), 4)

        # Assign the random integers to four variables
        index_one, index_two, index_three, index_four = random_numbers #index_one doesn't mean the first element's in list. etc.

        # Add the initial pokemon to the list
        pokemon_response_data.add_pokemon(index_one, pokemon)

        # Get data for the second random number
        pokemon_response = self.get_pokemon_data(second_random_number)
        pokemon = self.build_pokemon_from_response(second_random_number, pokemon_response, app)
        pokemon_response_data.add_pokemon(index_two, pokemon)

        pokemon_response = self.get_pokemon_data(third_random_number)
        pokemon = self.build_pokemon_from_response(third_random_number, pokemon_response, app)
        pokemon_response_data.add_pokemon(index_three, pokemon)

        pokemon_response = self.get_pokemon_data(fourth_random_number)
        pokemon = self.build_pokemon_from_response(fourth_random_number, pokemon_response, app)
        pokemon_response_data.add_pokemon(index_four, pokemon)

    def create_http_request(self, pokemon_id):
        url = BASE_URL + str(pokemon_id)
        print(url)
        return url

    def convert_image_to_silhouette(self, url, app):
        self.create_image_folder(app)
        image_url = url
        response = requests.get(image_url)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to download image'}), 400

        image = Image.open(BytesIO(response.content))

        silhouette_image = image.convert("L")  # This part should be replaced by the image conversion to silhouette

        return silhouette_image

    def create_image_folder(self, app):
        global IMAGE_FOLDER
        if not os.path.exists(IMAGE_FOLDER):
            os.makedirs(IMAGE_FOLDER)
        app.config['IMAGE_FOLDER'] = IMAGE_FOLDER

    def save_silhouette_image(self, pokemon_id, silhouette_image, app):
        filename = 'silhouette_image' + str(pokemon_id) + '.png'
        save_path = os.path.abspath(os.path.join(app.config['IMAGE_FOLDER'], filename))

        # Save the silhouette image locally
        silhouette_image.save(save_path)

        # Return the path of the saved silhouette image
        return save_path
