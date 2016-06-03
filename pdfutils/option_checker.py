#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import copy
from optparse import Option, OptionValueError


def alpha_checker(option, opt, value):
	if value >= 0.0 and value <= 1.0:
		return value
	else:
		raise OptionValueError(
			"option %s: value %s out of range (0.0 - 1.0)." %(opt, value))


class SpecializeOption(Option):
	specials = ("alpha",)
	checkers = {"alpha": alpha_checker}

	TYPES = Option.TYPES + specials
	TYPE_CHECKER = copy(Option.TYPE_CHECKER)
	for key in checkers:
		TYPE_CHECKER[key] = checkers[key] 