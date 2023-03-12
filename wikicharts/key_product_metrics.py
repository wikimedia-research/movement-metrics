import os
import sys

def main(argv):
	#-p flag prompts for input, -i flag hides display
	args = '-i'
	os.system(f'python individual_charts/content_interactions_mod.py {args}')
	os.system(f'python individual_charts/active_editors_mod.py {args}')
	os.system(f'python individual_charts/net_new_mod.py {args}')
	os.system(f'python individual_charts/unique_devices_mod.py {args}')

if __name__ == "__main__":
	main(sys.argv[1:])