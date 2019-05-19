# Interactive Limitless
A Web Socket / TCP Socket server for use inside Streamlabs Chatbot's scripting API.

## Index
* [Getting Started](#getting-started)
* [Prerequisites](#prerequisites)
* [Installing](#installing)
* [API Reference](#api-reference)


## Getting Started


Here I will show you how to set it up so you can start developing your own interactions for Streamlabs Chatbot.

## Prerequisites
• Streamlabs Chatbot

## Installing

* Download the latest version of the script
* Extract the folder in your Scripts folder

## Using in Python script
* In the top of your Python script, where all the imports are, include the following
```python
import clr
import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
clr.AddReferenceToFileAndPath('InteractiveLimitless.dll')
from InteractiveLS import Interaction
```
* Then on your variables initialization part o the script, add the following line:
```python
global InteractionInstance #Can be any name, this will hold our interaction instance
```
* Now lets define our own function which will be run when we get a message from the client:
```python
def OnMessageReceived(sender,e):
  Parent.SendStreamMessage(e.Message)
```

* Now, on the `init()` section of the script, add the following:
```python
def Init():
  global settings, InteractionInstance

  path = os.path.dirname(__file__)

  try:
    with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
      settings = json.load(file, encoding='utf-8-sig')
  except:
    settings = {
      "WebSocketPort": 15011,
      "TCPSocketPort": 15010
    }  
  InteractionInstance = Interaction.GetInstance()

  InteractionInstance.MessageReceived   += OnMessageReceived
  
  #"ws" for Web sockets and "tcp" for TCP server
  InteractionInstance.StartServer('ws',settings["WebSocketPort"])
  return
```
Make sure to register your function adding it to the `InteractionInstance.MessageReceived` event handler.

* To send data to the clients, we use the `SendMessage()` method as follows:
```python
def Execute(data):
  if data.IsChatMessage():
    InteractionInstance.SendMessage(data.UserName)
```
*You can only send strings to the client. You could convert a python dictionary to json before sending it to the client and parsing it when the client responds.

* To finish, make sure to unload everything just as follows:
```python
def Unload():
  global InteractionInstance
  InteractionInstance.Close()
  InteractionInstance= None
  return

def ReloadSettings(jsonData):
  Unload()
  Init()
  return
```
* Now using your favorite Web Sockets / TCP client connect to the localhost IP `127.0.0.1` and the port specified in the script/config file

## API Reference

### Interaction.GetInstance()
Get an instance of the class
```python
instance = Interaction Interaction.GetInstance()
```
### Interaction.MessageReceived
Add the function you want to run to this event handler
```python
def myFunction(sender,e):
  Parent.SendStreamMessage(e.Message)

Interaction.MessageReceived += myFunction
```
* ``sender`` - The object that called the event
* ``e`` - The event arguments, where the ``Message`` property has the message passed to the server

### Interaction.StartServer(``string serverType, int port``)
Start the desired server with the desired port
#### serverType
* ``"ws"`` - To start a Web Socket server
* ``"tcp"`` - To start a TCP socket server
#### port
* ``int`` - Port number to start the server on

```python
Interaction.ServerStart("ws", 15011)
```
#### Interaction.SendMessage(string message)
Send a message to all the clients connected to the server
```python
interaction.SendMessage("Hi clients, its server")
```
### Interaction.Close()
Closes all servers and cleans up. Must be used in the ``Unload()`` function of your script
```python
Interaction.Close()
```
### Interaction.Beep()
Plays a windows sound. Mostly used to debug
```python
Interaction.Beep()
```