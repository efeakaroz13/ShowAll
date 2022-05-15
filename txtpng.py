import os

pngFileRead = open("./static/fav.png","r").read()
txtWrite = open("./static/fav.txt","w").write(pngFileRead)
