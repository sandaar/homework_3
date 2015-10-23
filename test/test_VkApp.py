import pytest

from vk_audios import VkApp

mark_vk_tests = pytest.mark.regression


@pytest.fixture(scope="module", autouse=True)
def vk_app():
    return VkApp()


class TestVkapp(object):
    @mark_vk_tests
    def test_get_user_id_from_nickname(self, vk_app, input_data, output_data):
        test_class = 'test_VkApp'
        test_name = 'test_get_user_id_from_nickname'
        input_data = input_data[test_class][test_name]
        output_data = output_data[test_class][test_name]
        user_nickname = input_data['user_nickname']
        actual_user_id = vk_app.get_user_id(user_nickname)
        assert actual_user_id == output_data

    @mark_vk_tests
    def test_get_user_id_from_id(self, vk_app, input_data, output_data):
        test_class = 'test_VkApp'
        test_name = 'test_get_user_id_from_id'
        input_data = input_data[test_class][test_name]
        output_data = output_data[test_class][test_name]
        user_id = input_data['user_id']
        actual_user_id = vk_app.get_user_id(user_id)
        assert actual_user_id == output_data

    @mark_vk_tests
    def test_get_audios(self, vk_app, input_data, output_data):
        test_class = 'test_VkApp'
        test_name = 'test_get_audios'
        input_data = input_data[test_class][test_name]
        output_data = output_data[test_class][test_name]
        user_id = input_data['user_id']
        audios = vk_app.get_audios(user_id)
        assert audios_equal(audios, output_data)

    @mark_vk_tests
    def test_get_audios_list(self, vk_app, input_data, output_data):
        test_class = 'test_VkApp'
        test_name = 'test_get_audios_list'
        input_data = input_data[test_class][test_name]
        output_data = output_data[test_class][test_name]
        user_id = input_data['user_id']
        audios_list = vk_app.get_audios_list(user_id)
        assert audios_lists_equal(audios_list, output_data)

    @mark_vk_tests
    def test_get_audios_count(self, vk_app, input_data, output_data):
        test_class = 'test_VkApp'
        test_name = 'test_get_audios_count'
        input_data = input_data[test_class][test_name]
        output_data = output_data[test_class][test_name]
        user_id = input_data['user_id']
        audios_count = vk_app.get_audios_count(user_id)
        assert audios_counts_equal(audios_count, output_data)

    @mark_vk_tests
    def test_get_friends(self, vk_app, input_data, output_data):
        test_class = 'test_VkApp'
        test_name = 'test_get_friends'
        input_data = input_data[test_class][test_name]
        output_data = output_data[test_class][test_name]
        user_id = input_data['user_id']
        friends = vk_app.get_friends(user_id)
        assert friends == output_data

    @mark_vk_tests
    def test_get_users(self, vk_app, input_data, output_data):
        test_class = 'test_VkApp'
        test_name = 'test_get_users'
        input_data = input_data[test_class][test_name]
        output_data = output_data[test_class][test_name]
        user_id = input_data['user_id']
        users = vk_app.get_users(user_id)
        assert users == output_data


def audios_equal(actual_data, expected_data):
    counts_equal = audios_counts_equal(actual_data[0], expected_data[0])
    audios_equal = audios_lists_equal(actual_data[1:], expected_data[1:])
    return counts_equal and audios_equal


def audios_counts_equal(actual_count, expected_count):
    return actual_count == expected_count


def audios_lists_equal(actual_audios, expected_audios):
    if len(actual_audios) != len(expected_audios):
        return False
    for a in actual_audios:
        del a['url']
    return all([a in expected_audios for a in actual_audios])
