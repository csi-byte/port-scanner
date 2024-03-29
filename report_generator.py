

def ecritureFichier(htmlText, fileNameOutput):
    try:        
        FileReport = open(fileNameOutput,"w")
        FileReport.write(" ".join(htmlText))
        FileReport.close()
    except IOError:
        print("error while writing scan repport")


#creation d un rapport au format html

def generateReport(result, fileNameOutput):
    head = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\"><html xmlns=\"http://www.w3.org/1999/xhtml\"xml:lang=\"en\" lang=\"en\"><head><meta http-equiv=\"content-type\" content=\"text/html; charset=utf-8\" />  <title>Scan Report</title> </head><body> <center><h2>Scan Report</h2> <p>Total hosts : totalhosts   Up hosts : uphosts</p></center><br>"
    bottom = "	<br>	<br>	<hr>	<br>	<br></body></html>"
    templateMachine = "<p>	<h3>Nmap scan report for NameMachine (IpMachine)</h3>	<p>Host is MachineState</p><p>Mac address : MacAdress</p>	<p>PORT      STATE SERVICE VERSION</p> 	<ul>	#ici	</ul></p>"
    templatePortText = "<li>PortNumber     PortState  PortService PortSVersion</li>"
    

    
    
    htmlText = list()
    
    uphosts=0
    totalhosts=0
    
    
    #on regarde dans le dictionnaire result les ips scannees et on complete les templates htmls
    try:
        for host in result:

             
            uphosts+=int(result[host]['res']['nmap']['scanstats']['uphosts']   )
            totalhosts+=int(result[host]['res']['nmap']['scanstats']['totalhosts'] )   
                  
            for sousHost in  result[host]["res"]["scan"]:
                
                
                temptemplateMachine = templateMachine.replace("NameMachine", result[host]["res"]["scan"][sousHost]["hostnames"][0]["name"]+" "+result[host]["res"]["scan"][sousHost]["hostnames"][0]["type"] )
                temptemplateMachine = temptemplateMachine.replace("IpMachine", sousHost)
                temptemplateMachine = temptemplateMachine.replace("MachineState",result[host]["res"]["scan"][sousHost]["status"]["state"] + " reason : " + result[host]["res"]["scan"][sousHost]["status"]["reason"])
                if "mac" in result[host]["res"]["scan"][sousHost]["addresses"] and result[host]["res"]["scan"][sousHost]["addresses"]["mac"] != '':
                    temptemplateMachine = temptemplateMachine.replace("MacAdress", result[host]["res"]["scan"][sousHost]["addresses"]["mac"])
                else:
                    temptemplateMachine = temptemplateMachine.replace("MacAdress", "Not found")
                try:
                    for port in result[host]["res"]["scan"][sousHost]["tcp"]:                    
                        temptemplatePortText = templatePortText.replace("PortNumber",str(port))
                        temptemplatePortText=temptemplatePortText.replace("PortState",result[host]["res"]["scan"][sousHost]["tcp"][port]["state"])
                        temptemplatePortText=temptemplatePortText.replace("PortService",result[host]["res"]["scan"][sousHost]["tcp"][port]["name"] + " " +result[host]["res"]["scan"][sousHost]["tcp"][port]["product"])
                        temptemplatePortText=temptemplatePortText.replace("PortSVersion",result[host]["res"]["scan"][sousHost]["tcp"][port]["version"]+" "+result[host]["res"]["scan"][sousHost]["tcp"][port]["extrainfo"])
                        temptemplateMachine = temptemplateMachine.replace("#ici	", temptemplatePortText + "#ici	")
                except Exception as ex:
                    if 'tcp' not in result[host]["res"]["scan"][sousHost]:
                        temptemplateMachine = temptemplateMachine.replace("#ici	", "No open Ports" ) 
                    # pas de ports ouverts pour un scan, c est normal 
                    pass
                temptemplateMachine = temptemplateMachine.replace("#ici	", "") 
                htmlText.append(temptemplateMachine)
              
    except Exception as ex:
        print("error while reading scan results")      
        print(ex)

    htmlText.insert(0,head.replace("totalhosts",str(totalhosts) ).replace("uphosts",str(uphosts) ) )
    htmlText.append(bottom)
    ecritureFichier(htmlText, fileNameOutput)
    



