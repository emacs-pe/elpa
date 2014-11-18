PKGDIR  := $(CURDIR)/packages
RCPDIR  := $(CURDIR)/recipes
WORKDIR := $(CURDIR)/working

ELS      = package-build.el
ELCS     = $(ELS:.el=.elc)

EMACS   ?= emacs
BATCH    = $(EMACS) --batch -Q -L . --load $(ELS)

TIMEOUT := $(shell which timeout && echo "-k 60 600")

all: $(ELCS) archive-contents pkgs

%.elc: %.el
	$(BATCH) -f batch-byte-compile $<

clean-working:
	$(RM) -r $(WORKDIR)/*

clean-packages:
	$(RM) -r $(PKGDIR)/*

.PHONY: clean
clean: clean-working clean-packages

archive-contents:
	$(BATCH) -f package-build-dump-archive-contents-cmd $(PKGDIR)/archive-contents

pkgs: $(wildcard $(RCPDIR)/*.rcp)

%.rcp: .FORCE
	$(info • Building recipe $@ ...)
	-$(TIMEOUT) $(BATCH) -f package-build-recipe-cmd "$@"

.FORCE:
