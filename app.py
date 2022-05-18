from flask import Flask,render_template,request,redirect,make_response,abort
import pyrebase
import shutil
from cryptography.fernet import Fernet
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from os.path import join, dirname, realpath
import json
import requests
import smtplib


key =b'NDh7sdSVUmb6_O8-nvd2mADYzMFrrdhXoa-G8cqVIb0='
fernet = Fernet(key)


def currency_to_logo(value):
    if value =="dollar":
        return "$"
    else:
        return "₺"


def decrypt(textVal):
    out = fernet.decrypt(textVal.encode()).decode()
    return out

def encrypt(textVal):
    out = fernet.encrypt(textVal.encode()).decode()
    return out
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "./static/models"


class adminStuff:
    @app.route("/OrderRecieved")
    def OrderRecieved():
        return """
            <script>alert("We took your order and we will call you in 2 business days for delivery destination. We will take the payment face to face.");window.history.back()</script>

        """
    @app.route("/create/product",methods=["POST"])
    def createProduct():
        modelName = request.cookies.get("fileName")
        if modelName == None:
            return 403

        else:
            username = request.cookies.get("username")
            if username == None:
                return 403

            else:
                username = decrypt(username)
                password = decrypt(request.cookies.get("password"))

                if username == "efeakaroz13" and password=="efeAkaroz123":
                    title = request.form.get("title")
                    description = request.form.get("description")
                    price = request.form.get("price")
                    currency = request.form.get("currency")
                    theInfo = """
                        {
                            "title":"""+'"'+title+'"'+""",
                            "currency":"""+'"'+currency+'"'+""",
                            "price":"""+price+""",
                            "description":"""+'"'+description+'"'+""",
                            "model":"""+'"'+modelName+'"'+"""
                        }
                    """
                    fileWrite = open(f"products/{title.replace(' ','').replace('.','').replace('/','').replace('?','').replace('|','')}.txt","w")
                    fileWrite.write(encrypt(theInfo))
                else:
                    return 403
        return redirect("/admin?createdProduct=True")

    @app.route("/admin/logout")
    def adminLogout(): 
        response = make_response(redirect("/admin"))
        response.set_cookie("username",max_age=0)

        return response

    @app.route("/set/model/<modelName>")
    def setModelToCookie(modelName):
        username = request.cookies.get("username")
        if username!=None:
            username = decrypt(username)
            password= decrypt(request.cookies.get("password"))

            if username == "efeakaroz13" and password=="efeAkaroz123":
                response = make_response(redirect("/admin"))

                response.set_cookie("fileName",modelName)
                return response

            else:
                return abort(403)

        else:
            return abort(403)

    @app.route("/list/models")
    def listModels():
        import os

        models = os.listdir("./static/models")
        models.remove(".DS_Store")
        return {"models":models}


    @app.route("/deleteModel/<modelName>")
    def modelDelete(modelName):
        username = request.cookies.get("username")
        if username != None:
            username = decrypt(username)
            password = decrypt(request.cookies.get("password"))
            if username == "efeakaroz13" and password=="efeAkaroz123":
                response = make_response(redirect("/admin"))
                response.set_cookie("fileName",max_age=0)
                os.system(f"rm -r static/models/{modelName}")
            else:
                response= make_response({"error":"Forbidden"})
        else:
            response = make_response({"error":"Forbidden"})
        return response
    @app.route("/closePreview")
    def closePreview():
        username = request.cookies.get("username")
        if username != None:
            username = decrypt(username)
            password = decrypt(request.cookies.get("password"))
            if username == "efeakaroz13" and password=="efeAkaroz123":
                response = make_response(redirect("/admin"))
                response.set_cookie("fileName",max_age=0)
                
            else:
                response= make_response({"error":"Forbidden"})
        else:
            response = make_response({"error":"Forbidden"})
        return response
    @app.route("/modelUpload",methods=["POST"])
    def modelUpload():
        if request.method == "POST":
            filea = request.files["modelFileZip"]
            title = filea.filename.replace(".zip","")
            if filea:
                
                filea.save(os.path.join('static/models', title+".zip"))
                shutil.unpack_archive('./static/models/'+filea.filename, f'./static/models/{title}')
                import time
                time.sleep(0.08)
                os.system(f'rm -d static/models/{filea.filename}')
            else:
                pass

            response = make_response(redirect("/admin"))
            response.set_cookie("fileName",filea.filename)
            return response    

    @app.route("/admin",methods=["POST","GET"])
    def admin():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            response = make_response(redirect("/admin"))
            response.set_cookie("password",encrypt(password))
            response.set_cookie("username",encrypt(username))
            return response
        
        if request.method == "GET":
            username = request.cookies.get("username")
            if username != None:
                try:
                    username = decrypt(username)
                    password = decrypt(request.cookies.get("password"))
                    if username == "efeakaroz13" and password == "efeAkaroz123":
                        modelFile = request.cookies.get("fileName")
                        if modelFile ==None:
                            modelFile="False"
                        return render_template("admin.html",modelFile=modelFile.replace(".zip",""))
                    else:
                        return "Get the fuck out of my admin panel you son of a bitch"
                except Exception as e:
                    print(e)
                    response = make_response(redirect("/admin"))
                    response.set_cookie("username",max_age=0)
                    return response
                    
            else:
                return """
                <html>
                <body>
                    <center>
                    <br><br>
                    <img src="/static/fav.png" width=300 style="border-radius:20px">
                    <br><br>
                    <a href="/">Go to homepage</a>
                    </center>
                    <div class="container">
                    <form action="" method="POST">
                    
                        <input type="username" name="username" placeholder="Username For admin"><br>
                        
                        <input type="password"name="password" placeholder="Password"><br>
                        <button type=submit>Login as admin</button>
                    </form>
                    </div>
                    <style>
                        .container{
                            font-size:30px;
                            text-align:center;
                            padding-top:10%;
                        }
                    </style>
                    
                </body>
                </html>

                """


    @app.route("/product/json/<filename>")
    def productJson(filename):
        fileReader = open("products/{}".format(filename+".txt"),"r").read()
        json_obj = json.loads(decrypt(fileReader))
        return json_obj
    @app.route("/model/<modelName>")
    def model(modelName):
        return render_template("index.html",modelName=modelName)

    @app.route("/admin/viewers")
    def viewers():
        files = os.listdir("./views")

        return render_template("viewers.html",files=files)

    @app.route("/viewers/<fileName>")
    def viewerLoad(fileName):
        username = request.cookies.get("username")
        if username == None:
            return abort(403)
        else:
            username = decrypt(username)
            password = decrypt(request.cookies.get("password"))
            if username == "efeakaroz13" and password=="efeAkaroz123":

                out = []
                reader = open("views/{}".format(fileName),"r").readlines()
                for r in reader:
                    out.insert(0,decrypt(r.replace("\n","")))
            else:
                return abort(403)


        return {"out":out}

    @app.route("/admin/viewers/setCookie/<fileName>")
    def fileSetCookie(fileName):
        response = make_response(redirect("/admin/viewers"))
        response.set_cookie("viewerset",fileName)
        return response

