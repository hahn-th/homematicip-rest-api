#!/usr/bin/env python3
import homematicip
from homematicip.home import Home
from homematicip.group import MetaGroup
from homematicip.device import Device
import qrcode
import os

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
    for d in home.devices:
        img = qrcode.make(d.id)
        img.save("./img/{}.png".format(d.id))

    
    print("Creating website")
    with open("qrcodes.html", "w") as f:
        f.write("""<html><style>
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
th, td {
    padding: 15px;
    text-align: left;
}
</style><body>""")
        f.write("<table style=\"width:100%\">")
        f.write("<tr><th>Room</th><th>Device</th><th>DeviceID</th><th>Model</th><th>QRCode</tr>")
        for g in home.groups:
            if not isinstance(g, MetaGroup):
                continue;
            for d in g.devices:
                f.write("<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td><img src=\"img/{}.png\"></td></tr>".format(g.label, d.label, d.id, d.modelType, d.id))

        f.write("</table>")
        f.write("</body></html>")
    print("Finished")
if __name__ == "__main__":
    main()
