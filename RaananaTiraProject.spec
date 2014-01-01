%{!?python_ver: %global python_ver %(%{__python} -c "import sys ; print sys.version[:3]")}
%global __provides_exclude_from ^%{python_sitearch}/.*\\.so$
%global libname RaananaTiraProject

Name: %{libname}
Version: 1.0
Release: 1
Summary: Game for grown up kids

Group:	 Game
License: GPLv2+
URL:	 https://github.com/emesika/RaananaTiraProject
Source0: https://pypi.python.org/packages/source/R/RaananaTiraProject/RaananaTiraProject-1.0.tar.gz


BuildRequires: python2-devel
Requires: pygame
Requires: python-twisted

%description
Game for the grown up

%prep
%setup -q -n %{libname}-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install --root $RPM_BUILD_ROOT

%files
%doc AUTHORS COPYING README
%dir /usr/lib/python2.7/site-packages/server
%dir /usr/lib/python2.7/site-packages/client
%dir /usr/lib/python2.7/site-packages/components
%attr(755, root, root) /usr/bin/start_server
%attr(755, root, root) /usr/bin/start_client
/usr/lib/python2.7/site-packages/server/main.py*
/usr/lib/python2.7/site-packages/server/game.py*
/usr/lib/python2.7/site-packages/server/gameServer.py*
/usr/lib/python2.7/site-packages/client/config.py*
/usr/lib/python2.7/site-packages/client/game.py*
/usr/lib/python2.7/site-packages/client/__init__.py*
/usr/lib/python2.7/site-packages/client/main.py*
/usr/lib/python2.7/site-packages/components/car.py*
/usr/lib/python2.7/site-packages/components/component.py*
/usr/lib/python2.7/site-packages/components/__init__.py*
/usr/lib/python2.7/site-packages/components/matrix_config.py*
/usr/lib/python2.7/site-packages/components/matrix.py*
/usr/lib/python2.7/site-packages/components/message.py*
/usr/lib/python2.7/site-packages/%{libname}-%{version}-py*.egg-info

%changelog
* Tue Dec 31 2013 Yaniv Bronhaim <ybronhei@redhat.com> - 1.0
- Creating spec for setup
