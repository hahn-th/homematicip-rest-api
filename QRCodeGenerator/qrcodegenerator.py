#!/usr/bin/env python3
import homematicip
from homematicip.home import Home
from homematicip.group import MetaGroup
from homematicip.device import Device
import qrcode
import os
import codecs

config = homematicip.find_and_load_config_file()


def main():
    if config is None:
        print("COULD NOT DETECT CONFIG FILE")
        return


    home = Home()
    home.set_auth_token(config.auth_token)
    home.init(config.access_point)
    print("Downloading configuration")
    home.get_current_state()
    if not os.path.exists("./img/"):
        os.makedirs("./img/")

    print("Generating QRCodes")
    img = qrcode.make(config.access_point)
    img.save("./img/{}.png".format(config.access_point))
    for d in home.devices:
        img = qrcode.make(d.id)
        img.save("./img/{}.png".format(d.id))

    print("Creating website")
    templatePath = os.path.join(os.path.dirname(__file__), 'qrcodes_template.html')
    template = None
    tableText = ""
    with open(templatePath, "r") as t:
        template = t.read()
    
    tableText = tableText + "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td><img src=\"img/{}.png\"></td></tr>\n".format("#HAP#", "Access-Point", config.access_point, "HMIP-HAP", config.access_point)
    for g in home.groups:
        if not isinstance(g, MetaGroup):
            continue;
        for d in g.devices:
            tableText = tableText + "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td><img src=\"img/{}.png\"></td></tr>\n".format(g.label, d.label, d.id, d.modelType, d.id)
    result = template.replace("##QRROWS##", tableText)
    with codecs.open("qrcodes.html", "w", "UTF-8") as f:
        f.write(result)

    print("Finished")
if __name__ == "__main__":
    main()
