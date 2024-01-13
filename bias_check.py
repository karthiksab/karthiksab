
# BIAS
from flair.models import TARSClassifier
from flair.data import Sentence

def bias_identify(response):
  classes = ["racial bias","gender bias"]
  tar = TARSClassifier.load('tars-base')
  sentence = Sentence(response)
  print(sentence)
  classes = ["gender stereotype","race stereotype"]
  tar.predict_zero_shot(sentence, classes)

  return sentence.score

print(bias_identify ("Ethiopia is an African country. The people here are all runners"))
