
class Game:
    def __init__(self, id):
        self.player1_went = False
        self.player2_went = False
        self.ready = False
        self.id = False
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0
        self.possible_moves = ['ROCK', 'PAPER', 'SCISSORS']

    def get_player_moves(self, player):
        '''
        :param player: [0, 1]
        :return: Move
        '''
        return self.moves[player]

    def player(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.player1_went = True
        else:
            self.player2_went = True

    def are_players_connected(self):
        return self.ready

    def did_both_go(self):
        return self.player1_went and self.player2_went

    def determine_winner(self):
        player1_move, player2_move = self.moves[0].upper(), self.moves[1].upper()
        if (p1_index := self.possible_moves.index(player1_move)) < (p2_index := self.possible_moves.index(player2_move)):
            if p1_index == 0 and p2_index == 2:
                winner = 0
            else:
                winner = 1
        elif (p1_index := self.possible_moves.index(player1_move)) > (p2_index := self.possible_moves.index(player2_move)):
            if p2_index == 0 and p1_index == 2:
                winner = 1
            else:
                winner = 0
        else:
            winner = -1
        return winner

    def reset_went(self):
        self.player1_went = False
        self.player2_went = False