class Home:
    @app.route("/")
    def site_index():
        apiCall = requests.get("http://localhost:5000/api/v1/items")
        jsonout = json.loads(apiCall.content)
        return render_template("mainpage.html",items=jsonout,currency_to_logo=currency_to_logo)





    @app.route("/order/<theFile>",methods=["POST","GET"])
    def orderTheThing(theFile):
        orderRecieved = request.args.get("orderRecived")

        if orderRecieved == "True":
            messagge = "Your order has been recieved we will contact you soon."
        else:
            messagge=None
        if request.method == "POST":
            print("post")
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            gmail_sender = 'ceteleplatform@gmail.com'
            gmail_passwd = 'efeAkaroz123'
            fullname = request.form.get("fullName")
            city = request.form.get("city")
            email = request.form.get("email")
            phoneNumber = request.form.get("phonenum")
            address=request.form.get("address")
            coordinates=request.form.get("coords")
            ourOwnData = f"fullName1313={fullname}andthenemail={email}andthencity={city}andthenphoneNumber={phoneNumber}andthenaddress={address}andthencoordinates={coordinates}"

            ordersWrite = open("orders/{}.txt".format(theFile),"a")
            ordersWrite.write(encrypt(ourOwnData)+"\n")
            server.login(gmail_sender, gmail_passwd)
            message = 'Subject: {}\n\n{}'.format(f"{fullname} ,New Order",str(ourOwnData.replace("andthen","\n")+f"\n{str(theFile)}"))
            server.sendmail(gmail_sender, "efeakaroz13@proton.me", message.encode('utf-8'))
            server.sendmail(gmail_sender, email, 'Subject: {}\n\n{}'.format(f"{fullname} ,Order Recieved",str("We will call you in 2 business days for more info")).encode('utf-8'))
            return redirect("/order/{}?orderRecived=True".format(theFile))


        theF = json.loads(decrypt(open("products/{}".format(theFile),"r").read()))
        theFviewers = open("views/{}".format(theFile),"a")
        try:
            theLine =  f"{request.environ['HTTP_X_FORWARDED_FOR']} - {request.headers.get('User-Agent')}"
        except:
            
            theLine =  f"{request.environ['REMOTE_ADDR']} - {request.headers.get('User-Agent')}"
        theFviewers.write(str(encrypt(theLine))+"\n")

        theFviewers.close()




        return render_template("products.html",theF=theF,currency_to_logo=currency_to_logo,messagge=messagge)

class apiV1:
    @app.route("/api/v1/items")
    def itemsapiv1():
        out = {
            "Items":[]
        }
        filesinproducts = os.listdir("products")
        for f in filesinproducts:
            myfile = open("products/"+f,"r").read()
            myfileJsonObject = json.loads(decrypt(myfile))
            myfileJsonObject["model"] = myfileJsonObject["model"].replace(".zip","")
            myfileJsonObject["fileTXT"] = f
            
            
            out["Items"].insert(0,myfileJsonObject)


        return out


app.run(debug=True)

