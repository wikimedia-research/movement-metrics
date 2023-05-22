import os

def main():
	#edit month of interest and author name in wikicharts script
	os.system(f'python active_editors.py')
	os.system(f'python new_returning_editors.py')
	os.system(f'python net_new_content.py')

if __name__ == "__main__":
	main()