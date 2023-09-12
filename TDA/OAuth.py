# TD Ameritrade OAuth 2.0 authorization developer script
# This script:
#	Submits TD Ameritrade login information
#	Updates an expired refresh token every 90 days
# 	Updates an expired access token every 30 minutes
# OAuth.ipynb
# Author Sam Portillo
# References:
#   https://oauth.net/2/
#   https://developer.tdameritrade.com/


import ast
import os, requests, time, urllib, json
from splinter import Browser
from selenium import webdriver
from private.credentials import client_id, username, password, redirect_uri
from pathlib import Path
# from selenium.webdriver.common.keys import Keys
# from pynput.keyboard import Key, Controller
# keyboard = Controller()

class OAuth:
	def __init__(self):
		self.access_token = ''
		self.current_working_directory = Path.cwd()
		self.refresh_token_file = self.current_working_directory / 'private/refresh_token.json'
		self.access_token_file = self.current_working_directory / 'private/access_token.json'
		print( self.refresh_token_file )

		if not self.valid_refresh_token():
			refresh_token_data = self.update_tokens()
			self.write_tokens(self.refresh_token_file, refresh_token_data)
			print('Updated 90 day refresh token.')

		if not self.valid_access_token():
			# print('self.valid_access_token()')
			refresh_token_data = self.read_tokens(self.refresh_token_file)
			# print(f'refresh_token_data = {refresh_token_data}')
			access_token_data = self.update_access_token(refresh_token_data["refresh_token"])
			print('Should be a dictionary --->')
			print('41 access_token:')
			print( type( access_token_data ))
			print( access_token_data )
			if 'error' in access_token_data:
				print('invalid access token:')
				print( access_token_data )
				os.remove(self.access_token_file)
				os.remove(self.refresh_token_file)
				print('Possibly due to invalidated refresh token --> rerun')
				exit()

			if 'error' not in access_token_data:
				self.write_tokens(self.access_token_file, access_token_data)
				self.access_token = access_token_data["access_token"]
				print('Updated 30 minute access token.')


	def valid_refresh_token(self):
		if not Path.exists(self.refresh_token_file):
			return False

		refresh_token_data = self.read_tokens(self.refresh_token_file)
		expiration_date = refresh_token_data["time"] \
		+ refresh_token_data["refresh_token_expires_in"]
		print(f'expiration_date = {expiration_date}')
		print(f'current time = {time.time()}')
		if time.time() < expiration_date:
			print('It has been less than 90 days --> Valid Refresh Token')
			return True
		if expiration_date < time.time():
			print('It has been more than 90 days --> Expired Refresh Token')
			return False


	def valid_access_token(self):
		if not Path.exists(self.access_token_file):
			print('Access Token File does not exist.')
			return False
		access_token_data = self.read_tokens(self.access_token_file)
		print(f'access_token_data: {access_token_data}')
		if not access_token_data:
			#	The file may accidentally be empty.
			return False

		if 'expires_in' not in access_token_data:
			return False

		seconds_to_expire = access_token_data["time"] + access_token_data["expires_in"] - time.time()
		print(f'seconds_to_expire = {seconds_to_expire}')
		if seconds_to_expire > 0:
			print('It has been less than 30 minutes ➙ Valid Access Token')
			self.access_token = access_token_data["access_token"]
			return True
		else:
			print('Access Token has expired past its 30 minute life')
			return False


	def read_tokens(self, file_name):
		if Path.exists(file_name):
			f = open(file_name, "r")
			contents = f.read()
			print(f'contents: {contents}')
			if not contents:
				# run time error could cause empty file.
				os.remove(file_name)
				return {}
			d = ast.literal_eval(contents)
			return d
		else:
			print(f'{file_name} does not exist.')
			return {}

	def write_tokens(self, file_name, tokens):
		print('write_tokens:')
		print(tokens)
		print('******************************')
		f = open(file_name, "w")
		f.write( str( tokens ) + '\r\n')
		f.close()
		print('File Saved')
		print()

	def update_tokens(self):
		authorization_code = self.get_authorization_code()
		refresh_token_data = self.update_refresh_token(authorization_code)
		print(refresh_token_data)
		return refresh_token_data

	def get_authorization_code(self):
		# Chrome, Help, About Google Chrome → version needs to match driver.
		# chrome 14 & prior:
		# executable_path = {'executable_path': r'C:\Z\drivers\chromedriver.exe'}
		# browser = Browser('chrome', **executable_path, headless = False)
		# Version 116.0.5845.179 (Official Build) (x86_64)
		# Chrome 115 & newer does not need executable_path
		browser = Browser('chrome', headless = False)
		method = 'GET'
		url = 'https://auth.tdameritrade.com/auth?'
		payload = {'response_type':'code', 'redirect_uri':redirect_uri, 'client_id':client_id + '@AMER.OAUTHAP'}
		oauth_url = requests.Request(method, url, params = payload).prepare()

		browser.visit(oauth_url.url)
		browser.find_by_id("username0").first.fill(username)
		browser.find_by_id("password1").first.fill(password)
		browser.find_by_id("accept").first.click()
		time.sleep(2)
		browser.find_by_id("accept").first.click()		# Get Code Via Text Message - Continue buttone
		time.sleep(2)
		browser.find_by_id("smscode0").first.fill(" ")
		# Need time to manually enter TDA text key
		# Check trust this computer
		# Manually click continue
		time.sleep(50)

		# Click to 'Continue'
		# browser.find_by_id("accept").first.click()
		# time.sleep(3)

		# Click to 'Continue'
		browser.find_by_id("accept").first.click()
		time.sleep(3)
		authorization_code = urllib.parse.unquote(browser.url.split('code=')[1])
		browser.quit()
		return authorization_code

	def update_refresh_token(self, authorization_code):
		url = r'https://api.tdameritrade.com/v1/oauth2/token'
		headers = {'Content-Type': "application/x-www-form-urlencoded"}
		payload = {
					'grant_type': 'authorization_code',
					'access_type': 'offline',
					'code': authorization_code,
					'client_id': client_id,
					'redirect_uri': redirect_uri
				}
		response = requests.post(url, headers = headers, data = payload)
		token = response.json()
		token["time"] = int(time.time())
		return json.dumps(token)


	def update_access_token(self, refresh_token):
		url = r'https://api.tdameritrade.com/v1/oauth2/token'
		headers = {'Content-Type':"application/x-www-form-urlencoded"}
		payload = {
					'grant_type': 'refresh_token',
					'refresh_token': refresh_token,
					'client_id': client_id,
					'redirect_uri': redirect_uri
				}
		response = requests.post(url, headers = headers, data = payload)
		token = response.json()
		token["time"] = int(time.time())
		token_string = json.dumps(token)		# Formatting with double quotes
		token = json.loads(token_string)
		return token


	def get_principals(self):
		if not self.access_token:
			print('get_principles -> no access token')
			access_token_data = self.read_tokens(self.access_token_file)
			self.access_token = access_token_data["access_token"]
		endpoint = 'https://api.tdameritrade.com/v1/userprincipals'
		headers = {'Authorization':'Bearer {}'.format(self.access_token)}
		params = {'fields': 'streamerSubscriptionKeys,streamerConnectionInfo'}
		content = requests.get( url = endpoint, params = params, headers = headers )
		principals = content.json()
		principals_string = json.dumps(principals)
		principals_json = json.loads(principals_string)
		return principals_json