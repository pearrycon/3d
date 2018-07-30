import unittest
import os
import xml.etree.ElementTree as ET

from programy.brain import Brain
from programy.config.brain.brain import BrainConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.events.console.config import ConsoleConfiguration
from programy.oob.default import DefaultOutOfBandProcessor
from programy.oob.dial import DialOutOfBandProcessor
from programy.oob.email import EmailOutOfBandProcessor

from programytest.client import TestClient

class BrainTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self._client_context = client.create_client_context("testid")

    def load_os_specific_configuration(self, yaml, linux_filename, windows_filename):
        if os.name == 'posix':
            yaml.load_from_file(os.path.dirname(__file__)+ os.sep + "testdata" + os.sep + linux_filename, ConsoleConfiguration(), os.path.dirname(__file__))
        elif os.name == 'nt':
            yaml.load_from_file(os.path.dirname(__file__)+ os.sep + "testdata" + os.sep + windows_filename, ConsoleConfiguration(), os.path.dirname(__file__))
        else:
            raise Exception("Unknown os [%s]"%os.name)

    def test_brain_init_no_config(self):
        client = TestClient()
        client_context = client.create_client_context("testid")

        self.assertIsNotNone(client_context.brain)

        self.assertIsNotNone(client_context.brain.aiml_parser)
        self.assertIsNotNone(client_context.brain.denormals)
        self.assertIsNotNone(client_context.brain.normals)
        self.assertIsNotNone(client_context.brain.genders)
        self.assertIsNotNone(client_context.brain.persons)
        self.assertIsNotNone(client_context.brain.person2s)
        self.assertIsNotNone(client_context.brain.properties)
        self.assertIsNotNone(client_context.brain.rdf)
        self.assertIsNotNone(client_context.brain.sets)
        self.assertIsNotNone(client_context.brain.maps)
        self.assertIsNotNone(client_context.brain.preprocessors)
        self.assertIsNotNone(client_context.brain.postprocessors)
        self.assertIsNone(client_context.brain.default_oob)
        self.assertIsNotNone(client_context.brain.oobs)

    def test_brain_init_with_config(self):

        yaml = YamlConfigurationFile()
        self.load_os_specific_configuration(yaml, "test_brain.yaml", "test_brain.windows.yaml")

        brain_config = BrainConfiguration()
        brain_config.load_configuration(yaml, ".")

        client = TestClient()
        client_context = client.create_client_context("testid")
        brain = Brain(client_context.bot, brain_config)
        self.assertIsNotNone(brain)

        self.assertIsNotNone(brain.aiml_parser)
        self.assertIsNotNone(brain.denormals)
        self.assertIsNotNone(brain.normals)
        self.assertIsNotNone(brain.genders)
        self.assertIsNotNone(brain.persons)
        self.assertIsNotNone(brain.person2s)
        self.assertIsNotNone(brain.properties)
        self.assertIsNotNone(brain.rdf)
        self.assertIsNotNone(brain.sets)
        self.assertIsNotNone(brain.maps)
        self.assertIsNotNone(brain.preprocessors)
        self.assertIsNotNone(brain.postprocessors)
        self.assertIsNotNone(brain.authentication)
        self.assertIsNotNone(brain.authorisation)
        self.assertIsNotNone(brain.default_oob)
        self.assertIsNotNone(brain.oobs)

        oob_content = ET.fromstring("<oob><something>other</something></oob>")
        self.assertEqual("", brain.default_oob.process_out_of_bounds(self._client_context, oob_content))
        oob_content = ET.fromstring("<oob><dial>07777777777</dial></oob>")
        self.assertEqual("", brain.oobs['dial'].process_out_of_bounds(self._client_context, oob_content))

    def test_brain_init_with_secure_config(self):

        yaml = YamlConfigurationFile()
        self.load_os_specific_configuration(yaml, "test_secure_brain.yaml", "test_secure_brain.windows.yaml")

        brain_config = BrainConfiguration()
        brain_config.load_configuration(yaml, os.path.dirname(__file__))

        client = TestClient()
        client_context = client.create_client_context("testid")
        brain = Brain(client_context.bot, brain_config)
        self.assertIsNotNone(brain)

        self.assertIsNotNone(brain.aiml_parser)
        self.assertIsNotNone(brain.denormals)
        self.assertIsNotNone(brain.normals)
        self.assertIsNotNone(brain.genders)
        self.assertIsNotNone(brain.persons)
        self.assertIsNotNone(brain.person2s)
        self.assertIsNotNone(brain.properties)
        self.assertIsNotNone(brain.rdf)
        self.assertIsNotNone(brain.sets)
        self.assertIsNotNone(brain.maps)
        self.assertIsNotNone(brain.preprocessors)
        self.assertIsNotNone(brain.postprocessors)
        self.assertIsNotNone(brain.authentication)
        self.assertIsNotNone(brain.authorisation)
        self.assertIsNone(brain.default_oob)
        self.assertEquals({}, brain.oobs)

    def test_oob_loading(self):

        yaml = YamlConfigurationFile()
        self.load_os_specific_configuration(yaml, "test_brain.yaml", "test_brain.windows.yaml")

        brain_config = BrainConfiguration()
        brain_config.load_configuration(yaml, ".")

        client = TestClient()
        client_context = client.create_client_context("testid")
        brain = Brain(client_context.bot, brain_config)

        self.assertIsInstance(brain.default_oob, DefaultOutOfBandProcessor)
        self.assertIsInstance(brain.oobs['dial'], DialOutOfBandProcessor)
        self.assertIsInstance(brain.oobs['email'], EmailOutOfBandProcessor)

    def test_oob_stripping(self):

        yaml = YamlConfigurationFile()
        self.load_os_specific_configuration(yaml, "test_brain.yaml", "test_brain.windows.yaml")

        brain_config = BrainConfiguration()
        brain_config.load_configuration(yaml, ".")

        client = TestClient()
        client_context = client.create_client_context("testid")
        brain = Brain(client_context.bot, brain_config)

        response, oob = brain.strip_oob("<oob>command</oob>")
        self.assertEqual("", response)
        self.assertEqual("<oob>command</oob>", oob)

        response, oob = brain.strip_oob("This <oob>command</oob>")
        self.assertEqual("This ", response)
        self.assertEqual("<oob>command</oob>", oob)

        response, oob = brain.strip_oob("This <oob>command</oob> That")
        self.assertEqual("This That", response)
        self.assertEqual("<oob>command</oob>", oob)

    def test_oob_processing(self):

        yaml = YamlConfigurationFile()
        self.load_os_specific_configuration(yaml, "test_brain.yaml", "test_brain.windows.yaml")

        brain_config = BrainConfiguration()
        brain_config.load_configuration(yaml, ".")

        client = TestClient()
        client_context = client.create_client_context("testid")
        brain = Brain(client_context.bot, brain_config)

        self.assertEqual("", brain.process_oob("console", "<oob></oob>"))
