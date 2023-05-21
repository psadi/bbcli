<div id="texts" style="white-space:nowrap;">
     <img height="100" width="100" src="./resources/bb.png"  align="left"/>
     <h1>Bitbucket-CLI (bb) </h1>
     <h3>Work seamlessly with Bitbucket from the command line</h3>
     </br>
</div>

![](https://img.shields.io/badge/license-MIT-green.svg?style=flat)
[![Continuous Integration](https://github.com/psadi/bbcli/actions/workflows/ci.yml/badge.svg)](https://github.com/psadi/bbcli/actions/workflows/ci.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=psadi_bbcli&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=psadi_bbcli)



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
docker run -it -v $HOME/.config/bb:$HOME/.config/bb -v $(pwd):/app/. --network host psadi/bbcli [OPTIONS] COMMAND [ARGS]
```

Example:
```sh
docker run -it -v $HOME/.config/bb:$HOME/.config/bb -v $(pwd):/app/. --network host psadi/bbcli pr create --target master
```

---

###  CONFIGURATION

1. Run the following command to perform initial setup, this will setup a `config.ini` under `$XDG_CONFIG_HOME/bb` respective to the OS

```sh
bb auth setup
```

2. Validate

* Check the config file status `bb auth status`

* If the config file is setup properly, run `bb auth test` to validate

* if all went well, you should get a response like this

```sh
> bb auth test
⠏ Validating connection with 'https://bitbucket.<company>.com'... OK
```
---

###  HOW-TO?

<details>
  <summary>Create pull request</summary>

|Command|Action|
|-|-|
|`bb pr create --target master`|creates pull request and asks for confirmation|
|`bb pr create --target master --yes`|creates pull request without prompt|

</details>


<details>
  <summary>Show diff of files (ADD/DELETE/MODIFY & RENAME) as an overview</summary>

|Command|Action|
|-|-|
|`bb pr create --target master --yes --diff`|creates pull request without prompt and shows diff from the PR raised|
|`bb pr delete --id 1 --yes --diff`|deletes pull request without prompt and shows diff befoew PR is deleted|
|`bb pr diff --id 1`|shows diff for the given pull request id|


</details>

<details>
  <summary>Delete pull request(s)</summary>

|Command|Action|
|-|-|
|`bb pr delete --id 1`|deletes the given  pull request number with confirmation prompt|
|`bb pr delete --id 1 --yes`|deletes the given  pull request number without prompt|
|`bb pr delete --id 1,2,3`|deletes multiple pull requests|

</details>

<details>
  <summary>Show pull request(s) authored/reviewer</summary>

|Command|Action|
|-|-|
|`bb pr list`|show pull requests in current repository [Default]|
|`bb pr list --author`|show pull requests authored in current repository|
|`bb pr list --author --all`|show pull requests authored in all repositories|
|`bb pr list --reviewer`|show pull requests that you are a reviewer in current repository|
|`bb pr list --reviewer --all`|show pull requests that you are a reviewer in all repositories|

</details>

<details>
  <summary>Review pull request</summary>

|Command|Action|
|-|-|
|`bb pr review --id 1 --action approve`|marks the pull request as <span style="background-color:#00875a;color:white">**APPROVED**</span>|
|`bb pr review --id 1 --action unapprove`|marks the pull request as <span style="background-color:#de350b;color:white">**UNAPPROVED**</span>|
|`bb pr review --id 1 --action needs_work`|marks the pull request as <span style="background-color:#ffab00;color:white">**NEEDS WORK**</span>|

</details>


<details>
  <summary>Merge pull request</summary>

|Command|Action|
|-|-|
|`bb pr merge --id 1`|Validates pull request merge conditions and prompts for merge|
|`bb pr merge --id 1 --rebase`|adds optional rebase [Default: False]|
|`bb pr merge --id 1 --delete-source-branch`|deletes source branch after merge, [Default: False], If false will prompt for deletion|

</details>

---

###  Points to Ponder

* This utility is tested with bitbucket enterprise version 6.10.10
* I have personally tested it in Linux, Windows(Powershell and Command Prompt), MacOS and GIT Bash and it works flawlessly
* In case if your ID gets locked the token wont work, you may need to reset your ID (Token can remain the same)
* At times if there are frequent account lockouts, Bitbucket will prompt you to enter CAPTCHA, you may need to relogin with CAPTCHA validation in your broswer once else connection will fail

---

###  CREDITS

[bbcli](https://github.com/psadi/bbcli) wouldn't be possible if not for the awesome open-source tools made avaiable.

A huge thanks to,

* [tiangolo/typer](https://github.com/tiangolo/typer)
* [Textualize/rich](https://github.com/Textualize/rich)


---

<p align="left"><img height="150" width="200" src="./resources/thatsall.gif">

Enjoy being more efficient 😊
