#---------------------------
#   Import Libraries
#---------------------------
import clr
import json
import sys
import os
import ctypes
import codecs
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
clr.AddReferenceToFileAndPath('InteractiveLimitless.dll')
from InteractiveLS import Interaction

#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "Interactive Limitless"
Website = "https://github.com/LuisSanchez-Dev"
Description = "Web sockets / TCP server for Streamlabs Chatbot"
Creator = "LuisSanchezDev"
Version = "0.1.0"

#---------------------------
#   Define Global Variables
#---------------------------
global InteractionInstance
configFile = "config.json"
settings = {}

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
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

  InteractionInstance.MessageReceived += OnMessageReceived
  InteractionInstance.StartServer('ws',settings["WebSocketPort"])
  return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):
  global InteractionInstance
  if data.IsChatMessage():
    InteractionInstance.SendMessage(data.Message)
  return

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
  return

#---------------------------
#   [Required] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
  Unload()
  Init()
  return

def OpenReadMe():
  location = os.path.join(os.path.dirname(__file__), "README.txt")
  os.startfile(location)
  return

#---------------------------
#   [Required] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():
  global InteractionInstance
  InteractionInstance.Close()
  InteractionInstance= None
  return

def OnMessageReceived(sender,e):
  Parent.SendStreamMessage(e.Message)