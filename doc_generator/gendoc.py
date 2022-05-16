#!/usr/bin/env python3

import sys
import json

from copy import deepcopy

from model_parser import make_models
from url_parser import get_paths

collection_base = {
	"info": {
		"_postman_id": "4ab59fae-0f44-4ad6-988e-c545038c6ae4",
		"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
	},
	"auth": {
		"type": "bearer",
		"bearer": [
			{
				"key": "token",
				"value": "{{jwt_token}}",
				"type": "string"
			}
		]
	},
	"event": [],
	"variable": [
		{
			"key": "jwt_token",
			"value": "",
			"type": "string",
			"disabled": True
		}
	]
}

item_base = {
	"name": "name",
	"event": [
		{
			"listen": "test",
			"script": {
				"type": "text/javascript"
			}
		}
	],
	"request": {
		"auth": {
			"type": "bearer",
			"bearer": [
				{
					"key": "token",
					"value": "{{jwt_token}}",
					"type": "string"
				}
			]
		},
		"method": "method",
		"header": [],
		"url": {
			"host": [
				"localhost"
			],
			"port": "8000",
			"path": []
		},
	},
	"response": []
}

def make_param_table(model, path):
	return (
		"\n\n"
		"parameters:\n\n"
		"| **name** | **type** | **description** |\n"
		"| --- | --- | --- |\n"
	) + (
		'\n'.join(f"| {f['name']} | {f['type']} | foo |"
	) for f in model['fields'] if not skip_field(f, path))

def make_description(action, model_name, parent):
	if parent is None:
		desc_map = {
			'list': f"Get a list of all {model_name}s.",
			'create': f"create a new {model_name}.",
			'retrieve': f"Get a {model_name} details.",
			'update': f"Update a {model_name}.",
			'destroy': f"Delete a {model_name}."
		}
	else:
		desc_map = {
			'list': f"Get a list of the {parent}'s {model_name}s.",
			'create': f"create a new {model_name} for this {parent}",
			'retrieve': f"Get a{'n' if model_name.startswith(('a', 'e', 'i', 'o', 'u' ,'y')) else ''} {model_name} details.",
			'update': f"Update a{'n' if model_name.startswith(('a', 'e', 'i', 'o', 'u' ,'y')) else ''} {model_name}.",
			'destroy': f"Delete a{'n' if model_name.startswith(('a', 'e', 'i', 'o', 'u' ,'y')) else ''} {model_name}."
		}
	return desc_map[action]

def skip_field(field, path):
	return (
		any(field['opts'].get('to') == m for p, m in path)
		or field['name'].lower() == "author"
		or field['type'] == "DateTimeField"
	)

def make_request(action, path, model=None):
	method_map = {
		'list': "GET",
		'create': "POST",
		'retrieve': "GET",
		'update': "PUT",
		'destroy': "DELETE"
	}
	model_name = path[-1][1].lower()

	# print(f"{action}_{path[-1][0]}")
	p = [el for p, m in path for el in [f"{p}", f"{{{{{m.lower()}_id}}}}"]]
	if action in ["list", "create"]:
		p = p[:-1]
	item = deepcopy(item_base)
	item['name'] = f"{action}_{model_name}"
	item['request']['method'] = method_map[action]
	item['request']['url']['path'] = ["api"] + [el for p, m in path for el in [f"{p}", f"{{{{{m.lower()}_id}}}}"]] + [""]
	item['request']['description'] = make_description(action, model_name, path[-2][1].lower() if len(path) > 1 else None)
	if action in ["create", "update"] and model is not None:
		item['request']['body'] = {
			"mode": "formdata",
			"formdata": []
		}
		item['request']['description'] += (
			"\n\n"
			"parameters:\n\n"
			"| **name** | **type** | **description** |\n"
			"| --- | --- | --- |\n"
		)
		for field in model['fields']:
			if not skip_field(field, path):
				item['request']['body']['formdata'].append(
					{
						"key": field['name'],
						"value": f"{field['name']}_foo",
						"type": "text"
					}
				)
				item['request']['description'] += f"| {field['name']} | {field['type']} | foo |\n"


