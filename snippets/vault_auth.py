#!/usr/bin/env python

import argparse
import requests
import json

parser = argparse.ArgumentParser(description='Vault auth/get')
parser.add_argument('-s', '--server', help='[-s <vault_ip>:<port>]', required=True)
parser.add_argument('-p', '--secret-path', help='[-p <path/to/secret>]', required=True)
parser.add_argument('-r', '--role-id', help='[-r <role_id>]', required=True)
parser.add_argument('-S', '--secret-id', help='[-S <secret_id>]', required=True)

args = parser.parse_args()

class Vault(object):
	"""Creates Vault object"""
	def __init__(self, args):
		self.vault_server_endpoint = args.server
		self.secret_path = args.secret_path
		self.role_id = args.role_id
		self.secret_id = args.secret_id

	def vault_auth(self):

		data = ('{"role_id": "%s" ,"secret_id":"%s"}' % (self.role_id, self.secret_id))
		try:
			vault_token_request = requests.post('http://' + self.vault_server_endpoint + '/v1/auth/approle/login', data = data)

			if not vault_token_request.status_code // 100 == 2:
				return "Error: Unexpected response {}".format(vault_token_request.status_code)

			vault_token = json.loads(vault_token_request.text)
			return vault_token['auth']['client_token']


		except requests.exceptions.RequestException as e:
			return "Error: {}".format(e)        


def args_check():
	return 0

if __name__ == '__main__':

   	vault = Vault(args)
   	print vault.vault_auth()
