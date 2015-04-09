import os
import requests
#Mailgun api

mailgun_url = os.getenv('GENI_MAILGUN_URL', '')
mailgun_api_key = os.getenv('GENI_MAILGUN_API_KEY', '')
from_addr = os.getenv('GENI_FROM_ADDR', '')
def sendEmail(toMail, data):
    subject = "GFDC profile counts - " + data['guid']
    htmlContent = prepateHtml(data)
    ret = requests.post(
                        mailgun_url,
                        auth=("api", mailgun_api_key),
                        data={"from": from_addr,
                              "to": toMail,
                              "subject": subject,
                              "html": htmlContent})

def prepateHtml(data):
    htmlContent = '<html><body>'
    htmlContent = htmlContent + '<h3>Hi,</h3><br/>'
    if(data['remainingSteps'] == '0'):
        htmlContent = htmlContent + '<h5>Your GFDC background job is finished.<br/></h5>'
    else:
        htmlContent = htmlContent + '<h5>Your GFDC background job is running.<br/></h5>'
    htmlContent = htmlContent + '<h5>Profile Name:' + data['profileName'] + '</h5>'
    htmlContent = htmlContent + '<h5>Profile ID:<a href='+ str(data['geniLink'])+ '>' + str(data['guid'])+ '</a></h5>'
    htmlContent = htmlContent + '<table border=\'1\'><tr><th>Step</th><th>Profiles</th><th>Total</th></tr>'
    for s in data['steps']:
        htmlContent = htmlContent + '<tr><td>' + str(s['step']) + '</td><td>' + str(s['profiles']) + '</td><td>' + str(s['total']) + '</td></tr>'
    htmlContent = htmlContent + '</table><br/><br/>'
    htmlContent = htmlContent + '<h5>Steps remaining:' + data['remainingSteps'] + '</h5><br/>'
    htmlContent = htmlContent + 'Please visit GFDC  <b><a href=\'http://gfdc.herokuapp.com\'>here</a></b>.<br/><br/>'
    htmlContent = htmlContent + 'Thank you,<br/>GFDC</body></html>'
    return htmlContent

