import datetime
import os

def log(*text):
    text = ' '.join(text)
    if not os.path.isdir("./logs"):
        os.mkdir("logs")
    with open(f"./logs/{datetime.datetime.now().strftime("%d-%m-%y")}_log.txt", 'a') as f:
        message = f"{datetime.datetime.now()} - {text}\n"
        f.write(message)
        return message
    return "Error with file handler."