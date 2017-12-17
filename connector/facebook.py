import os
import requests
import json


def verify(request):
    if request.args.get("hub.mode") == "subscribe" and request.args.get(
            "hub.challenge"):
        if not request.args.get("hub.verify_token") == os.getenv(
                "FB_VERIFY_TOKEN"):
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return None


def handle(request):
    data = request.get_json()

    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):  # someone sent us a message
                    sender_id = messaging_event["sender"][
                        "id"]  # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"][
                        "id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"][
                        "text"]  # the message's text
                    return {"sender": sender_id, "message": message_text}

                if messaging_event.get("delivery"):
                    pass

                if messaging_event.get("optin"):
                    pass

                if messaging_event.get("postback"):
                    pass
    return None


def send_message(recipient_id, message):
    params = {"access_token": os.getenv("FB_ACCESS_TOKEN")}
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"recipient": {"id": recipient_id}, "message": message})
    r = requests.post(
        "https://graph.facebook.com/v2.6/me/messages",
        params=params,
        headers=headers,
        data=data)
    if r.status_code != 200:
        raise Exception(r.text)
