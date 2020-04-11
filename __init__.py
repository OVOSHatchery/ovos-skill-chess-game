from mycroft import MycroftSkill, intent_file_handler
import chess
from stockfish import Stockfish


class Chess(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.board = chess.Board()
        self.engine = Stockfish
        self.characters_value = self.translate_namedvalues('characters.value')
        self.color_value = self.translate_namedvalues('color.value')


    @intent_file_handler('chess.intent')
    def handle_chess(self, message):
        self.log.info(self.color_value["white"])
        if not self.settings["savegame"] is "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1":
            self.speak_dialog('chess')
            a = self.ask_yesno("you.have")
            if a == "yes":
                self.board = chess.Board(self.settings["savegame"])
            else:
                color = self.get_response("ask.color")
                if color in self.color_value["white"]:
                    self.log.info("color white")
                    self.board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
                elif color in self.color_value["black"]:
                    self.log.info("color black")
                    self.board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
                else:
                    self.log.info("no color")
        self.log.info("\n"+str(board))


    @intent_file_handler('turn.characters.intent')
    def handle_characters_turn(self, message):
        if message.data.get("from"):
            begin = message.data.get("from")
        else:
            self.get_response("from")
        if message.data.get("to"):
            end = message.data.get("to")
        else:
            self.get_response("to")
        #if not begin or end:
        #    self.log.info(begin+" "+end)
        #    self.speak_dialog('no.turn')
        begin = begin.replace(" ", "")
        end = end.replace(" ", "")
        self.log.info(begin+" "+end)
        move = chess.Move.from_uci(begin+end)
        if move in board.legal_moves:
            board.push(move)
        else:
            self.speak_dialog('wrong.turn')
        self.log.info("\n"+str(board))
        self.turn()


    @intent_file_handler('save.intent')
    def handle_save(self, message):
        self.log.info("save game")
        self.settings["savegame"] = board.fen()
    

    def turn(self):
        result = self.engine.play(self.board, chess.engine.Limit(time=0.1))
        self.log.info("result "+str(result))
        board.push(result.move)
        character = self.characters_value["r"]
        begin = result[0]
        end = result[1]
        self.speak_dialog("turn", data={"character": character, "from": begin, "to": end})

    def shutdown(self):
        self.settings["savegame"] = board.fen()
        super(Chess, self).shutdown()


def create_skill():
    return Chess()

