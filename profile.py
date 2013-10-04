#!/usr/bin/env python
# encoding: utf-8
# filename: profile.py

import pstats, cProfile

import participant

cProfile.runctx("participant.main()", globals(), locals(), "Profile.prof")

s = pstats.Stats("Profile.prof")
s.strip_dirs().sort_stats("time").print_stats()