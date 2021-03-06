from ceph_medic.checks import common
from ceph_medic import metadata


class TestGetFsid(object):

    def setup(self):
        metadata['cluster_name'] = 'ceph'

    def teardown(self):
        metadata.pop('cluster_name')

    def make_metadata(self, contents=None):
        contents = contents or ''
        data = {'paths': {'/etc/ceph':{'files':{'/etc/ceph/ceph.conf':{'contents': contents}}}}}
        data['cluster_name'] = 'ceph'
        return data

    def test_fails_to_find_an_fsid(self):
        data = self.make_metadata("[global]\nkey=value\n\n[mdss]\ndisabled=true\n")
        fsid = common.get_fsid(data)
        assert fsid == ''

    def test_empty_conf_returns_empty_string(self):
        data = self.make_metadata()
        fsid = common.get_fsid(data)
        assert fsid == ''

    def test_find_an_actual_fsid(self):
        data = self.make_metadata("[global]\nfsid = 1234-lkjh\n\n[mdss]\ndisabled=true\n")
        fsid = common.get_fsid(data)
        assert fsid == '1234-lkjh'

    def test_spaces_on_fsid_are_trimmed(self):
        data = self.make_metadata("[global]\nfsid = 1234-lkjh   \n\n[mdss]\ndisabled=true\n")
        fsid = common.get_fsid(data)
        assert fsid == '1234-lkjh'
