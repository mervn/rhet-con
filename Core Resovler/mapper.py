class Mapper:
    """This module takes a user-input string and chunks it into formatted tuples which
contains relevant data for all essential pieces of string."""

    def maptolist(self, arg, langbound):
        """Returns formatted-tuple containing relevant processing data for each token.""" #update
        return self._internalmap(arg, langbound)

    def _internalmap(self, arg, langbound):
        # Internally seperates the string into relevant tokens. # update
        return langbound.split(arg)
