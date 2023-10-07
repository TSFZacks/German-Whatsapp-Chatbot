import requests
import sett
import json
import time
import webbrowser

def obtener_Mensaje_whatsapp(message):
    if 'type' not in message :
        text = 'mensaje no reconocido'
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'mensaje no procesado'
    
    return text

def enviar_Mensaje_whatsapp(data):
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + whatsapp_token}
        print("se envia ", data)
        response = requests.post(whatsapp_url, 
                                 headers=headers, 
                                 data=data)
        
        if response.status_code == 200:
            return 'mensaje enviado', 200
        else:
            return 'error al enviar mensaje', response.status_code
    except Exception as e:
        return e,403
    
def text_Message(number,text):
    data = json.dumps(
            {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "body": text
                }
            }
    )
    return data
  
"""def send_image_message(number, image_data, caption):

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + "EAAH5ZCoK0SR0BO4QJyYnUjZC3CclxEkVRiZCY9LOz7ZCtr5OwNwVAgZBjr9v2ejihXQzsc8uqnKjSbRu9y9MtdN0U6Ou01ZBFs3zb4pfntFlvCbTdnDXfuY3MNloSZBBO47AguHbA1xSO2sNsHfYPTdleSmWpbERxETY2YZCYfq6r4CxgHqsa8KZBTGzR2brL3VGZAazhw5H7cnqdVTagqyg3WxkuZAZB7PevJycj4gBFKkZD"
        }

        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": "",
                "caption": caption,
                "filename": "lodfgo.png"  # Nome do arquivo de imagem
            }
        }

        response = requests.post(whatsapp_url, headers=headers, json=data, files={"file": ("imagem.jpg", image_data)})
        
        if response.status_code == 200:
            return 'Imagem enviada com sucesso!', 200
        else:
            return 'Erro ao enviar a imagem', response.status_code

        except Exception as e:
            return str(e), 403
"""

def buttonReply_Message(number, options, body, footer, sedd,messageId):
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data

def listReply_Message(number, options, body, footer, sedd,messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Opções",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )
    return data

def document_Message(number, url, caption, filename):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": url,
                "caption": caption,
                "filename": filename
            }
        }
    )
    return data

def sticker_Message(number, sticker_id):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {
                "id": sticker_id
            }
        }
    )
    return data

def get_media_id(media_name , media_type):
    media_id = ""
    if media_type == "sticker":
        media_id = sett.stickers.get(media_name, None)
    elif media_type == "image":
        media_id = sett.images.get(media_name, None)
    #elif media_type == "video":
    #    media_id = sett.videos.get(media_name, None)
    #elif media_type == "audio":
    #    media_id = sett.audio.get(media_name, None)
    return media_id

def replyReaction_Message(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    )
    return data

def replyText_Message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": { "message_id": messageId },
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data

def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data

def administrar_chatbot(text, number, messageId, name):
    text = text.lower() #mensaje que envio el usuario
    list = []
    print("mensaje del usuario: ", text)

    markRead = markRead_Message(messageId)
    list.append(markRead)
    
    if "hello" in text:
      
        url_da_sua_imagem = 'https://cdn.glitch.global/4eb4ae5c-8da2-472f-b91c-28d6afe4f15c/WhatsApp%20Image%202023-09-19%20at%2012.30.10.jpg?v=1695151589718'

    # Chame a função para enviar a imagem
        data = json.dumps(
            {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": number,
                "type": "image",
                "image": {
                    "link": url_da_sua_imagem,
                    "caption": ""
                }
            }
        )
        enviar_Mensaje_whatsapp(data)
    
        body = "Welcome to fresh shop 👋! Please choose any option 👇"
        footer = "Fresh Shop Team"
        options = ["Product & Services", "Complain"]
        #options = ["Weitermachen","Datenschutz Lesen"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1",messageId)
        list.append(replyButtonData)
        text = text.strip().lower()
        
    elif "go to main page" in text:
          
        body = "Please choose any option 👇"
        footer = "Fresh Shop Team"
        options = ["Product & Services", "Complain"]
        #options = ["Weitermachen","Datenschutz Lesen"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed2",messageId)
        list.append(replyButtonData)
        text = text.strip().lower()
        
    elif "complain" in text:
        
        body = "For requests, send a message to this number +8801875314620"
        footer = "Fresh Shop Team"
        options = ["Finish"]
        #options = ["Weitermachen","Datenschutz Lesen"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed3",messageId)
        list.append(replyButtonData)
        text = text.strip().lower()
        
    elif "product & services" in text:
      
        body = "Please choose a Category from smart shop 👇"
        footer = "Fresh Shop Team"
        options = ["Grocery", "Fashion"]
        #options = ["Weitermachen","Datenschutz Lesen"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed4",messageId)
        list.append(replyButtonData)
        text = text.strip().lower()
        
    elif "grocery" in text:
      
        body = "Please choose a brand for product catalog 👇"
        footer = "Fresh Shop Team"
        options = ["Fresh Brand", "RFL Brand"]#, "Migración Cloud", "Inteligencia de Negocio"

        """listReplyData = listReply_Message(number, options, body, footer, "sed2",messageId)
        sticker = sticker_Message(number, get_media_id("perro_traje", "sticker"))

        list.append(listReplyData)
        list.append(sticker)"""
      
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed5",messageId)
        list.append(replyButtonData)
        text = text.strip().lower()
        
    elif "fashion" in text:
      
        body = "Please choose a brand for product catalog 👇"
        footer = "Fresh Shop Team"
        options = ["Fresh Brand", "RFL Brand"]#, "Migración Cloud", "Inteligencia de Negocio"

        """listReplyData = listReply_Message(number, options, body, footer, "sed3",messageId)
        sticker = sticker_Message(number, get_media_id("perro_traje", "sticker"))

        list.append(listReplyData)
        list.append(sticker)"""
      
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed6",messageId)
        list.append(replyButtonData)
        text = text.strip().lower()
        
    elif "fresh brand" in text:
      
        document = document_Message(number, sett.document_url, "Here is the PDF", "Inteligencia de Negocio.pdf")
        enviar_Mensaje_whatsapp(document)
        
        textMessage = text_Message(number,"Please send a product list from pdf file")
        enviar_Mensaje_whatsapp(textMessage)
      
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed7",messageId)
        list.append(replyButtonData)
        text = text.strip().lower()
        
    elif "rfl brand" in text:
        
        document = document_Message(number, sett.document_url, "Here is the PDF", "Inteligencia de Negocio.pdf")
        enviar_Mensaje_whatsapp(document)
      
        textMessage = text_Message(number,"Please send a product list from pdf file")
        enviar_Mensaje_whatsapp(textMessage)

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed8",messageId)
        list.append(replyButtonData)
        text = text.strip().lower()
        
    elif "pdf list" in text:
        
        body = "Please share your delivery address"
        footer = "Fresh Shop Team"
        options = ["Go To Main Page", "Support"]
        
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed8",messageId)
        list.append(replyButtonData)
        text = text.strip().lower()
        
    for item in list:
      
        enviar_Mensaje_whatsapp(item)
        if text == "finalisieren":
          break
        

        
#al parecer para mexico, whatsapp agrega 521 como prefijo en lugar de 52,
# este codigo soluciona ese inconveniente.
def replace_start(s):
    if s.startswith("521"):
        return "52" + s[3:]
    else:
        return s

# para argentina
def replace_start(s):
    if s.startswith("549"):
        return "54" + s[3:]
    else:
        return s