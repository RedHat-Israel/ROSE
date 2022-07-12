# ROSE Project - how to use Github Actions CI

This file is a temporary guide about how to use [Github Actions](https://docs.github.com/en/actions) on the [ROSE Project](https://github.com/RedHat-Israel/ROSE). Parts of it might eventually not be needed, other parts might be incorporated into the main README.md.

Right now, Github Actions is not enabled for ROSE. So to use it, you have to enable it on your own fork:

- If you have not done so yet, login to github.com, go to the  [ROSE Project](https://github.com/RedHat-Israel/ROSE) page, and press "Fork". Follow the instructions to fork it to your own github account.

- Go to the main page of your own fork. This should be something like https://github.com/MyUserName/ROSE.

- Press Actions

- Press "set up a workflow yourself"

- You enter a page allowing you to create a new file under `.github/workflows`.

- Set the filename to `ci.yml`.

- Remove the default contents (e.g. press inside it, Ctrl-A, Backspace)

- Copy there the content of [my own copy](https://raw.githubusercontent.com/didib/ROSE/master/.github/workflows/ci.yml)

- Press "Start commit"

- Optionally change the commit's subject line and body

- Press "Commit new file"

You are done.

To test that this worked:

- Create a new branch

- Create a new Pull Request (PR) for this new branch. When creating the PR, make sure to choose your own fork's master branch as the base, and not RedHat-Israel.

- This should automatically trigger the action. If you didn't change any Python code, it should succeed, in a few minutes. If you created a Python bug, it should fail.
