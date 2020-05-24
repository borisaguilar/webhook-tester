A simple module for testing webhooks.

This software consists on an HTTP server running
and a library to speak to trigger HTTP actions
and reading whatever is being received in the HTTP server as consequence.

A typical webhook scenario is as follows:

0. You have two services running, lets say heybook and chatbot

1. You subscribe your webhook endpoint into heybook with a URL like:
https://chatbot.com/talk_to_me

2. Then you do something with heybook,
whatever triggers heybook to call chatbot,
that trigger might look like:
POST https://chatbot.com/talk_to_me?this=that

3. So then chatbot does whatever it has to do and talks back to heybook like:
POST https://heybook.com/say?what=hey_dude_there_you_go

Following the example, this package fakes being heybook,
so you can test chatbot responding correctly
when a fake hook action is triggered.

This is an example of what you've to do:

0. You need to have the url of your webhook as: x.com/my_hook

1. Start the webhook_tester in yourserver.com as follows:
HTTPSERVERPORT=9999 SOCKETSERVERPORT=1337 python -m webhook_tester

2. Configure your software to call to yourserver.com:9999

3. Use the library in hooksocket.py as follows:
socketclienttest = SocketClient(host = "localhost", port=1337)
result = socketclienttest.invoke(request = dict(method = "get",
                                                url = "http://x.com/myhook",
                                                data = dict()))

4. The socketclienttest.invoke will send the instructions to yourserver.com,
so yourserver.com does the following:
4.1. Invoke get http://x.com/myhook with the data specified in data
4.2. Wait until it receives on yourserver.com:9999 anything
4.3. Once it gets something in yourserver.com:9999 it will return

5. Variable result holds the following:
A dictionary with a key hook and a key result.
The key result holds the result of the request (get in the example)
The key hook contains the received whatever things on yourserver.com:9999
