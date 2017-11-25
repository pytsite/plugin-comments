"""
"""
from pytsite import testing, http_api, util
from plugins import auth, comments

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class HttpApiTest(testing.TestCase):
    def setUp(self):
        user_role = auth.get_role('user')
        user_role.add_permission('odm_auth.create.comment')
        user_role.add_permission('odm_auth.modify.comment')
        user_role.save()

        self.create_url = http_api.url('comments@post_comment')
        self.get_list_url = http_api.url('comments@get_comments')

        self.token = auth.generate_access_token(auth.get_user('user1@test.com'))
        self.headers = {'PytSite-Auth': self.token}

    def post_comment(self, driver: str, thread_uid: str, body: str = 'Hello World', parent_uid: str = None):
        args = {
            'driver': driver,
            'thread_uid': thread_uid,
            'body': body,
        }

        if parent_uid:
            args['parent_uid'] = parent_uid

        resp = self.send_http_request(self.prepare_http_request('POST', self.create_url, self.headers, args))

        # Some drivers may not implement comment creation via HTTP API
        if resp.status_code == 500 and resp.json().get('error').find('Not implemented') >= 0:
            raise NotImplementedError()

        self.assertHttpRespCodeEquals(resp, 200)
        self.assertHttpRespJsonFieldIsNonEmptyStr(resp, 'uid')
        self.assertHttpRespJsonFieldEquals(resp, 'thread_uid', thread_uid)
        self.assertHttpRespJsonFieldIsNonEmptyStr(resp, 'status')
        self.assertHttpRespJsonFieldEquals(resp, 'body', body)
        self.assertHttpRespJsonFieldIsNonEmptyDict(resp, 'author')
        self.assertHttpRespJsonFieldIsNonEmptyDict(resp, 'publish_time')
        self.assertHttpRespJsonFieldIsNonEmptyDict(resp, 'permissions')

        return resp

    def test_get_settings(self):
        token = auth.generate_access_token(auth.get_user('user1@test.com'))
        url = http_api.url('comments@get_settings')

        for driver in comments.get_drivers().values():
            resp = self.send_http_request(self.prepare_http_request('GET', url, {'PytSite-Auth': token}, {
                'driver': driver.get_name(),
            }))

            self.assertHttpRespCodeEquals(resp, 200)
            self.assertHttpRespJsonFieldIsInt(resp, 'max_depth')
            self.assertHttpRespJsonFieldIsInt(resp, 'body_min_length')
            self.assertHttpRespJsonFieldIsInt(resp, 'body_max_length')
            self.assertHttpRespJsonFieldIsDict(resp, 'statuses')
            self.assertHttpRespJsonFieldNotEmpty(resp, 'statuses')
            self.assertHttpRespJsonFieldIsDict(resp, 'permissions')
            self.assertHttpRespJsonFieldNotEmpty(resp, 'permissions')

    def test_post_comment(self):
        thread_uid = util.random_str()

        for driver in comments.get_drivers().values():
            try:
                resp = self.post_comment(driver.get_name(), thread_uid)
                self.assertHttpRespJsonFieldIsEmpty(resp, 'parent_uid')
                self.assertHttpRespJsonFieldEquals(resp, 'depth', 0)

            except NotImplementedError:
                pass

    def test_post_reply(self):
        thread_uid = util.random_str()

        for driver in comments.get_drivers().values():
            try:
                # Create 1st comment
                resp = self.post_comment(driver.get_name(), thread_uid)

                # Create 2nd comment
                parent_uid = resp.json()['uid']
                resp = self.post_comment(driver.get_name(), thread_uid, 'Hello Another World', parent_uid)

                # Check 2nd comment creation result
                self.assertHttpRespJsonFieldEquals(resp, 'parent_uid', parent_uid)
                self.assertHttpRespJsonFieldEquals(resp, 'depth', 1)

            except NotImplementedError:
                pass

    def test_get_comment(self):
        thread_uid = util.random_str()
        for driver in comments.get_drivers().values():
            try:
                resp = self.post_comment(driver.get_name(), thread_uid)

                self.get_url = http_api.url('comments@get_comment', {'uid': resp.json()['uid']})
                resp = self.send_http_request(self.prepare_http_request('GET', self.get_url, self.headers, {
                    'driver': driver.get_name(),
                    'thread_uid': thread_uid,
                }))
                self.assertHttpRespCodeEquals(resp, 200)

            except NotImplementedError:
                pass

    def test_get_comments(self):
        thread_uid = util.random_str()

        for driver in comments.get_drivers().values():
            try:
                for i in range(0, 2):
                    self.post_comment(driver.get_name(), thread_uid, 'Hello {}'.format(i))

                req = self.prepare_http_request('GET', self.get_list_url, self.headers, {
                    'driver': driver.get_name(),
                    'thread_uid': thread_uid,
                })
                resp = self.send_http_request(req)

                # Check list of comments
                self.assertHttpRespCodeEquals(resp, 200)
                self.assertHttpRespJsonFieldListLen(resp, 'items', 2)

            except NotImplementedError:
                pass

    def test_delete_comment(self):
        thread_uid = util.random_str()
        for driver in comments.get_drivers().values():
            try:
                resp = self.post_comment(driver.get_name(), thread_uid)
                self.report_url = http_api.url('comments@delete_comment', {'uid': resp.json()['uid']})
                resp = self.send_http_request(self.prepare_http_request('DELETE', self.report_url, self.headers, {
                    'driver': driver.get_name(),
                }))

                # Check response
                self.assertHttpRespCodeEquals(resp, 200)
                self.assertHttpRespJsonFieldEquals(resp, 'status', True)

            except NotImplementedError:
                pass

    def test_post_report(self):
        thread_uid = util.random_str()
        for driver in comments.get_drivers().values():
            try:
                resp = self.post_comment(driver.get_name(), thread_uid)
                self.report_url = http_api.url('comments@post_comment_report', {'uid': resp.json()['uid']})
                resp = self.send_http_request(self.prepare_http_request('POST', self.report_url, self.headers, {
                    'driver': driver.get_name(),
                }))

                # Check response
                self.assertHttpRespCodeEquals(resp, 200)
                self.assertHttpRespJsonFieldEquals(resp, 'status', True)

            except NotImplementedError:
                pass
