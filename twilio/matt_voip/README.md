# Matt's VOIP

Provides VOIP services for people calling me, and for me calling people.

Symmetric service that can be flipped between Spanish & English with a text.

Requires Twilio UK & ES landline numbers capable of text and voice.

# Spec

## Voice from Matt

Services to include:

* Menu to select a number to call from the phonebook
* Option to type a number that is then called

## Text from Matt

Services to include:

* Switch between ES & UK
* Dictionary lookup, translation services, callbacks etc.

## Voice from unknown number

Play a brief message 'Matt is currently in X and this number will redirect you
free of charge to his X number' and then redirect to Matt's mobile.

## Text

Redirect to Matt's mobile.

# Todo

* on startup send text so I know if it's rebooted
* save state (en vs es)
* protect things like /handle-dial - how?
* nice way to do the 2 modes
