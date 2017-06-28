# coding=utf-8

from config import app_texts
from config import config
from ws import ws_requester
from ws import institutions_service


_ = app_texts.get_texts('../locale')
configuration = config.Configuration(configuration_filename)
app_ws_requester = ws_requester.WebServicesRequester(configuration.is_web_access_enabled, configuration.proxy_info)
institutions_manager = institutions_service.InstitutionsManager()
