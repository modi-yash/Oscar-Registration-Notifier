import datetime
import os

def log(*text):
    text = ' '.join(str(t) for t in text)
    if not os.path.isdir("./logs"):
        os.mkdir("logs")
    with open(f"./logs/{datetime.datetime.now().strftime("%d-%m-%y")}.log", 'a') as f:
        message = f"{datetime.datetime.now().strftime("%d-%m-%y %I:%M:%S")} - {text}\n"
        f.write(message)
        print(message)
        return message
    return "Error with file handler."