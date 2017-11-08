# # coding=utf-8
# import platform
# import locale
# import logging
# import hashlib
#
# from .home import *
# from .device import *
# from .auth import *
# from .group import *
# from .securityEvent import *
#
# import requests
#
#
#
#
#
#
# def set_auth_token(token):
#     global auth_token
#     auth_token = token
#
#
# def get_auth_token():
#     global auth_token
#     return auth_token
#
# def get_clientauth_token():
#     global clientauth_token
#     return clientauth_token
#
#
# def get_clientCharacteristics():
#     return clientCharacteristics
#
#
#
#
# def get_urlREST():
#     return urlREST
#
#
# def get_urlWebSocket():
#     return urlWebSocket
#
# #adding a new "trace" log level
# TRACE_LEVEL_NUM = 5
# logging.addLevelName(TRACE_LEVEL_NUM, "TRACE")
# def trace(self, message, *args, **kws):
#     # Yes, logger takes its '*args' as 'args'.
#     if self.isEnabledFor(TRACE_LEVEL_NUM):
#         self._log(TRACE_LEVEL_NUM, message, args, **kws)
# logging.Logger.trace = trace