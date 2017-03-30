# Alexa Utterance Generator

A quick and dirty python script to create Alexa utterance and intent files from a more compact representation.

The script returns a list of utterances as well as a JSON snippet of intents.

## Syntax

The syntax is rather simple. For each intent write the intent name followed by a colon (`:`). On the next lines write the compact utterances prefixed with a space character.

Compact utterances support the following elements:

* comment: `#`

  Empty lines and lines beginning with `# ` will be ignored, which allows to add comments to the compact utterances source

* alternative: `(a|b)`

  Expands to two or more utterances, one for each option. The brackets can contain any numer of alternatives separated by `|`. Be aware that multiple alternatives in a compact utterance will result in the product of the numbers of alternatives utterances.

* optional: `[a]`

  Makes the text `a` optional, i.e. it expands to two utterances of which one contains the text and the other doesn't. This is the same as (a|) (i.e. an alternative with an empty value)

* typed slot: `{type:name}`

  This will be replaces by a slot with just the name, i.e. `{name}`. The type will be used to create the intent JSON object.

## Example usage

This script needs to be run with python3. Just pass the filename as a parameter

```
python3 aug.py compact_utterances.txt
```
The result will be printed to the console, ready for copy & paste.

## Example input

The following compact utterances will expand to the result underneath

```
# an intent to ask how something can be made.
# Note: The first utterance will expand to 40 different combinations
howToIntent:
 how (would|could|do|can) I (make|create|build|produce|generate) [a ]{THINGS:thing}
 how to {THINGS:thing}

# The default intents that always need to be present.
# Note: HelpIntent, StopIntent and CancelIntent will always be added by default. However,
# adding them here allows you to specifc custom utterances for these
AMAZON.HelpIntent:
AMAZON.StopIntent:
 leave me alone
 go away
 get lost
AMAZON.CancelIntent:
```
The output contains both, the utterances and the intent JSON, separated by a dashed line

```
howToIntent how would I make a {thing}
howToIntent how would I create a {thing}
howToIntent how would I build a {thing}
howToIntent how would I produce a {thing}
howToIntent how would I generate a {thing}
howToIntent how could I make a {thing}
howToIntent how could I create a {thing}
howToIntent how could I build a {thing}
howToIntent how could I produce a {thing}
howToIntent how could I generate a {thing}
howToIntent how do I make a {thing}
howToIntent how do I create a {thing}
howToIntent how do I build a {thing}
howToIntent how do I produce a {thing}
howToIntent how do I generate a {thing}
howToIntent how can I make a {thing}
howToIntent how can I create a {thing}
howToIntent how can I build a {thing}
howToIntent how can I produce a {thing}
howToIntent how can I generate a {thing}
howToIntent how would I make {thing}
howToIntent how would I create {thing}
howToIntent how would I build {thing}
howToIntent how would I produce {thing}
howToIntent how would I generate {thing}
howToIntent how could I make {thing}
howToIntent how could I create {thing}
howToIntent how could I build {thing}
howToIntent how could I produce {thing}
howToIntent how could I generate {thing}
howToIntent how do I make {thing}
howToIntent how do I create {thing}
howToIntent how do I build {thing}
howToIntent how do I produce {thing}
howToIntent how do I generate {thing}
howToIntent how can I make {thing}
howToIntent how can I create {thing}
howToIntent how can I build {thing}
howToIntent how can I produce {thing}
howToIntent how can I generate {thing}
howToIntent how to {thing}
AMAZON.StopIntent leave me alone
AMAZON.StopIntent go away
AMAZON.StopIntent get lost
--------------- snip ----------------
{
  "intents": [
    {
      "intent": "AMAZON.StopIntent",
      "slots": []
    },
    {
      "intent": "AMAZON.CancelIntent",
      "slots": []
    },
    {
      "intent": "AMAZON.HelpIntent",
      "slots": []
    },
    {
      "intent": "howToIntent",
      "slots": [
        {
          "name": "thing",
          "type": "THINGS"
        }
      ]
    }
  ]
}
```
