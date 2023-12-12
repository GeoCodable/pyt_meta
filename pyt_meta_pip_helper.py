import os, sys, time

# -----------------------------------------------------------------------------

def get_pip_cmds(pacakge_name, github_url, wait_sec=15) :
    '''Function prints instructions to perform pip installs from
    a GitHUb repo.  After instructions are printed, a command
    line (cmd) terminal will be launched for the user after a
    wait period. 
    :param - pacakge_name  - name of package to be installed
    :param - github_url  - repo & version https url
    :param - wait_sec  - seconds to wait before opening cmd
    :returns - none -
    '''
    # create the standard instructions
    insts = [
        '***Instructions to install: {0}***'.format(pacakge_name), 
        '  A command line terminal will open after {0} seconds'.format(wait_sec),
        '    Note: "pip install --upgrade pip" is a recommended, but optional command\n',
        '  Copy each line below into the open command line terminal one at a time:',
        '-' * 115 + '\n', 
        '    cd "{0}"'.format(os.path.dirname(os.path.realpath(sys.executable))),
        '    pip install --upgrade pip',
        '    pip install git+{0}'.format(github_url),
        '\n' + '-' * 115, ]
    # print the instructions
    [print(_) for _ in insts]

    # give the user time to read the instructions before opening cmd
    print('The command line will open in:')
    for _ in range(wait_sec,0,-1):
        if _ > 0:
            print(_, end='...\r')
        time.sleep(1)

    # open cmd    
    os.system("start /wait cmd")
    print('\nRemember to post issues, questions and feedback on  GitHub @:\n\t', github_url)

# -----------------------------------------------------------------------------

pacakge_name = 'pyt_meta'
github_url = r'https://github.com/ngageoint/python-toolbox-metadata-addon'
get_pip_cmds(pacakge_name, github_url, 20)

# -----------------------------------------------------------------------------
