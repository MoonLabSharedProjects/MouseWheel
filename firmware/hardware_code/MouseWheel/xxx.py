def serial():
    text = ""
    send = "RSD\r"
    port.write(send)
    s = port.read(1)
    if (s != ""):
        text = text + str(s)
        if ord(s) == 13:
            return text