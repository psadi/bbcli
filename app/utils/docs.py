#-*- coding: utf-8 -*-

from app import __version__
from app.utils.richprint import markdown_to_console

def alt():
    """.alt file configuration"""
    return """
### .ALT FILE CONFIGURATION

- Place the .alt file in your home directory, **https://raw.githubusercontent.com/psadi/bbcli/main/.alt** for raw file

```text
[default]
bitbucket_host=https://bitbucket.mycompany.com
username=myusername
token=thisisarandomwriteaccesstokengeneratedbybitbucket
```
---
"""

def install():
    """bb installation"""
    return f"""
### INSTALLATION

* Manual

```text
git clone https://github.com/psadi/bbcli.git
cd bb
pip3 install --user -r requirements.txt
poetry build
pip3 install --user dist/bb-<version>.tar.gz
```

* From Releases
* Download the latest build from releases page

```text
pip3 install --user bb-<version>.tar.gz
```
---
"""

def test():
    """bb test configuration and connection"""
    return """
### TEST

- If the .alt file is placed in you home directory and bb setup is completed, then

```text
➜ bb test
```

- if all went well, you should get a response like this

```text
➜ bb test
ᐅ Validating connection with 'https://bitbucket.<company>.com'...
✅ OK
```
---
"""


def create():
    """bb create pull-request functionality"""
    return """
### CREATE PULL REQUEST

- Usage

```text
bb create --target master           --> creates pull request and asks for confirmation
bb create --target master --yes    --> creates pull request without prompt
```

- Example:

```text
➜ bb create --target master --yes --diff
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ SUMMARY             ┃ DESCRIPTION                  ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Project             │ repoName                     │
│ Repository          │ bb                           │
│ Repository ID       │ 111111                       │
│ From Branch         │ feature/test                 │
│ To Branch           │ master                       │
│ Title & Description │ test commit                  │
└─────────────────────┴──────────────────────────────┘
ᐅ Contacting https://bitbucket.<company>.com ...
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ✅ PR Created ┃ https://bitbucket.<company>.com/project/name/repos/bb/pull-requests/1                  ┃
└───────────────┴────────────────────────────────────────────────────────────────────────────────────────┘
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ TYPE   ┃ CONTENT          ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ MODIFY │ requirements.txt │
└────────┴──────────────────┘
```
---
"""

def delete():
    """bb delete pull-request functionality"""
    return """
### DELETE PULL REQUEST
- Usage

```text
bb delete --target 1                        --> deletes the given  pull request number with confirmation prompt
bb delete --target 1 --yes                 --> deletes the given  pull request number without prompt
```

- Example

```text
➜ bb delete --target 1 --yes
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ SUMMARY     ┃ DESCRIPTION                                                                            ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ ID          │ 1                                                                                      │
│ Description │ refactor overhaul                                                                      │
│ From Branch │ feature/test                                                                           │
│ To Branch   │ master                                                                                 │
│ Url         │ https://bitbucket.<company>.com/project/name/repos/bb/pull-requests/1                  │
└─────────────┴────────────────────────────────────────────────────────────────────────────────────────┘
ᐅ Contacting https://bitbucket.<company>.com ...
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ✅ PR Deleted ┃ https://bitbucket.<company>.com/project/name/repos/bb/pull-requests/1                  ┃
└───────────────┴────────────────────────────────────────────────────────────────────────────────────────┘
```
---
"""

def diff():
    """bb show diffrence in pull-request functionality"""
    return """
### DIFF
- Show diff of files as an overview. Supported Types,
- Example:
```text
bb create --target master --yes --diff     --> creates pull request without prompt and shows diff from the PR raised
bb delete --target 1 --yes --diff          --> deletes pull request without prompt and shows diff beforw PR is deleted
```
---
"""

def view():
    """bb view authored and reviewer pull-request(s)"""
    return """
### VIEW AUTHORED AND REVIEWER PULL REQUESTS
- View pull requests authored/reviewer for the current repository
- Example:
```text
bb view             --> show pull requests authored[Default]
bb view --author    --> show pull requests authored
bb view --reviewer  --> show pull requests that you are a reviewer
```
---
"""

def autocomplete():
    """bb shell auto-completions"""
    return """
### ENABLE SHELL AUTOCOMPLETIONS
- BB is equipped with shell auto completions, To enable it,
- Example:
```text
bb --install-completion     Install completion for the current shell (One time setup)
bb  --show-completion       Show completion for the current shell, to copy it or customize the installation.
```
---
"""

def default():
    """bb docs default config"""
    return """
- Usage
```text
bb docs --help
```
^ Run the above command for more details
"""

def setup():
    """bb setup instructions"""
    return f"""
{install()}
{alt()}
{autocomplete()}
"""

def wrapper(option: str) -> None:
    md_selector = {
        'autocomplete' : autocomplete(),
        'alt': alt(),
        'create' : create(),
        'delete' : delete(),
        'diff' : diff(),
        'install' : install(),
        'view' : view(),
        'test': test(),
        'default': default(),
        'setup': setup()
    }

    markdown_to_console(md_selector[option])
