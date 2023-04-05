# TD Ameritrade OAuth 2.0 authorization script
# This python script opens a browser,
# invokes a TD Ameritrade OAuth server
# with a url to receive an authorization code.
# Submits TD Ameritrade login information to receive tokens.
# https://github.com/2020dataanalysis/OAuth2.git
# OAuth.ipynb
# 06/21/2020
# 11/27/2020 Revised user
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
import os, requests, time, urllib
from splinter import Browser
from selenium import webdriver
from credentials import client_id, username, password, redirect_uri
import pathlib import Path




# home = "C:\\Z\\Python\\TDA\\OAuth"
# home = "~/Applications/TDA"
home = '/Users/samsuper/Applications/TDA'

class OAuth:
	def __init__(self):
		self.tokens = self.get_tokens()
		# print( str( self.tokens ))

		# if type( self.tokens ) is not dict:
		# 	self.tokens = self.get_OAuth()
		
		# self.principles = self.get_principles()
		# # if self.principles['error'] == 'The access token being passed has expired or is invalid.':
		# if 'error' in self.principles:
		# 	print( 'Need to re authorize')
		# 	self.tokens = self.get_OAuth()



	def get_tokens(self):
		global home
		# home = "C:\Z\Python\TDA\OAuth"
		# os.chdir(home)
		os.chdir('/Users/samsuper/Applications/TDA')

		# logfile = "C:\\Z\\Python\\TDA\\OAuth\\tokens.txt"
		logfile = "~/Applications/TDA/tokens.txt"
		# print('get_tokens()')
		if os.path.isfile( logfile ):
			# print( 'tokens.txt is a file.')
			f = open("~/Applications/TDA/tokens.txt", "r")
			# fl = f.readlines()
			# for x in fl:
			# 	print (x)
			contents = f.read()
			d = ast.literal_eval( contents )
			return d

				# a = x.split('→')
				# relog_event( a[0], a[1].strip() )			#	Strip the left space & right carriage return
		else:
			# print('Not a file. **************************')
			return ''


	def get_OAuth(self):
		# Chrome, Help, About Google Chrome → version needs to match driver.
		executable_path = {'executable_path': r'C:\Z\drivers\chromedriver.exe' }
		browser = Browser('chrome', **executable_path, headless = False )

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

		#time.sleep(3)
		#browser.find_by_id("accept_pre").first.click()

		# Need time to manually enter TDA text key

		time.sleep(30)

		# Click to 'Continue'
		browser.find_by_id("accept").first.click()
		time.sleep(1)

		authorization_code = urllib.parse.unquote(browser.url.split('code=')[1])
		browser.quit()

		# Request Post Access Token
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

		# Convert python object into a JSON string
		tokens = response.json()
		#print(tokens)
		# print(tokens['access_token'])

		self.save_tokens( tokens )
		return tokens


	def save_tokens( self, d ):
		global home
		# home = "/home/pi/Desktop/sentinel"
		home = '/Users/samsuper/Applications/TDA'
		# os.chdir(home)
		# logfile = "C:\Z\Python\TDA\OAuth\tokens.txt"
		f = open("/Users/samsuper/Applications/TDA/tokens.txt","w+")
		f.write( str( d ) + '\r\n' )
		f.close()
		print('File Saved..............')



	def get_principles(self):
		endpoint = 'https://api.tdameritrade.com/v1/userprincipals'
		headers = {'Authorization':'Bearer {}'.format(self.tokens['access_token'])}
		# params = {'direction': 'down', 'change': 'percent'}
		content = requests.get( url = endpoint, headers = headers )
		principles = content.json()

		print( principles )
		return principles