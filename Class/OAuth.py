# TD Ameritrade OAuth 2.0 authorization script
# This python script opens a browser,
# invokes a TD Ameritrade OAuth server
# with a url to receive an authorization code.
# Submits TD Ameritrade login information to receive tokens.
# https://github.com/2020dataanalysis/OAuth2.git
# OAuth.ipynb
# 06/21/2020
# 11/27/2020 Revised user
# 2023.04.05 Start of many revisions
# Author Sam Portillo

# References:
#   https://oauth.net/2/
#   https://developer.tdameritrade.com/


# conda activate TDA
# conda install -n myenv scipy
# conda install -n myenv pip
# conda activate myenv
# pip <pip_subcommand>
# ipython kernel install --name TDA --user
# or
# python -m ipykernel install --user

import ast
import os, requests, time, urllib, json
from splinter import Browser
from selenium import webdriver
from credentials import client_id, username, password, redirect_uri
from pathlib import Path
from selenium.webdriver.common.keys import Keys


class OAuth:
	def __init__(self):
		self.current_working_directory = Path.cwd()
		self.refresh_token_file = self.current_working_directory / 'refresh_token.json'
		self.access_token_file = self.current_working_directory / 'access_token.json'
		print( self.refresh_token_file )
		if not self.valid_refresh_token():
			refresh_token = update_OAuth2_tokens()
			self.write_tokens(self.refresh_token_file, refresh_token)

		if not self.valid_access_token():
			refresh_token = self.read_tokens(self.refresh_token_file)
			access_token = self.update_OAuth2_refresh_token(refresh_token["refresh_token"])				
			self.write_tokens(self.access_token_file, access_token)


	def valid_refresh_token(self):
		if not Path.exists(self.refresh_token_file):
			return False

		refresh_token = self.read_tokens(self.refresh_token_file)
		expiration_date = refresh_token["time"] \
		+ refresh_token["refresh_token_expires_in"]
		print(f'expiration_date = {expiration_date}')
		print(f'current time = {time.time()}')
		if time.time() < expiration_date:
			print('It has been less than 90 days --> Valid Refresh Token')
			return True
		if expiration_date < time.time():
			print('It has been more than 90 days --> Expired Refresh Token')
			# refresh_token = None
			return False


	def valid_access_token(self):
		if not Path.exists(self.access_token_file):
			print('Access Token File does not exist.')
			return False
	
		access_token = self.read_tokens(self.access_token_file)
		if access_token["time"] + access_token["expires_in"] > time.time():
			print('Valid Access Token')
			self.access_token = access_token["access_token"]
			return True
		else:
			print('Access Token has expired past its 30 minute life')
			return False


	def read_tokens(self, file_name):
		if Path.exists(file_name):
			# print( 'tokens.txt is a file.')
			f = open(file_name, "r")
			contents = f.read()
			d = ast.literal_eval( contents )
			return d

				# a = x.split('→')
				# relog_event( a[0], a[1].strip() )			#	Strip the left space & right carriage return
		else:
			print(f'{file_name} does not exist.')
			return {}


	def write_tokens(self, file_name, tokens):
		f = open(file_name, "w+")
		f.write( str( tokens ) + '\r\n')
		f.close()
		print('File Saved')
		print()


	def update_OAuth2_tokens(self):
		# Chrome, Help, About Google Chrome → version needs to match driver.
		executable_path = {'executable_path': r'C:\Z\drivers\chromedriver.exe'}
		browser = Browser('chrome', **executable_path, headless = False)

		# Build OAuth 2.0 url
		method = 'GET'
		url = 'https://auth.tdameritrade.com/auth?'
		payload = {'response_type':'code', 'redirect_uri':redirect_uri, 'client_id':client_id + '@AMER.OAUTHAP'}
		oauth_url = requests.Request(method, url, params = payload).prepare()
		browser.visit(oauth_url.url)
		# Fill out each element in the form
		browser.find_by_id("username0").first.fill(username)
		browser.find_by_id("password1").first.fill(password)
		browser.find_by_id("accept").first.click()

		time.sleep(3)
		browser.find_by_id("accept").first.click()		# Get Code Via Text Message - Continue buttone
		# Need time to manually enter TDA text key

		time.sleep(2)
		# smscode0
		browser.find_by_id("smscode0").first.fill("1")
		# Actions builder = new Actions(driver);
		# builder.keyDown(Keys.TAB).perform()
		# browser.type(Keys.TAB)
		# browser.type(Keys.RETURN)
		# x = browser.is_element_visible_by_css("rememberdevice", 10)
		# print(f'x = {x}')
		# browser.find_by_id("rememberdevice").click()
		# browser.find_by_name("rememberdevice").click()
		# browser.find_by_xpath('//*[@id="rememberdevice"]').click()

		time.sleep(30)

		# Click to 'Continue'
		browser.find_by_id("accept").first.click()
		time.sleep(5)
		# Click to 'Continue'
		browser.find_by_id("accept").first.click()

		time.sleep(3)
		authorization_code = urllib.parse.unquote(browser.url.split('code=')[1])
		# browser.quit()
		url = r'https://api.tdameritrade.com/v1/oauth2/token'
		headers = {'Content-Type':"application/x-www-form-urlencoded"}
		payload = {
					'grant_type':'authorization_code',
					'access_type':'offline',
					'code':authorization_code,
					'client_id':client_id,
					'redirect_uri':redirect_uri
				}
		response = requests.post(url, headers = headers, data = payload)
		tokens = response.json()
		tokens["time"] = int(time.time())
		refresh_token = json.dumps(tokens)
		print(refresh_token)
		return refresh_token

	def update_OAuth2_refresh_token(self, refresh_token):
		url = r'https://api.tdameritrade.com/v1/oauth2/token'
		headers = {'Content-Type':"application/x-www-form-urlencoded"}
		payload = {
					'grant_type': 'refresh_token',
					'refresh_token': refresh_token,
					'client_id':client_id,
					'redirect_uri':redirect_uri
				}
		response = requests.post(url, headers = headers, data = payload)
		tokens = response.json()
		tokens["time"] = int(time.time())
		tokens = json.dumps(tokens)		# Formatting with double quotes
		return tokens


	def get_principles(self):
		if not self.access_token:
			print('get_principles -> no access token')
			access_token_data = self.read_tokens(self.access_token_file)
			self.access_token = access_token_data["access_token"]

		endpoint = 'https://api.tdameritrade.com/v1/userprincipals'
		headers = {'Authorization':'Bearer {}'.format(self.access_token)}
		# params = {'direction': 'down', 'change': 'percent'}
		content = requests.get( url = endpoint, headers = headers )
		principles = content.json()

		# print( principles )
		return principles
