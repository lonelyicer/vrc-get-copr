# SPDX-License-Identifier: MPL-2.0
#
# Convenience targets for the vrc-get COPR packaging repository.
#
# The package builds are triggered with COPR's buildscm feature, which clones
# this Git repository and runs .copr/Makefile (make_srpm).  No compilation is
# performed locally.

SHELL := /bin/bash

COPR ?= ringlo/vrc-get
CLONE_URL ?= $(shell git remote get-url origin 2>/dev/null)
COMMIT ?= main

CLI_SPEC := vrc-get-cli.spec
GUI_SPEC := vrc-get-gui.spec
SPECS := $(CLI_SPEC) $(GUI_SPEC)

.PHONY: help check versions buildscm buildscm-cli buildscm-gui require-clone-url clean

help: ## Show this help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make <target>\n\nTargets:\n"} /^[a-zA-Z0-9_-]+:.*##/ {printf "  %-14s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

check: ## Validate the spec files and the .copr Makefile
	@for spec in $(SPECS); do \
		echo "==> $$spec"; \
		rpmspec -P "$$spec" >/dev/null || exit 1; \
	done
	@make -n -f .copr/Makefile srpm spec=$(abspath $(CLI_SPEC)) outdir=/tmp >/dev/null
	@echo "spec files and .copr/Makefile look OK"

versions: ## Show packaged versions and the latest upstream tags
	@printf '%-12s %s\n' 'vrc-get-cli' "$$(rpmspec -q --srpm --qf '%{VERSION}' $(CLI_SPEC))"
	@printf '%-12s %s\n' 'vrc-get-gui' "$$(rpmspec -q --srpm --qf '%{VERSION}' $(GUI_SPEC))"
	@echo
	@echo "Latest vrc-get CLI tags:"
	@git ls-remote --tags --refs https://github.com/vrc-get/vrc-get.git \
		| awk -F/ '{print $$3}' \
		| grep -E '^v[0-9]' \
		| sort -V \
		| tail -3
	@echo
	@echo "Latest ALCOM tags:"
	@git ls-remote --tags --refs https://github.com/vrc-get/vrc-get.git \
		| awk -F/ '{print $$3}' \
		| grep -E '^gui-v[0-9]' \
		| sort -V \
		| tail -3

require-clone-url:
	@test -n "$(CLONE_URL)" || { echo "CLONE_URL is empty; set origin or pass CLONE_URL=..."; exit 1; }

buildscm-cli: require-clone-url ## Build vrc-get-cli in COPR from the Git repository
	copr-cli buildscm $(COPR) \
		--clone-url $(CLONE_URL) \
		--commit $(COMMIT) \
		--subdir . \
		--spec $(CLI_SPEC) \
		--type git \
		--method make_srpm

buildscm-gui: require-clone-url ## Build vrc-get-gui (ALCOM) in COPR from the Git repository
	copr-cli buildscm $(COPR) \
		--clone-url $(CLONE_URL) \
		--commit $(COMMIT) \
		--subdir . \
		--spec $(GUI_SPEC) \
		--type git \
		--method make_srpm

buildscm: buildscm-cli buildscm-gui ## Build both packages in COPR from Git

clean: ## Remove downloaded sources and locally generated SRPMs
	rm -f ./*.tar.gz ./*.src.rpm
