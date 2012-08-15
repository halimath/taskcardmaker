
class CamelCaseHyphenator (object):
    def hyphenate (self, word):
        syliables = []
        syliable_begin = 0

        i = len(word) - 1
        for i in range(1, len(word)):
            if word[i].istitle():
                syliables.append(word[syliable_begin:i])
                syliable_begin = i

        syliables.append(word[syliable_begin:i + 1])


        return syliables

