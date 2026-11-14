# Called by COPR when the source build method is "make_srpm":
#
#   make -f .copr/Makefile srpm outdir=<dir> spec=<spec>
#
# The spec is passed by COPR.  Sources are downloaded by spectool from the
# Source0 URLs in the spec, then rpmbuild creates the SRPM.

spec ?= vrc-get-cli.spec
outdir ?= $(CURDIR)

.PHONY: srpm
srpm:
	dnf -y install rpmdevtools
	spectool -g -C $(dir $(spec)) $(spec)
	rpmbuild -bs $(spec) \
		--define "_sourcedir $(dir $(spec))" \
		--define "_srcrpmdir $(outdir)" \
		--define "_disable_source_fetch 0"
