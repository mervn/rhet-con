from Interfaces.rulebounds import RuleBoundsInterface

class AssonanceRuleContext(RuleBoundsInterface):
    """Defines the properties and rules of the assonance rhetorical figure."""

    def _applyrule(self, sourcedata, tokentargetcount, langbound):
        """Trim interal-map token list to only retain tokens that constrain to the assonance ruleset."""

        phenomeselect = []
        for phenomeset in sourcedata:
            if phenomeset in langbound.vowelphenomes:
                #run proportion algorithm
                setrep = sourcedata[phenomeset]
                if tokentargetcount <= len(setrep):
                    phenomeselect.append(sourcedata[phenomeset])

        # Return selection
        if not phenomeselect:
            return None
        else:
            return phenomeselect

    def _applyscan(self, sourcematrix, langbound):
        """Scan a token-matrix and return a dataset that holds information on the phenome frequency of assonance
        in the matrix."""

        dataset = {} # Dicitonary is of type 'char' -> dict{int -> list[str]}'

        for index, item in enumerate(sourcematrix): # going through each token
            for content in item: # going through synonym content of each token

                phenomelists = self._getsourcephenome(content, langbound) # generate phenomes for alliteration evaluation
                for phenomes in phenomelists: # going through each phenome list for token (some tokes may have multiple pronounciations)

                    relevantphenome = phenomes[0] # use the FIRST phenome because this is assonance

                    if dataset.get(relevantphenome, None) is None: # if letter has NOT been scanned previously, create an entry
                       dataset[ relevantphenome ] = {} # Dictionary will contain key-value pairs corresponding to the index and the list of words available.
                       dataset[ relevantphenome ] [index] = [content]

                    else:
                        if dataset[ relevantphenome ].get(index, None) is None: # if an entry for THIS index has NOT been created, create one.
                            dataset[ relevantphenome ] [index] = [content]
                        else:
                            if content not in dataset[ relevantphenome ] [index]:
                                dataset[ relevantphenome ] [index].append(content)
                                
        return dataset

    def _getsourcephenome(self, evaltoken, langbound):
        """Returns a phenome value for a string-token."""

        phenomeform = langbound.getphenomes(evaltoken)
        return phenomeform


    def _getrelevantsynonyms(self, tokenlist, sourcetoken, langbound):
        """Returns a token-list of the original context and synonyms that are relevant, if applicable."""

        relevant = [sourcetoken] # original token is always first within the collection

        # Add all relevant synonyms to evaluation list as strings

        hypernyms = langbound.hypernyms(tokenlist, sourcetoken)
        hyponyms = langbound.hyponyms(tokenlist, sourcetoken)

        if hypernyms is not None:
            relevant.extend(hypernyms)
        if hyponyms is not None:
            relevant.extend(hyponyms)

        return relevant

    def _internalmap(self, tokenlist, langbound):
        """Map relevant replacement tokens to a matrix. This return token-matrix will have a one-to-to corresspondence
        to the passed tokenlist argument."""

        replacements = []
        for token in tokenlist:
            similar = self._getrelevantsynonyms(tokenlist, token, langbound)
            replacements.append(similar)

        return replacements

    def evaluate(self, tokenlist, replacementquota, langbound):
        if replacementquota < 1: # Nothing will be applied to the target list. Do not process.
            return None

        # Map and chart data for rule application
        preprocess = self._internalmap(tokenlist, langbound)
        process = self._applyscan(preprocess, langbound)

        # Apply rule and return data
        postprocess = self._applyrule(process, replacementquota, langbound)
        return postprocess