class LanguageBoundsInterface:
    """This interface is used to define different properties and implementation of a language.
These properties will create a ruleset for a language, which will be the bounds an algorithm
can work in the given context."""

    ########## Variables ##########

    _NULL_PHENOME_INDICATOR = None # Phenome representation of an unknown phenome
    _SIMILARITY_THRESHOLD = 0.2 # The threshold that must be passed for a word to be considered similar. Scaled from 0-1.
    MULTI_TOKEN_INDICATOR = None # Character used to identify when a token has multiple words. This functionality is specific to a corpus. Must be changed if corpus is changed.
    vowelphenomes = None # Contains all phenomes that produce vowel-related sounds for this language.
    
    ###############################

    ########## Constructor ##########

    def __init__(self, sensitivity):
        self._SIMILARITY_THRESHOLD = sensitivity

    #################################

    def getphenomes(self, arg):
        """Returns all phenome-lists related to the token."""
        pass

    def hypernyms(self, arg):
        """Returns all hypernyms related to the token. ('context' is the representation of the phrase in collection form.)"""
        pass

    def hyponyms(self, arg):
        """Returns all hyponyms related to the token. ('context' is the representation of the phrase in collection form.)"""
        pass

    def messagefail(self, input):
        """Produces the fail message to print to users in this language if the process cannot return a value."""
        pass

    def messageonlyresult(self, arg):
        """Produces a indicator message if only one result was possible from the input parameters given."""
        pass
    
    def messagetopresult(self, resultlen, requestedresultcount):
        """Produces the top 'x' results message to users in this language if the process has multiple results."""
        pass

    def similarity(self, arg, arg2):
        """Returns a token similarity score based on language-based weights. Used for determining optimal replacement for
        contexts."""
        pass

    def split(self, arg):
        """Returns an ordered list of tokens, split at delimiters based off of the the language context settings."""
        pass
