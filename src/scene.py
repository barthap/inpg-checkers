from abc import ABC
from typing import Dict, Any
import pydoc


# Base class for game scene (Intro, Menu, Game etc.). All states should derive from it
class BaseScene(ABC):
	def __init__(self, app: 'App'):
		self.app = app

	def setup(self):
		pass

	def update(self, events):
		pass

	# something like destructor, called when state is changing or app is quitting
	def destroy(self):
		pass


class SceneManager:
	def __init__(self, app: 'App'):
		self._scenes: Dict[str, BaseScene] = {}
		self.current: BaseScene = None
		self.app = app

	# Call this after pygame.init()
	def setup(self, initial: str):
		self.go(initial)

	def get_scene_object(self, scene_name: str, reload=False, arg: Any=None) -> BaseScene:
		if scene_name in self._scenes.keys() and not reload:
			scene = self._scenes[scene_name]

		else:
			scene_class = pydoc.locate(scene_name)
			if scene_class is None:
				raise RuntimeError("Couldn't load scene " + scene_name)
			if arg is None:
				scene = scene_class(self.app)
			else:
				scene = scene_class(self.app, arg)
			self._scenes[scene_name] = scene
			print("Loaded", scene_class.__name__)

		return scene

	def go(self, new_scene: str, reload=False, arg: Any=None):
		if self.current is not None:
			self.current.destroy()
		self.current = self.get_scene_object(new_scene, reload, arg)
		self.current.setup()

	def go_once(self, scene_object):
		assert isinstance(scene_object, BaseScene)
		if self.current is not None:
			self.current.destroy()
		self.current = scene_object
		self.current.setup()
