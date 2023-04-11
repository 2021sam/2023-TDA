# import dateutil.parser
import requests, json, urllib.parse
from datetime import datetime
from TDA.OAuth import OAuth
auth = OAuth()


class Stream:
	def __init__(self):
		self.principals = auth.get_principals()
		print(self.principals)
		userPrincipalsResponse = self.principals
		timestamp = int(datetime.timestamp(datetime.strptime(userPrincipalsResponse['streamerInfo'].get('tokenTimestamp'), "%Y-%m-%dT%H:%M:%S%z"))) * 1000

		credentials = {
			"userid": userPrincipalsResponse['accounts'][0]['accountId'],
			"token": userPrincipalsResponse['streamerInfo']['token'],
			"company": userPrincipalsResponse['accounts'][0]['company'],
			"segment": userPrincipalsResponse['accounts'][0]['segment'],
			"cddomain": userPrincipalsResponse['accounts'][0]['accountCdDomainId'],
			"usergroup": userPrincipalsResponse['streamerInfo']['userGroup'],
			"accesslevel": userPrincipalsResponse['streamerInfo']['accessLevel'],
			"authorized": "Y",
			"timestamp": timestamp,
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
							"credential": urllib.parse.urlencode(credentials),
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

		quote_sub_request = {
			"requests": [
					{
						"service": "QUOTE",
						"command": "SUBS",
						"requestid": "2",
						"account": userPrincipalsResponse['accounts'][0]['accountId'],
						"source": userPrincipalsResponse['streamerInfo']['appId'],
						"parameters": {
							"keys": "SPY, QQQ, AAPL, BA",
							"fields": "0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16"
						}
					}
			]
		}

		quote_unsub_request = {
			"requests": [
					{
						"service": "QUOTE",
						"command": "UNSUBS",
						"requestid": '2',
						"account": userPrincipalsResponse['accounts'][0]['accountId'],
						"source": userPrincipalsResponse['streamerInfo']['appId'],
						"parameters": {
							"keys": 'SPY, QQQ, AAPL, BA',
							"fields": '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16',
							"frequency": "m1"
						}
					}
			]
		}

		self.login = json.dumps(login_request)
		self.qos = json.dumps(qos_request)
		self.quote_sub = json.dumps(quote_sub_request)


	def unix_time_millis(self, dt):
		epoch = datetime.utcfromtimestamp(0)
		return (dt - epoch).total_seconds() * 1000.0
