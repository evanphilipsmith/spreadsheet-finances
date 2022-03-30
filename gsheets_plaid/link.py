import os
import shlex
import shutil
import subprocess
import webbrowser
from time import sleep

from gsheets_plaid.initialization import CONFIG


def run_link_server(port: int = None, env: str = None, redirect_uri: str = None):
    """Run Plaid Link flow.
    """
    # Start tiny-quickstart
    command = f'{shutil.which("npm")} start'
    print(shlex.split(command))  # FIXME delete this
    plaid_env = os.environ.copy()
    if port:
        CONFIG['PLAID_LINK_PORT'] = port
    if env:
        CONFIG['PLAID_ENV'] = env
    if redirect_uri:
        CONFIG['PLAID_SANDBOX_REDIRECT_URI'] = redirect_uri
    plaid_env.update(CONFIG)
    p = subprocess.Popen(shlex.split(command), cwd='include/plaid_link_server', env=plaid_env)

    sleep(1)  # Wait for the server to start

    # Direct the user to Plaid Link
    webbrowser.open(f'http://localhost:{CONFIG["PLAID_LINK_PORT"]}/', new=1, autoraise=True)
    p.wait()


if __name__ == '__main__':
    run_link_server()
