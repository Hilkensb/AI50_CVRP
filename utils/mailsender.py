# Standard Library
from __future__ import annotations
import os
import base64

# Other Library
from mailjet_rest import Client

# Other module
from utils.mailtemplate import MAIL_TEMPLATE

def sendMailFinished(
    mail_receiver: str, mail_name: str, link: str
) -> None:
    """
    """
    
    # Non secure way to get the keys
    # Just for now and the poc and tp use it the easiest way
    # Can just be used to send email not to connect to mailjet
    api_key: str = '0a4a02c2cae80add052cdbb0a84bc6a9'
    api_secret: str = 'f938a38495766b6cf0da5f48e59921bd'
    # A better way and more secure would be to use system variable and getting them
    # like the following would do
    #   api_key: str = os.environ.get('MAILJET_USER')
    #   api_secret: str = os.environ.get('MAILJET_PASS')
    # To be changed for production version if one
    
    # Search for the receiver name
    name: str = " ".join([
        n.capitalize() 
        for n in mail_receiver.split("@")[0].split(".")
    ])
    
    with open("./gui/static/image/finish.png", "rb") as img_file:
        # Convert the image into 64 base
        base64_img: str = base64.b64encode(img_file.read())
    
    cid = "id1"
    # Build the html
    html: str = MAIL_TEMPLATE.format(receiver_name=name, report_link=link, cid=cid)
    
    # Get the mailjet client
    mailjet: Client = Client(auth=(api_key, api_secret), version='v3.1')
    
    # Set the data of the email
    data = {
      'Messages': [
        {
          "From": {
            "Email": "cvrp.ai50@gmail.com",
            "Name": "The ROAD's team"
          },
          "To": [
            {
              "Email": mail_receiver,
              "Name": name
            }
          ],
          "Subject": "Your report is ready",
          "TextPart": mail_name,
          "HTMLPart": html,
          "CustomID": mail_name,
          "InlinedAttachments": [{
                "ContentType": "image/png",
                "Filename": "finish.png",
                "ContentID": cid,
                "Base64Content": str(base64_img)[1:]
            }]
        }]
    }
    
    # Send the email
    result = mailjet.send.create(data=data)
    # Return the request code
    return result.status_code

