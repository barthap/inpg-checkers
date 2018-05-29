import unittest
import utils.config as cfg
import utils.locale as i18n

class LocaleTests(unittest.TestCase):
	def setUp(self):
		cfg.init()

	def test_successfulInit(self):
		self.assertTrue(i18n.locale_exists())
		i18n.init()

	def test_languageDoesNotExist(self):
		setts = cfg.get('GENERAL')
		setts['locale'] = 'bhuva' # bhuva language doesnt exist

		# re init after changing locale
		i18n.init()

		with self.assertRaises(KeyError):
			i18n.get('play')

	def test_keyDoesNotExist(self):
		with self.assertRaises(KeyError):
			i18n.get('key_that_doesnt_exist')

	def test_getKey(self):
		# make sure its English
		setts = cfg.get('GENERAL')
		setts['locale'] = 'english'
		i18n.init()

		self.assertEqual(i18n.get('play'), 'Play')
