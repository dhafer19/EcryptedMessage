# EcryptedMessage
This folder contains two clients and one server. To set this up you must first start each of them in the correct order.
First the server, then Alice, then Bob. The order will be determined by the order their pre shared keys are entered.
The pre-shared key can be anything but must match on both sides to properly encrypt and decrypt.


Alice can then send messages to Bob. This is encrypted using a vigenere cipher then sent to the server. The server then
wll send it to Bob. Bob will receive it and then decrypt it using the shared key.

Currently the communication only works once and one way.  Alice to Bob
