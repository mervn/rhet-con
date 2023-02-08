import heapq

class Analyzer:
    """Takes a rule-output and applies it to the target-input while attempting to retain the original meaning of the input as much as possible."""

    def _checkaccuracy(self, bestfitdata):
        """Takes a bestfitted output-slice and scores it on its accuracy when compared to original sentence."""

        if not bestfitdata:
            return None
        elif len(bestfitdata) is 1:
            return bestfitdata[0] # only one possible return
        else:
            
            accuracyheap = []
            for collection in bestfitdata:
                accuracy = 0 # reset every iteration
                for item in collection:
                    accuracy += item[0] # the first value in every tuple is expected to be accuracy score.

                heapq.heappush(accuracyheap, (accuracy, collection))

            return accuracyheap.nlargest(len(accuracyheap) - 1, accuracyheap)[0] # contains all values in highest to lowest order, but only returns highest

    def _checkbestfit(self, input, outputslice, langbound, replacementquota):
        """Takes a index to word-list mapping and selects the word from the list that retains the most sentence meaning. If no word applies, there will be no word
        replacement for that slot."""

        bestfitinorder = [] # Used as a heapq to sort by highest scores.
        for index in outputslice: # each replacement index in dict

            tokenselect = None
            highestscore = 0 # Used to select best word, resets on every changed index.

            for token in outputslice[index]: # each word in replacement index
                compareto = input[index] #corressponding index in original input
                score = langbound.similarity(input, compareto, token)

                if score[0] and highestscore < score[1]: # Does satisfy similarity criteria?
                    tokenselect = token
                    highestscore = score[1]

            if tokenselect: # After evaluation, check if there are any valid tokens to use.
                heapq.heappush(bestfitinorder, (highestscore, index, tokenselect)) # Acts as a priority queue and orders values from lowest to highest

        # Returning
        if len(bestfitinorder) < replacementquota: # Not enough values to return, replacements are invalid
            return None
        else:
            return heapq.nlargest(int(replacementquota), bestfitinorder)

    def _construct(self, originalinput, tokenchain, langbound, requestedresults): # add variable top X accurate results 
        """Converts a token list and bestfit data into a readable string."""

        convergence = []
        result = " "
        empty = " " # placeholder to perform syntax operations on

        if tokenchain is None:
            result = langbound.messagefail(originalinput)

        else:
            convergence = self._replacetokens(originalinput, tokenchain)
            result = langbound.messageonlyresult(empty.join(convergence))

        return result

    def _internalmap(self, originalinput, ruleoutput, langbound, replacementquota):
        """Maps each rule-output dictionary to be checked for bestfit."""

        mapping = []

        if ruleoutput is not None:
            for outs in ruleoutput: # Iterate through each output dict avaliable
                trimmed = self._checkbestfit(originalinput, outs, langbound, replacementquota)
                if trimmed is not None:
                    mapping.append(trimmed)

        return mapping

    def _replacetokens(self, originalinput, tokenchain):
        """Replaces tokens at targeted indicies in the original input from tokenchain, and returns a list of the results. This algorithm expects tokenchain to be a list."""

        for item in tokenchain: # Tuples containing (score, index, token)
            originalinput[item[1]] = item[2] # works because indicies were marked from beginning of process

        return originalinput # this is after modifications
            
    def analyze(self, originalinput, ruleoutput, langbound, replacementquota, topresults = 1):
        """Applies a rule-output to a target input and attempts to retain input meaning. Rule output is expected to be in (float, list[ dict(int, list[str]) ]) format."""

        preprocess = self._internalmap(originalinput, ruleoutput, langbound, replacementquota)
        process = self._checkaccuracy(preprocess)
        postprocess = self._construct(originalinput, process, langbound, topresults)
        return postprocess
