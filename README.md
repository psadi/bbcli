# BBCLI

Bitbucket CLI (bbcli): A command line utility that will help you manage pull requests from your terminal.

---

## REQUIREMENTS

* Python3 (3.6.2 or Higher) & Pip3 (latest recommended)
* Write access token from bitbucket

---

### INSTALL

a. Place the .alt file in your home directory

```text
[default]
bitbucket_host=https://bitbucket.mycompany.com
username=myusername
token=thisisarandomwriteaccesstokengeneratedbybitbucket
```

b. clone the git repository

Manual

```text
git clone https://github.com/psadi/bbcli.git
cd bb
pip3 install --user -r requirements.txt
poetry build
pip3 install --user dist/bb-<version>.tar.gz
```

From Releases

* Download the latest build from releases page

```text
pip3 install --user bb-<version>.tar.gz
```

c. Validate

* If the .alt file is placed in you home directory and setup didnt throw any error, then

```text
bb test
```

* if all went well, you should get a response like this

```text
➜ bb test
ᐅ Validating connection with 'https://bitbucket.<company>.com'...
✅ OK
```

### WHAT CAN IT DO?

* Create pull requests

```text
bb create --target master           --> creates pull request and asks for confirmation
bb create --target master --yes    --> creates pull request without prompt
```

* Show diff of files (ADD/DELETE/MODIFY & RENAME) as an overview

```text
bb create --target master --yes --diff     --> creates pull request without prompt and shows diff from the PR raised
bb delete --target 1 --yes --diff          --> deletes pull request without prompt and shows diff befoew PR is deleted
```

* Delete pull requests

```text
bb delete --target 1                        --> deletes the given  pull request number with confirmation prompt
bb delete --target 1 --yes                 --> deletes the given  pull request number without prompt
```

* View pull requests authored/reviewer for the current repository

```text
bb view             --> show pull requests authored[Default]
bb view --author    --> show pull requests authored
bb view --reviewer  --> show pull requests that you are a reviewer
```

### Enable shell autocompletions

* BB is equipped with shell auto completions, To enable it,

```text
bb --install-completion     Install completion for the current shell (One time setup)
bb  --show-completion       Show completion for the current shell, to copy it or customize the installation.
```

---

### Points to Ponder

* This utility is tested with bitbucket enterprise version 6.10.10
* I have personally tested it in Linux, Windows(Powershell and Command Prompt), MacOS and GIT Bash and it works flawlessly
* In case if your ID gets locked the token wont work, you may need to reset your ID (Token can remain the same)
* At times if there are frequent account lockouts, Bitbucket will prompt you to enter CAPTCHA, you may need to relogin with CAPTCHA validation in your broswer once else connection will fail

---

### 💡 PRO TIP 💡

* Use [Windows Terminal](https://github.com/microsoft/terminal) for better visual rendering
* Use Nerd font for better font/icon support, I personally use [DroidSansMono Nerd Font](https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/DroidSansMono.zip)
  * [Preview Font](https://www.programmingfonts.org/#droid-sans)

---

🕺🕺 That's all folks !!

🕺🕺 Enjoy being more efficient 😊
