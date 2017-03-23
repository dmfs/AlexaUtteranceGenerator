import re
import fileinput
import json

def parseFile(f):

  currentIntent = ""
  # initialize intents with the mandatory defaults
  intents = {"AMAZON.HelpIntent":{}, "AMAZON.StopIntent":{}, "AMAZON.CancelIntent": {}}

  for line in f:
    line = line.rstrip()
    if len(line) == 0 or line[0] == '#':
      # ignore empty lines and lines starting with # 
      continue

    if line[-1:] is ":":
      # we have an intent
      currentIntent = line[:-1]
      intents[currentIntent] = {}
      continue

    if line[0] is not " ":
      raise Exception("utterances must start with a space char: {}".format(line))

    if len(currentIntent) == 0: 
      raise Exception("no intent specified")
    slots, utterances = expandLine(currentIntent, line[1:])

    if slots:
      if not "slots" in intents[currentIntent]:
        intents[currentIntent]['slots'] = {}
      intents[currentIntent]['slots'].update(slots)
      
    for u in utterances:
      print (u)

  print ("--------------- snip ----------------")
  print (json.dumps({"intents": [{"intent": name, "slots": [{"name": n, "type": t} for n, t in value.get("slots", {}).items()]} for name, value in intents.items()]}, indent=2, sort_keys=True))

def expandLine(intent, line):
  slots, utterance = expandUtterance(line)
  return slots, ["{} {}".format(intent, u) for u in utterance]


def expandUtterance(utterance):
  slots, utterance = collectSlots(utterance)
  return slots, [alternative for optional in expandOptionals(utterance) for alternative in expandAlternatives(optional)]


def expandOptionals(utterance):
  if "[" in utterance:
    return [re.sub("\[([^\[\]]+)\]","\g<1>", utterance), re.sub("\[([^\[\]]+)\]","", utterance)]
  return [utterance]

def expandAlternatives(utterance):
  if "(" in utterance:
    m = re.search(r'\(([^\(\)]+)\)', utterance)
    if not m:
      return [utterance]
    match = m.group(0)
    words = m.group(1).split("|")
    return [a for w in words for a in expandAlternatives(utterance.replace(match, w))]
  return [utterance]


def collectSlots(utterance):
  p = re.compile("\{([\w.]+):(\w+)\}")
  return dict([(a, b) for b,a in p.findall(utterance)]), p.sub(lambda m: "{{{}}}".format(m.group(2)), utterance)


with fileinput.input() as f:
   parseFile(f)
