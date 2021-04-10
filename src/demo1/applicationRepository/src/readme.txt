Service1: To check whether application is present or not:

URL:"http://127.0.0.1:5000/appIdVerification/"
    Here : applicationRepository IP_address : 127.0.0.1
            applicationRepository port      : 5000

Input : Data should be in json Format 
    Example : 
         applicationNameToCheck = "123.txt"
          s = json.dumps(conv)
          res = requests.post("http://127.0.0.1:5000/appIdVerification/", json=s).json()
          return res
output : [res] is boolean value
            True : File is present
            False: File is not present


Service2 :  To generate AppId

URL : "http://127.0.0.1:5000/generateAppId/"
    Here : applicationRepository IP_address : 127.0.0.1
            applicationRepository port      : 5000

    output :int data in json format 
            return json.dumps(result)


service 3 : Insert zip file from Dashboard to Application repository
            output: unique 3 digit appID


service 4 : nabhiraj API  : To send zip file 
            URL : "http://127.0.0.1:5000/retrieve/"
    Here : applicationRepository IP_address : 127.0.0.1
            applicationRepository port      : 5000

            input : appid Name 
            output : zipFile







To get Zip File and upload in directory

// send zip File from Deployer to applicationRepository
URL:"http://127.0.0.1:5000/uploadZipInRepository/"
    Here : applicationRepository IP_address : 127.0.0.1
            applicationRepository port      : 5000

Input : Zip File 

Output : Zip File got Downloaded



