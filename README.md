<div id="texts" style="white-space:nowrap;">
     <img height="100" width="100" src="./img/bb.png"  align="left"/>
     <h1>bb (bitbucket-cli) </h1>
     <h3>A command line tool to manage your pull requests</h3>
     </br>
</div>

<p><i>be lazy and still get things done</i></p>

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=psadi_bbcli&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=psadi_bbcli)
![](https://img.shields.io/badge/license-MIT-green.svg?style=flat)
<a href="https://www.buymeacoffee.com/addy3494" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 22px !important;width: 100px !important;" ></a>

---

###  REQUIREMENTS

* [Git](https://git-scm.com/downloads)
* [Python3](https://www.python.org/downloads/) (3.7 or Higher)
* [Pip3]( https://pypi.org/project/pip/) (latest recommended)
* A write access token from bitbucket

---

###  INSTALLATION

<b>From Source</b>

```sh
git clone https://github.com/psadi/bbcli.git && cd bb
python3 -m build .
pip3 install --user dist/bb-<version>.tar.gz
```

<b>From Releases</b>

Download the latest build from [releases](https://github.com/psadi/bbcli/releases) page

```sh
pip3 install --user bb-<version>.tar.gz
```

<b>From Docker</b>

A docker image is published to [hub.docker.com](https://hub.docker.com/r/psadi/bbcli)

```sh
docker pull psadi/bbcli:<tag>
docker run -it -v $HOME/.alt:/root/.alt psadi/bbcli:<tag> [OPTIONS] COMMAND [ARGS]
```

Example:
```sh
docker run -it -v $HOME/.alt:/root/.alt psadi/bbcli:<tag> create --target master
```

---

###  CONFIGURATION

1. Place the .alt file in your home directory, [refer](.alt) for more details

```text
[default]
bitbucket_host=https://bitbucket.mycompany.com
username=myusername
token=thisisarandomwriteaccesstokengeneratedbybitbucket
```

2. Validate

* If the .alt file is placed in you home directory and setup didnt throw any error, then

```sh
bb test
```

* if all went well, you should get a response like this

```sh
> bb test
⠏ Validating connection with 'https://bitbucket.<company>.com'... OK
```
---

###  HOW-TO ?

<details>
  <summary>Create pull request</summary>

|Command|Action|
|-|-|
|`bb create --target master`|creates pull request and asks for confirmation|
|`bb create --target master --yes`|creates pull request without prompt|

</details>


<details>
  <summary>Show diff of files (ADD/DELETE/MODIFY & RENAME) as an overview</summary>

|Command|Action|
|-|-|
|`bb create --target master --yes --diff`|creates pull request without prompt and shows diff from the PR raised|
|`bb delete --id 1 --yes --diff`|deletes pull request without prompt and shows diff befoew PR is deleted|
|`bb diff --id 1`|shows diff for the given pull request id|


</details>

<details>
  <summary>Delete pull request(s)</summary>

|Command|Action|
|-|-|
|`bb delete --id 1`|deletes the given  pull request number with confirmation prompt|
|`bb delete --id 1 --yes`|deletes the given  pull request number without prompt|
|`bb delete --id 1,2,3`|deletes multiple pull requests|

</details>

<details>
  <summary>Show pull request(s) authored/reviewer</summary>

|Command|Action|
|-|-|
|`bb show`|show pull requests in current repository [Default]|
|`bb show --author`|show pull requests authored in current repository|
|`bb show --author --all`|show pull requests authored in all repositories|
|`bb show --reviewer`|show pull requests that you are a reviewer in current repository|
|`bb show --reviewer --all`|show pull requests that you are a reviewer in all repositories|

</details>

<details>
  <summary>Review pull request</summary>

|Command|Action|
|-|-|
|`bb review --id 1 --action approve`|marks the pull request as <span style="background-color:#00875a;color:white">**APPROVED**</span>|
|`bb review --id 1 --action unapprove`|marks the pull request as <span style="background-color:#de350b;color:white">**UNAPPROVED**</span>|
|`bb review --id 1 --action needs_work`|marks the pull request as <span style="background-color:#ffab00;color:white">**NEEDS WORK**</span>|

</details>


<details>
  <summary>Merge pull request</summary>

|Command|Action|
|-|-|
|`bb merge --id 1`|Validates pull request merge conditions and prompts for merge|
|`bb merge --id 1 --rebase`|adds optional rebase [Default: False]|
|`bb merge --id 1 --delete-source-branch`|deletes source branch after merge, [Default: False], If false will prompt for deletion|

</details>

<details>
  <summary>Enable shell autocompletions</summary>

* bb is equipped with shell auto completions, To enable it,

|Command|Action|
|-|-|
|`bb --install-completion`|Install completion for the current shell (One time setup)|
|`bb  --show-completion`|Show completion for the current shell, to copy it or customize the installation.|


</details>

---

###  Points to Ponder

* This utility is tested with bitbucket enterprise version 6.10.10
* I have personally tested it in Linux, Windows(Powershell and Command Prompt), MacOS and GIT Bash and it works flawlessly
* In case if your ID gets locked the token wont work, you may need to reset your ID (Token can remain the same)
* At times if there are frequent account lockouts, Bitbucket will prompt you to enter CAPTCHA, you may need to relogin with CAPTCHA validation in your broswer once else connection will fail

---

###  💡 TIP

* You could use [Windows Terminal](https://github.com/Microsoft/Terminal) for better visual rendering
* You could use an Nerd font for better font/icon support, I personally use [DroidSansMono Nerd Font](https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/DroidSansMono.zip)
  * [Preview Font](https://www.programmingfonts.org/#droid-sans)

---

###  CREDITS

[bbcli](https://github.com/psadi/bbcli) wouldn't be possible if not for the awesome open-source tools made avaiable.

A huge thanks to,

* [tiangolo/typer](https://github.com/tiangolo/typer)
* [Textualize/rich](https://github.com/Textualize/rich)


---

<p align="left"><img height="150" width="200" src="./img/thatsall.gif">

Enjoy being more efficient 😊