####3


		# item['request']['body'] = {
		# 	"mode": "formdata",
		# 	"formdata": [
		# 		{
		# 			"key": field['name'],
		# 			"value": f"{field['name']}_foo",
		# 			"type": "text"
		# 		} for field in model['fields'] if not skip_field(field, path)
		# 	]
		# }
		# item['request']['description'].append(make_param_table(field, path))
		# print("_"*20)
		# print(f"{model['name']}: {action}")
		# print("_"*20)
		# print(path)
		# print(json.dumps(model['fields'], indent=2))
		# print(json.dumps(item['request']['body'], indent=2))
	return item

def make_item_from_model(path, model):
	return {
		'name': model['name'],
		'item': [
			make_request('list', path, model),
			make_request('create', path, model),
			make_request('retrieve', path, model),
			make_request('update', path, model),
			make_request('destroy', path, model),
		]
	}

def make_item(path, model):
	if model is not None:
		return make_item_from_model(path, model)
	return None

def main():
	models_file = sys.argv[1]
	with open(models_file, 'r') as f:
		source = f.read()
	models = make_models(source)

	url_file = sys.argv[2]
	with open(url_file, 'r') as f:
		source = f.read()
	paths = get_paths(source)

	# print(json.dumps(paths, indent=2))

	collection = collection_base
	collection['info']['name'] = (sys.argv[3:4] or ["collection"])[0]
	collection["item"] = [
		make_item(p['path'], next((m for m in models if m['name'] == p['model']), None))
		for p in paths if next((m for m in models if m['name'] == p['model']), None) is not None
	]

	print(json.dumps(collection, indent=2))

if __name__ == "__main__":
	main()



# def make_list(model, path):
# 	item = deepcopy(item_base)
# 	item['name'] = f"list_{path[-2]}"
# 	item['request']['method'] = "GET"
# 	item['request']['url']['path'] = path[:-1] + [""]
# 	item['request']['description'] = f"get a list of all {path[-2]}"
# 	item['event'][0]['script']['exec'] = [
# 		"pm.test(\"Status code is 200\", function () {",
# 		"    pm.response.to.have.status(200);",
# 		"});",
# 		"",
# 		"pm.test(\"Response is a json array\", function () {",
# 		"    pm.response.to.be.json",
# 		"    pm.expect(pm.response.json()).to.be.an('array')",
# 		"});"
# 	]
# 	return item

# def make_create(model, path):
# 	item = deepcopy(item_base)
# 	item['name'] = f"create_{path[-2][:-1]}"
# 	item['request']['method'] = "POST"
# 	item['request']['url']['path'] = path[:-1] + [""]
# 	item['request']['description'] = f"create a new {path[-2][:-1]}"
# 	item['event'][0]['script']['exec'] = [
# 		"pm.test(\"Status code is 201\", function () {",
# 		"    pm.response.to.have.status(201);",
# 		"});",
# 		"",
# 		"const r = pm.response.json();",
# 		f"pm.globals.set(\"{path[-1]}\", r.id);"
# 	]
# 	return item

# def make_retrieve(model, path):
# 	item = deepcopy(item_base)
# 	item['name'] = f"retrieve_{path[-2][:-1]}"
# 	item['request']['method'] = "GET"
# 	item['request']['url']['path'] = path + [""]
# 	item['request']['description'] = f"get a {path[-2][:-1]} details"
# 	item['event'][0]['script']['exec'] = [
# 		"pm.test(\"Status code is 200\", function () {",
# 		"    pm.response.to.have.status(200);",
# 		"});"
# 	]
# 	return item

# def make_update(model, path):
# 	item = deepcopy(item_base)
# 	item['name'] = f"update_{path[-2][:-1]}"
# 	item['request']['method'] = "PUT"
# 	item['request']['url']['path'] = path + [""]
# 	item['request']['description'] = f"update a {path[-2][:-1]}"
# 	item['event'][0]['script']['exec'] = [
# 		"pm.test(\"Status code is 200\", function () {",
# 		"    pm.response.to.have.status(200);",
# 		"});"
# 	]
# 	return item

# def make_destroy(model, path):
# 	item = deepcopy(item_base)
# 	item['name'] = f"destroy_{path[-2][:-1]}"
# 	item['request']['method'] = "DELETE"
# 	item['request']['url']['path'] = path + [""]
# 	item['request']['description'] = f"delete a {path[-2][:-1]}"
# 	item['event'][0]['script']['exec'] = [
# 		"pm.test(\"Status code is 204\", function () {",
# 		"    pm.response.to.have.status(204);",
# 		"});"
# 	]
# 	return item