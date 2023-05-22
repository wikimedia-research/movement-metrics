import os

def main():
	#get original path this script is being run from (for reset)
	current_script_path = os.getcwd()
	#get path this script exists in
	path_to_this_script = os.path.realpath(os.path.dirname(__file__))
	print("Changing directory to:" + path_to_this_script)
	os.chdir(path_to_this_script)

	#local
	os.system(f'python active_editors.py')
	os.system(f'python new_returning_editors.py')
	os.system(f'python net_new_content.py')

	#jupyter notebook
	'''
	%run active_editors.ipynb
	%run new_returning_editors.ipynb
	%run net_new_content.
	'''

	#reset directory to original
	print("Resetting directory to:" + path_to_this_script)
	os.chdir(current_script_path)

if __name__ == "__main__":
	main()