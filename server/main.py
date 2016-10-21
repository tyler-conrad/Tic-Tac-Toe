"""
Stateless server implementation.
"""

from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.resource import Resource

from common import config
from common.model import board
from server.ai.minimax import alpha_beta


class GetMove(Resource):
    isLeaf = True

    def render_GET(self, request):
        # construct a Board from the requests query parameter
        old_board = board.from_string(request.args['board'][0])
        # return the best move
        return board.to_string(alpha_beta(old_board)[0][1])

if __name__ == '__main__':
    reactor.listenTCP(config.port, Site(GetMove()))
    reactor.run()
