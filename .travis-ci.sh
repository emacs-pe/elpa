#!/usr/bin/env bash

sudo add-apt-repository -y ppa:cassou/emacs
sudo apt-get update -qq
sudo apt-get install -qq curl exim4 m4
sudo apt-get install -qq bzr cvs darcs fossil git mercurial subversion
sudo apt-get install -qq emacs24 emacs24-el emacs24-common-non-dfsg
wget -O - https://github.com/milkypostman/melpa/archive/master.tar.gz | tar xz
find melpa-master/recipes -type f -execdir mv {} {}.rcp \;
mkdir -p "${PKGDIR}"
make PKGDIR="${PKGDIR}" STABLE="${STABLE}" clean-packages
make PKGDIR="${PKGDIR}" STABLE="${STABLE}" RCPDIR="melpa-master/recipes" -j6 pkgs
make PKGDIR="${PKGDIR}" STABLE="${STABLE}" archive-contents
