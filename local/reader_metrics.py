import os
import sys

def main(argv):
	#edit month of interest and author name in wikicharts script
	#-p flag prompts for input, -i flag hides display
	args = '-i'
	os.system(f'python individual_chart_scripts/content_interactions_mod.py {args}')
	os.system(f'python individual_chart_scripts/unique_devices_mod.py {args}')

if __name__ == "__main__":
	main(sys.argv[1:])