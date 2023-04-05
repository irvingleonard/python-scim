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
		
		


class ResourceSchema(dict):
	
	SCHEMAS_ROOT_DIR_NAME = 'schemas'
	
	def __init__(self, *common_attributes, _schema = None, _multi_valued_attributes = None):
		
		super().__init__()
		self.schema = ':'.join(_schema.split(':')[:-1])
		self.common_attributes = list(common_attributes)
		if _multi_valued_attributes is not None:
			self.multi_valued_attributes = _multi_valued_attributes
	
	def __setitem__(self, name, value):
		
		# LOGGER.debug('Setting "%s" with: %s', name, value)
		if 'schema' not in self:
			super().__setitem__('schema', self.schema)
		
		if name == 'attributes':
			value = self.common_attributes + value
			
			for attribute in value:
				if 'schema' not in attribute:
					attribute['schema'] = self.schema
				if attribute['multiValued'] and ('subAttributes' in attribute) and (attribute['type'] == 'complex') and hasattr(self, 'multi_valued_attributes'):
					sub_attributes = {sub_attribute['name'] : sub_attribute for sub_attribute in self.multi_valued_attributes}
					sub_attributes.update({sub_attribute['name'] : sub_attribute for sub_attribute in attribute['subAttributes']})
					attribute['subAttributes'] = list(sub_attributes.values())
		
		super().__setitem__(name, value)
	
	@classmethod
	def _builtin_schema_root_path(cls):
		return pathlib.Path(__file__).parent / cls.SCHEMAS_ROOT_DIR_NAME
	
	@classmethod
	def from_builtin(cls, uri = None):
		
		if uri.startswith('urn:scim:schemas:'):
			LOGGER.debug('Loading a SCIM 1.0 schema...')
			partial_uri = uri[17:].split(':', maxsplit = 3)
			if len(partial_uri) < 3:
				raise ValueError('Not a resource schema: {}'.format(uri))
			core_1_schema = json.loads((cls._builtin_schema_root_path() / 'core' / '1.0.json').read_text())
			LOGGER.debug('Load core:1.0 schema: %s', core_1_schema)
			if partial_uri[0] == 'core':
				if partial_uri[1] != '1.0':
					raise NotImplementedError('Only support SCIM 1.0 schemas with this prefix (urn:scim:schemas:): {}'.format(uri))
				result = cls(*core_1_schema['common'], _schema = uri, _multi_valued_attributes = core_1_schema['multi-valued'])
				resource_path = cls._builtin_schema_root_path() / 'core' / '1.0' / (partial_uri[2] + '.json')
				if not resource_path.is_file():
					raise ValueError('Not a valid core 1.0 resource: {}'.format(partial_uri[2]))
				resource_schema = json.loads(resource_path.read_text())
				result.update(resource_schema)
			elif (partial_uri[0] == 'extension'):
				extension_schema_path = cls._builtin_schema_root_path() / 'extension' / (partial_uri[1] + '.json')
				if not extension_schema_path.is_file():
					raise ValueError('Not a valid extension schema: {}'.format(partial_uri[1]))
				extension_schema = json.loads(extension_schema_path.read_text())
				if partial_uri[2] not in extension_schema:
					raise ValueError('Not a valid extension schema version for {}: {}'.format(partial_uri[1], partial_uri[2]))
				result = cls(_schema = 'urn:scim:schemas:core:1.0:User')
				result['attributes']=[extension_schema[partial_uri[2]]]
			else:
				raise ValueError('Unknown SCIM schema: {}'.format(uri))
		else:
			ValueError('Not a builtin schema: {}'.format(uri))
	
		return result

	def update(self, other):
		for key, value in other.items():
			self[key] = value


def local_schemas():
	
	core_schema_path = pathlib.Path(__file__).parent / Schema.SCHEMAS_ROOT_DIR / 'core' 
	
	core_schema_shared = json.loads((core_schema_path / '1.0.json').read_text())
	core_schema_user = json.loads((core_schema_path / '1.0' / 'User.json').read_text())
	core_schema_group = json.loads((core_schema_path / '1.0' / 'Group.json').read_text())
	
	return core_schema_shared, core_schema_user, core_schema_group
