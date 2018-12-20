#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
通过VT_setting.json加载全局配置
"""

from .vtFunction import loadJsonSetting

settingFileName = "VT_setting.json"
globalSetting = loadJsonSetting(settingFileName)