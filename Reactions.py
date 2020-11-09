class Reaction:
    def __init__(self, icon, text):
        self.icon = icon
        self.text = text


    def recipeAsList(self):
        return {
            "icon": self.icon,
            "text": self.text
        }

class ReactionsHandler:
    reactions = []

    #0: sucess
    #1: repeated text
    @staticmethod
    def addReaction(icon, text):
        for reaction in ReactionsHandler.reactions:
            if reaction.text == text:
                return 1

        ReactionsHandler.reactions.append(Reaction(icon, text))
        return 0

    #0: sucess
    #1: no reaction found
    @staticmethod
    def removeReaction(text):
        for reaction in ReactionsHandler.reactions:
            if reaction.text == text:
                ReactionsHandler.reactions.remove(reaction)
                return 0
        return 1


    @staticmethod
    def modifyReaction(pastText,icon,text):
        theReaction = ReactionsHandler.geatReaction(text)

        if (theReaction and pastText != text):
            return 1

        for reaction in ReactionsHandler.reactions:
            if reaction.text == pastText:
                reaction.icon = icon
                reaction.text = text
                return 0
        return 2



    @staticmethod
    def geatReaction(text):
        for reaction in ReactionsHandler.reactions:
            if reaction.text == text:
                return reaction
        return None
