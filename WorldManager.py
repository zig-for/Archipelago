from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config

import typing
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'width', '1200')

Builder.load_string('''
<Widget>:
    canvas.after:
        Line:
            rectangle: self.x+1,self.y+1,self.width-1,self.height-1
            # Can't figure out line colors lmao
            # This is not the proper way to do this
            # dash_offset: 5
            # dash_length: 3
                    
<ApWorldLayout@RecycleKVIDsDataViewBehavior+StackLayout>:
    size_hint_y: None
    height: 30

    Label:
        id: world_name
        # text: world_data.name  # uses the text StringProperty
        text: ' Game'
        size_hint: None, None
        size: 300, 30
        text_size: self.size
        halign: 'left'
        valign: 'middle'
    Label:
        id: installed
        # text: world_data.name  # uses the text StringProperty
        text: 'Installed Version'
        size_hint: None, None
        size: 150, 30
    Label:
        id: foobar
        # text: world_data.name  # uses the text StringProperty
        text: 'Newest Available'
        size_hint: None, None
        size: 150, 30
    Label:
        id: info
        # text: world_data.name  # uses the text StringProperty
        text: 'Info'
        size_hint: None, None
        size: 300, 30
    Button:
        id: available
        # text: world_data.name  # uses the text StringProperty
        text: 'Install'
        size_hint: None, None
        size: 150, 30
    # DropDown:
    #     id: versions
                    
<RV>:
    viewclass: 'ApWorldLayout'
    RecycleBoxLayout:
        default_size: None, 30
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
<LoginScreen>:

    ApWorldLayout:
        id: header
    RV:
        id: rv             
''')

from dataclasses import dataclass


@dataclass
class ApWorldVersion:
    blessed: bool

@dataclass
class ApWorldMetadata:
    name: str
    developers: list[str]
    installed_version: typing.Optional[str]
    versions: dict[str, ApWorldVersion]

# TODO: check against from source

TEST_WORLDS = [
    ApWorldMetadata("Link to the Past", ["AP Core Team"], '1.0.0', {"1.0.0": True}),
    ApWorldMetadata("Link's Awakening", ["zig"], None, {"1.0.0": ApWorldVersion(True), "1.1.0": ApWorldVersion(False)}),
    ApWorldMetadata('adventure', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('alttp', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('archipidle', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('bk_sudoku', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('blasphemous', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('bumpstik', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('checksfinder', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('clique', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('dark_souls_3', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('dkc3', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('dlcquest', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('doom_1993', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('factorio', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('ff1', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('hk', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('hylics2', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('kh2', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('ladx', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('lufia2ac', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('meritous', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('messenger', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('minecraft', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('mmbn3', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('musedash', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('noita', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('oot', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('oribf', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('overcooked2', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('pokemon_rb', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('raft', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('rogue_legacy', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('ror2', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('sa2b', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('sc2wol', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('sm', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('sm64ex', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('smw', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('smz3', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('soe', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('spire', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('stardew_valley', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('subnautica', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('terraria', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('timespinner', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('tloz', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('undertale', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('v6', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('wargroove', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('witness', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),
    ApWorldMetadata('zillion', ['test data'], None, {"0.1.0": ApWorldVersion(True)}),

]



class ApWorldLayout(BoxLayout):
    show = ObjectProperty(None)
    text = StringProperty('Abba')

    # # Do I need this?
    # def on_show(self, instance, new_obj):
    #     # handle the ObjectProperty named show
    #     if new_obj.parent:
    #         # remove this obj from any other MyObject instance
    #         new_obj.parent.remove_widget(new_obj)
    #     for ch in self.children:
    #         if isinstance(ch, Image):
    #             # remove any previous obj instances
    #             self.remove_widget(ch)
    #             break
    #     # add the new obj to this MyObject instance
    #     self.add_widget(new_obj)

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{
            'world_name.text': ' ' + world.name,
            'installed.text': str(world.installed_version),
            'available.text': 'click me'
                      }
                     for world in TEST_WORLDS]
        
class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 1



class WorldManagerApp(App):

    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    WorldManagerApp().run()