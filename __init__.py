from mycroft import MycroftSkill, intent_file_handler
import chess

board = chess.Board()


class Chess(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.characters_value = self.translate_namedvalues('characters.value')
        self.play = True

    @intent_file_handler('chess.intent')
    def handle_chess(self, message):
        if self.play is True:
            self.speak_dialog('chess')
        else:
            color = self.get_response("ask.color")
            if color == "white":
                True
            elif color == "black":
                True


    @intent_file_handler('turn.characters.intent')
    def handle_turn(self, message):
        if message.data("from"):
            begin = message.data("from")
        else:
            self.get_response("from")
        if message.data.get("to"):
            end = message.data.get("to")
        else:
            self.get_response("to")
        if not begin or end:
            self.log.info(begin+end)
            self.speak_dialog('no.turn')
        else:
            begin.sorted(end, reverse=True).replace(" ", "")
            end.sorted(end, reverse=True).replace(" ", "")
            self.log.info(begin+end)
            move = chess.Move.from_uci(begin+end)
            board.push(move)


    @intent_file_handler('save.intent')
    def handle_turn(self, message):
        self.log.info("save game")
        True


    

    def turn(self):
        character = self.characters_value["r"]

def create_skill():
    return Chess()

