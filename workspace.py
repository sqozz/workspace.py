#!/usr/bin/env python3
import i3 as i3
from time import sleep
from sys import stdout

# labels define the icons for each workspace
# colors is the color of each label
labels = ["",				"",				"",				"",				"",				"",				"",				"",				"",				""]
colors = ["#a54242",	"#c5c8c6",	"#de935f",	"#5f819d",	"#85678f",	"#5e8d87",	"#707880",	"#f0c674",	"#FFFFFF",	"#b5bd68"]
total_workspaces = 10 # how many maximum workspaces you have
loop_sleep = 0.1 # smaller numbers means more loop runs so more responivenes for workspace changes
tick_every = 0.2 # seconds on urgent; 0 = disabled; multiple of loop_sleep
urgent_pattern = "--__---___-----_____---___" # pattern in which the icon should change color if workspace is urgent
urgent_color = "#ff0000" # color for the label if workspace is urgent


## Internal stuff - not suposed to be modified but with a short explaination
urgent_active = False # urgent_color applied on label or not. Enables the blinking on orgent
urgent_counter = 0 # walks up by one on every tick
patternPos = 0 # walks up to len(urgent_pattern) on every blink
interval = tick_every / loop_sleep # magic value that allows blinking interval independent of loop_sleep

# more classic labels
# labels_1 = ["➀", "➁", "➂", "➃", "➄", "➅", "➆", "➇", "➈", ""]
# labels_2 = ["➊", "➋", "➌", "➍", "➎", "➏", "➐", "➑", "➒", "➓"]

def default_format(string):
	return string

def used_ws(string):
	return string
	return "<span>{}</span>".format(string)

def empty_ws(string):
	return "<span color=\"#494d1e\">{}</span>".format(string)

def focus_ws(string):
	return "<span underline=\"low\">{}</span>".format(used_ws(string))

def urgent_ws(string):
		return "<span color=\"" + urgent_color + "\">{}</span>".format(used_ws(string))

def prepend_index(string, index):
	return "{}<sub>{}</sub>".format(string, index)

def set_color(string, index):
	return "<span color=\"{}\">{}</span>".format(colors[index - 1], string)


while True:
	if tick_every != 0:
		urgent_counter += 1

		if urgent_counter % interval == 0:
			if urgent_pattern[patternPos] is "_":
				urgent_active = False
			else:
				urgent_active = True

			patternPos += 1

		if urgent_counter >= interval:
			urgent_counter = 0

		if patternPos >= len(urgent_pattern):
			patternPos = 0

	data = i3.get_workspaces()
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

		if ws is not None and ws["urgent"]:
			if urgent_active:
				formatted_string = urgent_ws(formatted_string)
			else:
				formatted_string = set_color(formatted_string, ws_number)
		else:
			formatted_string = set_color(formatted_string, ws_number)

		print(formatted_string, end="  ")
		ws_number += 1

	print("</span>", end="")
	print() # new line
	stdout.flush()

	sleep(loop_sleep)

# vim: noexpandtab:ts=2:sw=2:sts=2
