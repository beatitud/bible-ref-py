from scriptures.text import Text
from .text import text

# text = "(Jn 17, 21) " + \
#        "(1 P 3, 8) " + \
#        "(cf. Jn 18, 33b-37) " + \
#        "(cf. Jc 2, 18) " + \
#        "(cf. Rm 8, 16). " + \
#        "(Ep 6, 23) " + \
#        "(1 Co 12, 13) " + \
#        "(cf. Ep 2, 14-16) " + \
#        "(cf. Ph 1, 6). " + \
#        "(cf. Ps 138, 1). " + \
#        "(cf. Jn 9, 5) " + \
#        "(v. 49) " + \
#        "Ez 13, 9 " + \
#        "Ézéchiel 13, 12 " + \
#        "Jr 3, 5 " + \
#        "Osee 1"

text = Text(text, language='fr', canon='catholic')
print(text)

for ref in text.extract_refs(guess=True):
    print(str(ref))

