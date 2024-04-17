class PokemonVerifyData:

    def __init__(self, correct_pokemon_name, correct_pokemon_image_uri):
        self._correct_pokemon_name = correct_pokemon_name
        self._correct_pokemon_image_uri = correct_pokemon_image_uri
        self._display_message = None
        self._is_answer_correct = False

    def get_correct_pokemon_name(self):
        return self._correct_pokemon_name

    def get_correct_pokemon_image_uri(self):
        return self._correct_pokemon_image_uri

    def get_display_message(self):
        return self._display_message

    def get_is_answer_correct(self):
        return self._is_answer_correct

    def set_display_message(self, display_message):
        self._display_message = display_message

    def set_is_answer_correct(self, is_answer_correct):
        self._is_answer_correct = is_answer_correct

    def to_dict(self):
        return {
            "correctPokemonName": self._correct_pokemon_name,
            "correctPokemonImageUri": self._correct_pokemon_image_uri,
            "displayMessage": self._display_message,
            "isAnswerCorrect": self._is_answer_correct
        }
