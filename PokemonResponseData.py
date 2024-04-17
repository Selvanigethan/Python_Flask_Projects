class PokemonResponseData:

    def __init__(self, pokemon):
        self._pokemon = pokemon
        self._decoy_pokemons_list = []
        self._all_pokemons = []

    def get_pokemon(self):
        return self._pokemon

    def get_decoy_pokemons_list(self):
        return self._decoy_pokemons_list

    def get_all_pokemons(self):
        return self._all_pokemons

    def set_decoy_pokemons_list(self, decoy_pokemons_list):
        self._decoy_pokemons_list = decoy_pokemons_list

    def set_all_pokemons(self, all_pokemons):
        self._all_pokemons = all_pokemons

    def add_pokemon(self, pokemon):
        self._all_pokemons.append(pokemon)

    def to_dict(self):
        return {
            "pokemon": self._pokemon.to_dict(),
            "decoyPokemonsList": self._decoy_pokemons_list,
            "allPokemons": [pokemon.to_dict() for pokemon in self._all_pokemons]
        }
