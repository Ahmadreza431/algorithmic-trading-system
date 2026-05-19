import requests
import json

url = "Url Webhook Adreess"

def handler(pd: "pipedream"):
    # دریافت مقدار target2 و ذخیره آن در symb
    signal_text = pd.steps["trigger"]["event"]["body"]
 
    payload = json.dumps({
      "type": "py",
      "message": {
        "text": signal_text
      }
    })
    headers = {
      'Content-Type': 'application/json',
      'Cookie': 'XSRF-TOKEN='
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    print(response.text)
  
 
    return 
