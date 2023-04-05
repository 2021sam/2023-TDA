import requests
import dateutil.parser
import datetime
import json

from Class.OAuth import OAuth
auth = OAuth()

import urllib.parse
from credentials import client_id, refresh_token

class Stream:
	def __init__(self):
		# Get User Principals
		endpoint = 'https://api.tdameritrade.com/v1/userprincipals'
		headers = {'Authorization':'Bearer {}'.format(auth.tokens['access_token'])}
		params = {'fields': 'streamerSubscriptionKeys,streamerConnectionInfo'}
		content = requests.get( url = endpoint, params = params, headers = headers )

		userPrincipalsResponse = content.json()
		tokenTimeStamp = userPrincipalsResponse['streamerInfo']['tokenTimestamp']
		date = dateutil.parser.parse(tokenTimeStamp, ignoretz = True)
		tokenTimeStampAsMs = self.unix_time_millis(date)

		credentials = {
			"userid": userPrincipalsResponse['accounts'][0]['accountId'],
			"token": userPrincipalsResponse['streamerInfo']['token'],
			"company": userPrincipalsResponse['accounts'][0]['company'],
			"segment": userPrincipalsResponse['accounts'][0]['segment'],
			"cddomain": userPrincipalsResponse['accounts'][0]['accountCdDomainId'],
			"usergroup": userPrincipalsResponse['streamerInfo']['userGroup'],
			"accesslevel": userPrincipalsResponse['streamerInfo']['accessLevel'],
			"authorized": "Y",
			"timestamp": int(tokenTimeStampAsMs),
			"appid": userPrincipalsResponse['streamerInfo']['appId'],
			"acl": userPrincipalsResponse['streamerInfo']['acl']
		}
		login_request = {
			"requests": [
					{
						"service": "ADMIN",
						"command": "LOGIN",
						"requestid": '0',
						"account": userPrincipalsResponse['accounts'][0]['accountId'],
						"source": userPrincipalsResponse['streamerInfo']['appId'],
						"parameters": {
							"credential": urllib.parse.urlencode( credentials ),
							"token": userPrincipalsResponse['streamerInfo']['token'],
							"version": "1.0"
						}
					}
			]
		}
		qos_request = {
			"requests": [
					{
						"service": "ADMIN",
						"requestid": '1',
						"command": "QOS",
						"account": userPrincipalsResponse['accounts'][0]['accountId'],
						"source": userPrincipalsResponse['streamerInfo']['appId'],
						"parameters": {
							"qoslevel": '0'
						}
					}
			]
		}
		quote_request = {
			"requests": [
					{
						"service": "QUOTE",
						"command": "SUBS",
						"requestid": '2',
						"account": userPrincipalsResponse['accounts'][0]['accountId'],
						"source": userPrincipalsResponse['streamerInfo']['appId'],
						"parameters": {
							"keys": 'SPY, QQQ, AAPL, BA',
							"fields": '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16'
						}
					}
			]
		}

		self.userPrincipalsResponse = userPrincipalsResponse
		# encode requests
		self.login = json.dumps(login_request)
		self.qos = json.dumps(qos_request)
		self.quote = json.dumps(quote_request)


	def unix_time_millis(self, dt):
		epoch = datetime.datetime.utcfromtimestamp(0)
		return (dt - epoch).total_seconds() * 1000.0
