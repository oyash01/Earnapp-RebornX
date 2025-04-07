import unittest
from unittest.mock import patch, MagicMock
import platform
from utils.detector import detect_os, detect_architecture, is_wsl

class TestDetector(unittest.TestCase):

    @patch('utils.loader.load_json_config')
    @patch('platform.system', return_value='Linux')
    @patch('utils.detector.is_wsl', return_value=True)
    def test_detect_os_wsl(self, mock_is_wsl, mock_platform_system, mock_load_json_config):
        """
        Test detecting WSL environment.
        """
        mock_load_json_config.return_value = {
            "system": {
                "os_map": {
                    "win32nt": "Windows",
                    "windows_nt": "Windows",
                    "windows": "Windows",
                    "linux": "Linux",
                    "wsl": "WSL",
                    "darwin": "MacOS",
                    "macos": "MacOS",
                    "macosx": "MacOS",
                    "mac": "MacOS",
                    "osx": "MacOS",
                    "cygwin": "Cygwin",
                    "mingw": "MinGw",
                    "msys": "Msys",
                    "freebsd": "FreeBSD"
                }
            }
        }

        result = detect_os({"system": {"os_map": {"wsl": "WSL"}}})
        self.assertEqual(result["os_type"], "WSL")
        self.assertTrue(result["is_wsl"])
        mock_platform_system.assert_called_once()
        mock_is_wsl.assert_called_once()

    @patch('utils.loader.load_json_config')
    @patch('platform.system', return_value='Linux')
    @patch('utils.detector.is_wsl', return_value=False)
    def test_detect_os_linux(self, mock_is_wsl, mock_platform_system, mock_load_json_config):
        """
        Test detecting Linux environment.
        """
        mock_load_json_config.return_value = {
            "system": {
                "os_map": {
                    "win32nt": "Windows",
                    "windows_nt": "Windows",
                    "windows": "Windows",
                    "linux": "Linux",
                    "wsl": "WSL",
                    "darwin": "MacOS",
                    "macos": "MacOS",
                    "macosx": "MacOS",
                    "mac": "MacOS",
                    "osx": "MacOS",
                    "cygwin": "Cygwin",
                    "mingw": "MinGw",
                    "msys": "Msys",
                    "freebsd": "FreeBSD"
                }
            }
        }

        result = detect_os({"system": {"os_map": {"linux": "Linux"}}})
        self.assertEqual(result["os_type"], "Linux")
        self.assertFalse(result["is_wsl"])
        mock_platform_system.assert_called_once()
        mock_is_wsl.assert_called_once()

    @patch('builtins.open', new_callable=MagicMock)
    def test_is_wsl(self, mock_open):
        """
        Test WSL detection.
        """
        # Test WSL environment
        mock_open.return_value.__enter__.return_value.read.return_value = "Microsoft"
        self.assertTrue(is_wsl())

        # Test non-WSL environment
        mock_open.return_value.__enter__.return_value.read.return_value = "Linux"
        self.assertFalse(is_wsl())

        # Test file not found
        mock_open.side_effect = FileNotFoundError
        self.assertFalse(is_wsl())

    @patch('utils.loader.load_json_config')
    @patch('platform.system', return_value='Linux')
    def test_detect_os(self, mock_platform_system, mock_load_json_config):
        """
        Test detecting the operating system type.
        """
        mock_load_json_config.return_value = {
            "system": {
                "os_map": {
                    "win32nt": "Windows",
                    "windows_nt": "Windows",
                    "windows": "Windows",
                    "linux": "Linux",
                    "darwin": "MacOS",
                    "macos": "MacOS",
                    "macosx": "MacOS",
                    "mac": "MacOS",
                    "osx": "MacOS",
                    "cygwin": "Cygwin",
                    "mingw": "MinGw",
                    "msys": "Msys",
                    "freebsd": "FreeBSD"
                }
            }
        }

        expected_os_type = "Linux"
        result = detect_os({"system": {"os_map": {"linux": "Linux"}}})
        self.assertEqual(result, {"os_type": expected_os_type})
        mock_platform_system.assert_called_once()

    @patch('utils.loader.load_json_config')
    @patch('platform.machine', return_value='x86_64')
    def test_detect_architecture(self, mock_platform_machine, mock_load_json_config):
        """
        Test detecting the system architecture.
        """
        mock_load_json_config.return_value = {
            "system": {
                "arch_map": {
                    "x86_64": "amd64",
                    "amd64": "amd64",
                    "aarch64": "arm64",
                    "arm64": "arm64"
                }
            }
        }

        expected_arch = "x86_64"
        expected_dkarch = "amd64"
        result = detect_architecture({"system": {"arch_map": {"x86_64": "amd64"}}})
        self.assertEqual(result, {"arch": expected_arch, "dkarch": expected_dkarch})
        mock_platform_machine.assert_called_once()

if __name__ == '__main__':
    unittest.main()
