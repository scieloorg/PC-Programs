# coding = utf-8
from ... import _
from ...generics.reports import validation_status
from ...generics.reports import html_reports


class ORCIDValidator:

    def __init__(self, ws_requester):
        self.ORCID_MAIN_URL = 'https://orcid.org/'
        self._is_available_orcid_website = None
        self.ws_requester = ws_requester

    @property
    def is_available_orcid_website(self):
        if not self.ws_requester:
            return False
        if self._is_available_orcid_website is None:
            self._is_available_orcid_website = self.ws_requester.is_valid_url(
                self.ORCID_MAIN_URL)
        return self._is_available_orcid_website

    def validate_contrib_names(self, contrib_names):
        with_orcid = {}
        msgs = []
        for contrib_name in contrib_names:
            orcid = contrib_name.contrib_id.get('orcid')
            if orcid is None:
                continue
            error_msg = self._is_duplicated(with_orcid, orcid, contrib_name)
            if error_msg:
                msgs.append(error_msg)
            else:
                error_msg = self._is_valid_orcid(orcid, contrib_name)
                if error_msg:
                    msgs.append(error_msg)

        if len(with_orcid) == 0:
            error_msg = (
                'contrib-id',
                validation_status.STATUS_FATAL_ERROR,
                _("It is required at least one {label}. ".format(
                    label="orcid"))
            )
            msgs.append(error_msg)
        return msgs

    def _is_duplicated(self, with_orcid, orcid, contrib_name):
        contrib = with_orcid.get(orcid)
        if not contrib:
            with_orcid[orcid] = contrib_name.fullname
        if contrib and contrib != contrib_name.fullname:
            return (
                'contrib-id',
                validation_status.STATUS_BLOCKING_ERROR,
                _('"{}" and "{}"" can not have the same ORCID: {}').format(
                   contrib_name.fullname, contrib, orcid
                )
            )

    def _is_valid_orcid(self, orcid, contrib_name):
        contrib_orcid_url = '{}{}'.format(self.ORCID_MAIN_URL, orcid)
        if self.is_available_orcid_website:
            if not self.ws_requester.is_valid_url(contrib_orcid_url):
                return (
                    'contrib-id',
                    validation_status.STATUS_FATAL_ERROR,
                    _('{value} is an invalid value for {label}. ').format(
                        value=orcid, label='ORCID'))
        return ('contrib-id',
                validation_status.STATUS_WARNING,
                _('Unable to check if {} belongs to {}. ').format(
                    html_reports.link(contrib_orcid_url, orcid),
                    contrib_name.fullname))
