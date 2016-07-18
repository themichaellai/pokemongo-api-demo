from datetime import datetime
from decode import parse_response_pokemon
from libmproxy.models import decoded


def response(context, flow):
    if 'rpc' in flow.request.path:
        with decoded(flow.response):
            pokemon = parse_response_pokemon(flow.response.body)

        append_str = '\n'.join(
            ['{} {},{} {}'.format(p['name'],
                                  p['latitude'],
                                  p['longitude'],
                                  p['despawn_in'])
             for p in pokemon])
        with open('pokelog', 'a') as log:
            log.write(datetime.now().isoformat())
            log.write('\n')
            log.write(append_str)
            log.write('\n\n')
