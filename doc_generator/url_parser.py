#!/usr/bin/env python3

import ast

from model_parser import ast_visit


def get_endpoint(node):
	# print("*"*20)
	# ast_visit(node)
	return {
		'base': node.value.func.value.id,
		'endpoint': node.value.args[0].value,
		'model': node.value.args[1].attr.removesuffix("ViewSet")
	}

def get_router(node):
	# print("*"*20)
	# ast_visit(node)
	return {
		'name': node.targets[0].id,
		'parent': next((arg.id for arg in node.value.args if isinstance(arg, ast.Name)), None),
		'lookup': next((kw.value.value for kw in node.value.keywords if kw.arg == "lookup"), None)
	}

def parse_urls(tree):
	routers = []
	endpoints = []

	for field, value in ast.iter_fields(tree):
		if isinstance(value, list):
			for item in value:
				if isinstance(item, ast.Assign) and "router" in item.targets[0].id:
					routers.append(get_router(item))
				if isinstance(item, ast.Expr) and "route" in item.value.func.value.id:
					endpoints.append(get_endpoint(item))
	# print(json.dumps(endpoints, indent=2))
	return routers, endpoints


def get_paths(source):
	tree = ast.parse(source)
	routers, endpoints = parse_urls(tree)

	def build_path(e):
		r = next(r for r in routers if r['name'] == e['base'])
		if r['parent'] is None:
			return [(e['endpoint'], e['model'])]
		else:
			return next(e for e in endpoints if e['base'] == r['parent'])['path'] + [(e['endpoint'], e['model'])]

	for e in endpoints:
		e['path'] = build_path(e)
	return endpoints

if __name__ == "__main__":
	import sys
	import json

	source_file = sys.argv[1]
	with open(source_file, 'r') as f:
		source = f.read()
	paths = get_paths(source)
	print(json.dumps(paths, indent=2))
