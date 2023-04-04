#python
'''testing the Schema part
'''

import datetime
import json
import logging
import pathlib

__version__ = '0.0.1'

LOGGER = logging.getLogger(__name__)


class BaseAttribute:
	
	@staticmethod
	def from_schema(type_, multiValued = False, multiValuedAttributeChildName = None, subAttributes = None, **features):
		
		if multiValued:
			result = MultiValuedAttribute(type = type_, multiValued = multiValued, multiValuedAttributeChildName = multiValuedAttributeChildName, **features)
		elif type_.lower() == 'complex':
			if subAttributes is not None:
				features['subAttributes'] = subAttributes
			return ComplexAttribute(type = type_, multiValued = multiValued, **features)
		else:
			return SimpleAttribute(type = type_, multiValued = multiValued, **features)
	
	def _adopt_features(self, **features):
		
		for feature_name, feature_value in features:
			setattr(self, feature_name, feature_value)
 

class SimpleAttribute:

	def __init__(self, **features):
		
		pass


class MultiValuedAttribute(list):
	
	def __init__(self, **features):
		
		super().__init__()


class ComplexAttribute(dict):
	
	def __init__(self, **features):
		
		super().__init__()


class Resource(dict):
	
	def __init__(self, *schemas, **attributes):
		
		super().__init__()
		
		


class Schema:
	
	SCHEMAS_ROOT_DIR = 'schemas'
	
	def __init__(self, *args, **kwargs):
		print('Initializineg with ', args, kwargs)
	
	@classmethod
	def from_builtin(cls, partial_urn):
		path = pathlib.Path(__file__).parent / cls.SCHEMAS_ROOT_DIR 
		return cls(path)


if __name__ == '__main__':
	Schema.from_builtin('core:1.0:User')
	# print()

