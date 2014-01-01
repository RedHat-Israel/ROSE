VERSION=1.0
NAME=RaananaTiraProject
TAR_FILE=${NAME}-${VERSION}.tar.gz

SOURCEDIR=${HOME}/rpmbuild/SOURCES
SPECFILE=${NAME}.spec

DIST=dist

TAR_DIST_LOCATION=${DIST}/${TAR_FILE}
TAR_RPM_LOCATION=${SOURCEDIR}/${TAR_FILE}

all: ${TAR_DIST_LOCATION}

.PHONY: build rpm srpm ${TAR_DIST_LOCATION}

build:
	python setup.py build

$(TAR_DIST_LOCATION):
	mkdir -p dist
	python setup.py sdist

${TAR_RPM_LOCATION}: ${TAR_DIST_LOCATION}
	cp "$<" "$@"

srpm: ${SPECFILE} $(TAR_RPM_LOCATION)
	rpmbuild -bs ${SPECFILE}

rpm: ${SPECFILE} ${TAR_RPM_LOCATION}
	rpmbuild -ba ${SPECFILE}

clean:
	python setup.py clean
	rm -rf ${DIST}
	rm -rf build
