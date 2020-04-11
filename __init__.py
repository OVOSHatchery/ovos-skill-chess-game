from mycroft import MycroftSkill, intent_file_handler


class Chess(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('chess.intent')
    def handle_chess(self, message):
        self.speak_dialog('chess')


def create_skill():
    return Chess()

