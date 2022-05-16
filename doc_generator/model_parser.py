#!/usr/bin/env python3

import ast

def str_node(node):
	if isinstance(node, ast.AST):
		fields = [(name, str_node(val)) for name, val in ast.iter_fields(node) if name not in ('left', 'right')]
		return '%s(%s)' % (node.__class__.__name__, ', '.join('%s=%s' % field for field in fields))
	else:
		return repr(node)

def ast_visit(node, level=0):
	print('  ' * level + str_node(node))
	for field, value in ast.iter_fields(node):
		if isinstance(value, list):
			for item in value:
				if isinstance(item, ast.AST):
					ast_visit(item, level=level+1)
		elif isinstance(value, ast.AST):
			ast_visit(value, level=level+1)


### SOURCE PARSING

def is_model_field(field):
	return (
		isinstance(field, ast.Assign) 
		and isinstance(field.value, ast.Call)
		and field.value.func.value.id == 'models'
	)

def is_choices_list(field):
	return (
		isinstance(field, ast.Assign)
		and isinstance(field.value, ast.List)
		and "CHOICES" in field.targets[0].id
	)
	# [print(k.value.id) for k in field.value.keywords if k.arg == 'choices']

def parse_class(node):
	# print(node.name)
	model = {'name': node.name, 'fields': []}

	choices = {}

	# ast_visit(node)
	
	for field in node.body:
		if is_model_field(field):
			# ast_visit(field)
			name = field.targets[0].id
			field_type = field.value.func.attr
			options = {}

			choices_idx = next((i for i, kw in enumerate(field.value.keywords) if kw.arg == "choices"), None)
			if choices_idx is not None:
				choices_list_name = field.value.keywords[choices_idx].value.id
				options['choices'] = choices[choices_list_name]
			
			if field_type == "ForeignKey":
				# ast_visit(field.value)
				options['to'] = next(kw.value.id for kw in field.value.keywords if kw.arg == "to")

			model['fields'].append(
				{
					'name': name,
					'type': field_type,
					'opts': options
				}
			)
		elif is_choices_list(field):
			name = field.targets[0].id
			choices[name] = [item.elts[1].value for item in field.value.elts]
	return model

def parse_models(tree):
	r = []
	for field, value in ast.iter_fields(tree):
		if isinstance(value, list):
			for item in value:
				if isinstance(item, ast.ClassDef):
					r.append(parse_class(item))
	return r

def make_models(source):
	tree = ast.parse(source)
	return parse_models(tree)

if __name__ == "__main__":
	import sys
	import json

	source_file = sys.argv[1]
	with open(source_file, 'r') as f:
		source = f.read()
	models = make_models(source)

	print(json.dumps(models, indent=2))



# class Walker(ast.NodeVisitor):

# 	def generic_visit(self, node):
# 		r = []
# 		for field, value in ast.iter_fields(node):
# 			if isinstance(value, list):
# 				for item in value:
# 					if isinstance(item, ast.ClassDef):
# 						r.append(self.visit(item))
# 		return r

# 	def visit_ClassDef(self, node):
# 		# print(node.name)
# 		model = {'name': node.name, 'fields': []}

# 		choices = {}

# 		for field in node.body:
# 			if is_model_field(field):
# 				# ast_visit(field)
# 				name = field.targets[0].id
# 				field_type = field.value.func.attr
# 				options = []

# 				choices_idx = next((i for i, kw in enumerate(field.value.keywords) if kw.arg == "choices"), None)
# 				if choices_idx is not None:
# 					choices_list_name = field.value.keywords[choices_idx].value.id
# 					options.append(
# 						{
# 							'choices': choices[choices_list_name]
# 						}
# 					)
				
# 				model['fields'].append(
# 					{
# 						'name': name,
# 						'type': field_type,
# 						'opts': options
# 					}
# 				)
# 			elif is_choices_list(field):
# 				name = field.targets[0].id
# 				choices[name] = [item.elts[1].value for item in field.value.elts]
# 		return model