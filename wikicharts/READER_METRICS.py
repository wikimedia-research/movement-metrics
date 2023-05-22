import os

def main():
	#edit month of interest and author name in wikicharts script
	os.system(f'python content_interactions.py')
	os.system(f'python unique_devices.py')

if __name__ == "__main__":
	main()