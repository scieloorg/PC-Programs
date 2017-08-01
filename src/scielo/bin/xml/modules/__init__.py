# coding=utf-8

from . import app_texts
from ws import ws_requester
from ws import institutions_service


_ = app_texts.get_texts('../locale')

app_ws_requester = ws_requester.WebServicesRequester()
institutions_manager = institutions_service.InstitutionsManager()
