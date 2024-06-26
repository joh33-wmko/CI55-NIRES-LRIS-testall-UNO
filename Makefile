################################################################################
#+
#  Module:	$KROOT/src/kss/nires/testall
#
#  Author:	JMader
#
#  Date:	2020-05-28
#
#  Description:	Makefile for $KROOT/src/kss/nires/testall
#
#  Revisions:
#-
################################################################################

#  If this is a release point, define version macros to override values
#  inherited from the environment.

override SYSNAM = kss/nires/testall
override VERNUM = 0-0-0

# Directories to make

DIRS = data

# File to release

RELBIN  = testall_check.csh
RELBIN += testall_check.py

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
