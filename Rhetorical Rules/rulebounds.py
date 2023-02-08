class RuleBoundsInterface:
    """This interface is used to define different properties of a rhetorical figure generating algorithm.
These properties will create a ruleset for a rhectorical figure, allowing the algorithm to produce results relevant
to the user-request."""

    def evaluate(self, tokenlist, replacementquota):
        """Returns a dataset containing the best application of the rule to the original tokenlist using the proportion specified. This also means
        that certain conditions will have no return value."""
        pass

