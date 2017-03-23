#!/usr/bin/env python3
import i3
from time import sleep
from sys import stdout

total_workspaces = 10
urgent_active = False
labels = ["", "", "", "", "", "", "", "", "", ""]
colors = ["#a54242", "#c5c8c6", "#de935f", "#5f819d", "#85678f", "#5e8d87", "#707880", "#f0c674", "#FFFFFF", "#b5bd68"]
labels_inuse = ["➀", "➁", "➂", "➃", "➄", "➅", "➆", "➇", "➈", ""]
labels_focus = ["➊", "➋", "➌", "➍", "➎", "➏", "➐", "➑", "➒", "➓"]

def default_format(string):
	return string

def used_ws(string):
	return "<span>{}</span>".format(string)

def empty_ws(string):
	return "<span color=\"#494d1e\">{}</span>".format(string)

def focus_ws(string):
	return "<span underline=\"low\">{}</span>".format(used_ws(string))

def urgent_ws(string):
	if urgent_active:
		return "<span color=\"#FF0000\">{}</span>".format(used_ws(string))
	else:
		return string

def prepend_index(string, index):
	return "{}<sub>{}</sub>".format(string, index)

def set_color(string, index):
	return "<span color=\"{}\">{}</span>".format(colors[index - 1], string)

def workspace_event_handler(event, data, subscription):
	# map the output of the i3 IPC to a
	# more usefull list which also represents
	# the empty workspaces with "None" objects
	print("<span font=\"11\">", end="")
	workspaces = [None] * total_workspaces
	for workspace in data:
		workspaces[workspace["num"] - 1] = workspace

	ws_number = 1
	for ws in workspaces:
		formatted_string = default_format(labels[ws_number - 1])
		if ws is None:
			formatted_string = empty_ws(prepend_index(formatted_string, ws_number))
		elif ws["focused"] is True:
			formatted_string = prepend_index(focus_ws(formatted_string), ws_number)
		else:
			formatted_string = prepend_index(used_ws(formatted_string), ws_number)

		formatted_string = set_color(formatted_string, ws_number)
		if ws is not None and ws["urgent"]:
			formatted_string = urgent_ws(formatted_string)

		print(formatted_string, end="  ")
		ws_number += 1

	print("</span>", end="")
	print() # new line
	stdout.flush()

data = i3.get_workspaces()
workspace_event_handler(None, data, None)
while True:
	subscription = i3.Subscription(workspace_event_handler, "workspace")
	while subscription.is_alive:
		sleep(0.2)
	data = i3.get_workspaces()
	workspace_event_handler(None, data, None)
	subscription = i3.Subscription(workspace_event_handler, "workspace")

