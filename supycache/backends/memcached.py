#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pylibmc
from .base import BaseCache


class MemcachedCache(pylibmc.Client, BaseCache):

    clear = pylibmc.Client.flush_all
