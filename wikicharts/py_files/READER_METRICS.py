import os

def main():
    #get original path this script is being run from (for reset)
    current_script_path = os.getcwd()
    #get path this script exists in
    path_to_this_script = os.path.realpath(os.path.dirname(__file__))
    print("Changing directory to:" + path_to_this_script)
    os.chdir(path_to_this_script)

    #local
    os.system(f'python content_interactions.py')
    os.system(f'python unique_devices.py')

    #jupyter notebook
    '''
    %run content_interactions.ipynb
    %run unique_devices.ipynb
    '''

    #reset directory to original
    print("Resetting directory to:" + path_to_this_script)
    os.chdir(current_script_path)

if __name__ == "__main__":
    main()