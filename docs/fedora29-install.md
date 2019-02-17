# Fedora 29 and up setup

Since Fedora 29, Python2 is not install by default.
For now, the following steps are required:

```bash
sudo dnf install git python2 gcc redhat-rpm-config python2-devel -y
pip3 install --user pipenv
cd
git clone https://github.com/RedHat-Israel/ROSE.git
cd ./ROSE
pipenv install

```
