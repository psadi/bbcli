<p align="center"><img height="200" width="200" src="./img/bitbucket.png">

# <p align="center">Bitbucket CLI (bb): A command line utility to manage pull requests from your terminal


## REQUIREMENTS

* Git
* Python3 (3.7 or Higher)
* Pip3 (latest recommended)
* Write access token from bitbucket

---

### INSTALL

Manual

```text
git clone https://github.com/psadi/bbcli.git
cd bb
python3 -m build .
pip3 install --user dist/bb-<version>.tar.gz
```

From Releases

* Download the latest build from releases page

```text
pip3 install --user bb-<version>.tar.gz
```

a. Place the .alt file in your home directory, [refer](.alt) for more details

```text
[default]
bitbucket_host=https://bitbucket.mycompany.com
username=myusername
token=thisisarandomwriteaccesstokengeneratedbybitbucket
```

c. Validate

* If the .alt file is placed in you home directory and setup didnt throw any error, then

```text
bb test
```

* if all went well, you should get a response like this

```text
➜ bb test
> bb test           
⠏ Validating connection with 'https://bitbucket.<company>.com'... OK
```

### WHAT CAN IT DO?

#### Create pull request

|Command|Action|
|-|-|
|`bb create --target master`|creates pull request and asks for confirmation|
|`bb create --target master --yes`|creates pull request without prompt|

#### Show diff of files (ADD/DELETE/MODIFY & RENAME) as an overview

|Command|Action|
|-|-|
|`bb create --target master --yes --diff`|creates pull request without prompt and shows diff from the PR raised|
|`bb delete --id 1 --yes --diff`|deletes pull request without prompt and shows diff befoew PR is deleted|
|`bb diff --id 1`|shows diff for the given pull request id|

#### Delete pull request(s)

|Command|Action|
|-|-|
|`bb delete --id 1`|deletes the given  pull request number with confirmation prompt|
|`bb delete --id 1 --yes`|deletes the given  pull request number without prompt|
|`bb delete --id 1,2,3`|deletes multiple pull requests|

#### Show pull request(s) authored/reviewer

|Command|Action|
|-|-|
|`bb show`|show pull requests in current repository [Default]|
|`bb show --author`|show pull requests authored in current repository|
|`bb show --author --all`|show pull requests authored in all repositories|
|`bb show --reviewer`|show pull requests that you are a reviewer in current repository|
|`bb show --reviewer --all`|show pull requests that you are a reviewer in all repositories|

#### Review pull request

|Command|Action|
|-|-|
|`bb review --id 1 --action approve`|marks the pull request as <span style="background-color:#00875a;color:white">**APPROVED**</span>|
|`bb review --id 1 --action unapprove`|marks the pull request as <span style="background-color:#de350b;color:white">**UNAPPROVED**</span>|
|`bb review --id 1 --action needs_work`|marks the pull request as <span style="background-color:#ffab00;color:white">**NEEDS WORK**</span>|

#### Merge pull request

|Command|Action|
|-|-|
|`bb merge --id 1`|Validates pull request merge conditions and prompts for merge|
|`bb merge --id 1 --rebase`|adds optional rebase [Default: False]|
|`bb merge --id 1 --delete-source-branch`|deletes source branch after merge, [Default: False], If false will prompt for deletion|

### Enable shell autocompletions

* bb is equipped with shell auto completions, To enable it,

|Command|Action|
|-|-|
|`bb --install-completion`|Install completion for the current shell (One time setup)|
|`bb  --show-completion`|Show completion for the current shell, to copy it or customize the installation.|

---

### Points to Ponder

* This utility is tested with bitbucket enterprise version 6.10.10
* I have personally tested it in Linux, Windows(Powershell and Command Prompt), MacOS and GIT Bash and it works flawlessly
* In case if your ID gets locked the token wont work, you may need to reset your ID (Token can remain the same)
* At times if there are frequent account lockouts, Bitbucket will prompt you to enter CAPTCHA, you may need to relogin with CAPTCHA validation in your broswer once else connection will fail

---

### 💡💡 PRO TIP 💡💡

* Use [Windows Terminal](https://github.com/Microsoft/Terminal) for better visual rendering
* Use Nerd font for better font/icon support, I personally use [DroidSansMono Nerd Font](https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/DroidSansMono.zip)
  * [Preview Font](https://www.programmingfonts.org/#droid-sans)

---

### CREDITS

[bbcli](https://github.com/psadi/bbcli) wouldn't be possible if not for the open-source tools made avaiable.

A huge thanks to,

* [tiangolo/typer](https://github.com/tiangolo/typer)
* [Textualize/rich](https://github.com/Textualize/rich)
* [encode/httpx](https://github.com/encode/httpx)


---

<p align="left"><img height="150" width="200" src="./img/thatsall.gif">

Enjoy being more efficient 😊