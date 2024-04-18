class PokemonResponseData:

    def __init__(self, pokemon):
        self._pokemon = pokemon
        self._all_pokemons = []

    def get_pokemon(self):
        return self._pokemon

    def get_all_pokemons(self):
        return self._all_pokemons

    def set_all_pokemons(self, all_pokemons):
        self._all_pokemons = all_pokemons

    def add_pokemon(self, index, pokemon):
        self._all_pokemons.insert(index, pokemon)

    def to_dict(self):
        return {
            "pokemon": self._pokemon.to_dict(),
            "allPokemons": [pokemon.to_dict() for pokemon in self._all_pokemons]
        }
