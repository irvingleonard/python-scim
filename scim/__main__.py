#!python
'''Environmental Shell Piping
Supplies some utility functions to handle complex data structures as
environmental shell variables. Useful to docker and other CLI tools requiring lots of dynamic data

This is the executable script
'''

import simplifiedapp

try:
	import scim
except ModuleNotFoundError:
	import __init__ as scim

simplifiedapp.main(scim)
