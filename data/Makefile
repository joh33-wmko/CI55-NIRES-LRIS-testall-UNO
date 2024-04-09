################################################################################
#+
#  Module:	$KROOT/util/testall/data
#
#  Author:	JMader
#
#  Date:	2020-05-28
#
#  Description:	Makefile for $KROOT/util/testAll/data
#
#  Revisions:
#-
################################################################################

# File to release
# (NOTE: Moving these to instrument dirs)
RELDAT  = testall-kpf.yaml
#RELDAT += testall-esi.yaml
#RELDAT += testall-hires.yaml
#RELDAT += testall-kcwi.yaml
#RELDAT += testall-lris.yaml
#RELDAT += testall-mosfire.yaml
#RELDAT += testall-nirc2.yaml
#RELDAT += testall-nires.yaml
##RELDAT += testall-nirspec.yaml
#RELDAT += testall-osiris.yaml
#RELDAT += testall-pcs1.yaml
#RELDAT += testall-koa.yaml

################################################################################
# KROOT boilerplate:
# Include general make rules, using default values for the key environment
# variables if they are not already set.

ifndef KROOT
        KROOT = /kroot
endif

ifndef RELNAM
        RELNAM = default
endif

ifndef RELDIR
        RELDIR = $(KROOT)/rel/$(RELNAM)
endif

include $(KROOT)/etc/config.mk
