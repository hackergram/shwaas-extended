# Shwaas NLP Bot - based on Rasa Framework

### Install Rasa Framework

'''
pip3 install rasa
pip3 install rasa-x --extra-index-url https://pypi.rasa.com/simple
'''

_ Note: This may need you to downgrade pip to v20.2 _

### Run the bot API

'''
cd shwaasnlp
rasa run
'''

### Test the API

API calls may be made to http://<server_ip>:5005/webhooks/rest/webhook by making a POST request with JSON body

'''
{
  "sender": "test_user",
  "message": "Hi !"
}
'''
