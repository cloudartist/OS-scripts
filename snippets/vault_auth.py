#!/usr/bin/env python

import argparse
import requests

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
		#vault_token = requests.post('http://' + self.vault_server_endpoint + '/v1/auth/approle/login', data = {"role_id": self.role_id,"secret_id":self.secret_id})
		#vault_token = requests.post("http://7.7.7.73:8200/v1/auth/approle/login", data = '{"role_id": "7f538aca-bcdc-f6e1-fec8-2b6d8689a480", "secret_id": "d3d156fc-2a0e-07dd-0aea-3e5b20705abd"}')
		#print(vault_token.status_code, vault_token.reason)
		#r = requests.post("http://bugs.python.org", data={'number': 12524, 'type': 'issue', 'action': 'show'})
		#print(r.status_code, r.reason)
		#return r
		#return vault_token.text
		data = ('{"role_id": "%s" ,"secret_id":"%s"}' % (self.role_id, self.secret_id))
		try:
			vault_token = requests.post('http://' + self.vault_server_endpoint + '/v1/auth/approle/login', data = data)

			if not vault_token.status_code // 100 == 2:
				return "Error: Unexpected response {}".format(vault_token.status_code)

			#print self.role_id
			return vault_token.text


		except requests.exceptions.RequestException as e:
			return "Error: {}".format(e)        



#	def vault_get_secret():
#		return 0

#'curl -s -X GET -H "X-Vault-Token:$vault_token" http://$vault_server_endpoint/v1/$secret_path | jq -r .data.value


def args_check():
	return 0

if __name__ == '__main__':
	#print vault_server_endpoint
   	vault = Vault(args)
   	print vault.vault_auth()
   	#vault.vault_auth()