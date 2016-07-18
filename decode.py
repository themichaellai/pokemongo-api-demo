import json
import pokemon_pb2
import sys


with open('pokemon.json', 'r') as f:
    pokemon = json.loads(f.read())


def decode_heartbeat(content):
    p_ret = pokemon_pb2.ResponseEnvelop()
    p_ret.ParseFromString(content)

    payload = p_ret.payload[0]
    heartbeat = pokemon_pb2.ResponseEnvelop.HeartbeatPayload()
    heartbeat.ParseFromString(payload)
    return heartbeat


def nearby_info(nearby_pokemon):
    pokemon_info = pokemon[nearby_pokemon.pokemon.PokemonId - 1]
    return {
        'latitude': nearby_pokemon.Latitude,
        'longitude': nearby_pokemon.Longitude,
        'name': pokemon_info['Name'],
        'despawn_in': nearby_pokemon.TimeTillHiddenMs / 1000,
    }


def parse_nearby(heartbeat):
    return [nearby_info(pokeman) for c in heartbeat.cells
            for pokeman in c.WildPokemon]


def parse_response_pokemon(content):
    heartbeat = decode_heartbeat(content)
    return parse_nearby(heartbeat)


if __name__ == '__main__':
    # content = sys.stdin.read()
    with open(sys.argv[1], 'r') as f:
        content = f.read()
    heartbeat = decode_heartbeat(content)
    near = parse_nearby(heartbeat)
    print near
    sys.stdout.flush()
