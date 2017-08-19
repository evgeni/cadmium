import os
import imp
import unittest
try:
    from unittest import mock
except ImportError:
    import mock


cadmium = imp.load_source('cadmium', 'cadmium')


class CadmiumTestCase(unittest.TestCase):

    @mock.patch.dict('os.environ', {})
    def test_get_xdg_config_home_none(self):
        config_home = cadmium.get_xdg_config_home()

        self.assertEqual(config_home, '~/.config/')

    @mock.patch.dict('os.environ', {'XDG_CONFIG_HOME': '/cadmium/config'})
    def test_get_xdg_config_home_defined(self):
        config_home = cadmium.get_xdg_config_home()

        self.assertEqual(config_home, '/cadmium/config')

    @mock.patch('glob.glob', return_value = ['/cadmium/config/chromium/System Profile/Preferences'])
    def test_find_chrome_profiles_none(self, glob):
        profiles = cadmium.find_chrome_profiles('/cadmium/config/chromium')

        self.assertEqual(profiles, {})

    @mock.patch('glob.glob', return_value = ['/cadmium/config/chromium/My Profile/Preferences'])
    @mock.patch('cadmium.open', mock.mock_open(read_data='{"profile":{"name":"My"}}'))
    def test_find_chrome_profiles_my(self, glob):
        profiles = cadmium.find_chrome_profiles('/cadmium/config/chromium')

        self.assertEqual(profiles, {'My': 'My Profile'})

    def test_find_chrome_chrome(self):
        self._test_find_chrome('google-chrome')

    def test_find_chrome_chromium(self):
        self._test_find_chrome('chromium')

    @mock.patch.dict('os.environ', {'XDG_CONFIG_HOME': '/cadmium/config'})
    @mock.patch('distutils.spawn.find_executable')
    def _test_find_chrome(self, name, find_exec):
        def find_executable(executable):
            if executable == name:
                return os.path.join('/cadmium/bin/', name)
        find_exec.side_effect = find_executable

        (chrome, config_path) = cadmium.find_chrome()

        self.assertEqual(chrome, os.path.join('/cadmium/bin/', name))
        self.assertEqual(config_path, os.path.join('/cadmium/config/', name))


if __name__ == '__main__':
    unittest.main()
