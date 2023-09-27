from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

from collections import defaultdict
from dataclasses import dataclass
import requests
import json
import os
import typing
import zipfile
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'width', '1600')
Config.write()

Builder.load_string('''
<Widget>:
    canvas.after:
        Line:
            rectangle: self.x,self.y,self.width,self.height
            # Can't figure out line colors lmao

<CustomDropDown>:
    Button:
        text: 'My first Item'
        size_hint_y: None
        height: 44
        on_release: root.select('item1')
    Label:
        text: 'Unselectable item'
        size_hint_y: None
        height: 44
    Button:
        text: 'My second Item'
        size_hint_y: None
        height: 44
        on_release: root.select('item2')                   
<ApWorldLayout@RecycleKVIDsDataViewBehavior+StackLayout>:
    size_hint_y: None
    height: 30

    Label:
        id: world_name
        text: ' Game'
        size_hint: None, None
        size: 300, 30
        text_size: self.size
        halign: 'left'
        valign: 'middle'
    Label:
        id: installed
        text: 'Installed Version'
        size_hint: None, None
        size: 150, 30
    Label:
        id: available
        text: 'Newest Available'
        size_hint: None, None
        size: 150, 30
    InfoButton:
        id: info
        text: 'Info'
        size_hint: None, None
        size: 75, 30
    InstallButton:
        id: install
        text: 'Install'
        size_hint: None, None
        size: 75, 30
    DropBut:
        id: available_versions
        size_hint: None, None
        size: 150, 30
        background_color: 0,0,0
        text: 'Install Version...'
    CheckBox:
        id: is_installed
        size_hint: None, None
        size: 75, 30


<PackagesRV>:
    viewclass: 'ApWorldLayout'

    RecycleBoxLayout:
        default_size: None, 30
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
<MainLayout>:
    ApWorldLayout:
        id: header
    PackagesRV:
        id: rv        
    GridLayout:
        columns: 2
        rows: 1
        size_hint_y: None
        row_default_height: 1
        Button:
            id: refresh
            text: 'Refresh'
            size_hint_y: None
        Button:
            id: autoupdate
            text: 'Auto-Update'
            size_hint_y: None
''')
from kivy.properties import ListProperty
class DropBut(Button):
    options = ListProperty(['test'])
    foobar = StringProperty()
    def __init__(self, **kwargs):
        super(DropBut, self).__init__(**kwargs)
        
        self.drop_list = None
        self.drop_list = DropDown()

        # options = ['1.1.0', '1.1.1', '1.1.1-doors']
       
        self.bind(on_release=self.drop_list.open)

        def on_drop_list_select(instance, x):
            setattr(self, 'text', x)
        self.drop_list.bind(on_select=on_drop_list_select)

    def on_options(self, instance, value):
        for i in value:
            btn = Button(text=i, size_hint_y=None, height=25)
            btn.bind(on_release=lambda btn: self.drop_list.select(btn.text))
           
            self.drop_list.add_widget(btn)


class CustomDropDown(DropDown):
    pass


@dataclass
class ApWorldVersion:
    blessed: bool

@dataclass
class ApWorldMetadataAllVersions:
    name: str
    developers: list[str]
    installed_version: typing.Optional[str]
    versions: dict[str, ApWorldVersion]

from enum import Enum


class WorldSource(Enum):
    SOURCE_CODE = 0
    LOCAL = 1
    REMOTE_BLESSED = 2
    REMOTE = 3

@dataclass
class ApWorldMetadata:
    source: WorldSource
    source_url: typing.Optional[str]
    data: dict[str, typing.Any]
    # source: WorldSource

    # TODO: .validate()

    @property
    def id(self) -> str:
        return self.data['metadata']['id']
    
    @property
    def name(self) -> str:
        return self.data['metadata']['game']
    
    @property
    def world_version(self) -> str:
        return self.data['metadata']['world_version']


class Repository:
    def __init__(self, world_source: WorldSource, path: str) -> None:
        self.path = path
        self.index_json = None
        self.world_source = world_source

        self.worlds: typing.List[ApWorldMetadata] = []

    def refresh(self):
        self.get_repository_json()

    def get_repository_json(self):
        if self.world_source == WorldSource.REMOTE or self.world_source == WorldSource.REMOTE_BLESSED:
            response = requests.get(self.path)
            self.index_json = response.json()

            self.worlds = [
                ApWorldMetadata(self.world_source, self.path, world) for world in self.index_json['worlds']
            ]
        elif self.world_source == WorldSource.LOCAL:
            self.worlds = []
            print(self.path)
            for file in os.listdir(self.path):
                try:
                    metadata_str = zipfile.ZipFile(os.path.join(self.path, file)).read('metadata.json')
                    metadata = json.loads(metadata_str)
                    metadata = {
                        'metadata': metadata
                    }
                    self.worlds.append(ApWorldMetadata(self.world_source, self.path, metadata))
                except:
                    continue
        
                # ApWorldMetadata(self.world_source, self.path, world) for world in self.index_json['worlds']
            
        else:
            assert False
        self.worlds.sort(key = lambda x: x.name)

class RepositoryManager:
    def __init__(self) -> None:
        self.all_known_package_ids: typing.Set[str] = set()
        self.repositories: typing.List[Repository] = []
        self.local_packages_by_id: typing.Dict[str, ApWorldMetadata] = {}
        self.packages_by_id_version: typing.DefaultDict[str, typing.Dict[str, ApWorldMetadata]] = defaultdict(dict)

    def add_local_dir(self, path: str):
        self.repositories.append(Repository(WorldSource.LOCAL, path))
        
    def add_remote_repository(self, url: str, blessed=False) -> None:
        self.repositories.append(Repository(WorldSource.REMOTE_BLESSED if blessed else WorldSource.REMOTE, url))

    def refresh(self):
        self.packages_by_id_version.clear()
        for repo in self.repositories:
            repo.refresh()
            if repo.world_source == WorldSource.LOCAL:
                for world in repo.worlds:
                    self.all_known_package_ids.add(world.id)
                    self.local_packages_by_id[world.id] = world
            else:
                for world in repo.worlds:
                    self.all_known_package_ids.add(world.id)
                    self.packages_by_id_version[world.id][world.world_version] = world
        print(self.packages_by_id_version)

class ApWorldLayout(BoxLayout):
    show = ObjectProperty(None)
    # text = StringProperty('None')

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

class InfoButton(Button):
    def on_press(self):
        try:
            game_id = getattr(self.parent, 'game_id')
        except:
            return
        
        print(f'The info button <{game_id}> is being pressed')
    

class InstallButton(Button):
    def on_press(self):
        try:
            game_id = getattr(self.parent, 'game_id')
        except:
            return
        
        print(f'The install button <{game_id}> is being pressed')

class PackagesRV(RecycleView):
    def __init__(self, **kwargs):
        super(PackagesRV, self).__init__(**kwargs)
        self.data = []
        self.repositories = None

    def set_repositories(self, repositories):
        self.repositories = repositories
        self.data = []

        for world_id in repositories.all_known_package_ids:
            available_versions = set()
            world_info = {
                'game_id': world_id,
                # 'info.game_id': world_id,
                'available.text': 'N/A',
                'install.disabled': True,
                'available_versions.text': 'N/A'
            }
            for world in repositories.packages_by_id_version[world_id].values():
                # Note, probably we need to use actual "properties" here to get good refresh
                world_info['world_name.text'] = world.name
                world_info['available.text'] = str(world.world_version)
                world_info['install.disabled'] = False
                available_versions.add(world.world_version)
                
            if world_id in repositories.local_packages_by_id:
                world = repositories.local_packages_by_id[world_id]
                world_info['world_name.text'] = world.name
                world_info['installed.text'] = str(world.world_version)
                available_versions.add(world.world_version)
                world_info['available_versions.text'] = str(world.world_version)
            else:
                world_info['installed.text'] = 'N/A'
            world_info['available_versions.options'] = list(available_versions)
            
            world_info['world_name.text'] = ' ' + world_info['world_name.text']
            self.data.append(world_info)
        from Utils import title_sorted
        self.data = title_sorted(self.data, key=lambda x: x['world_name.text'])

class MainLayout(GridLayout):

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.cols = 1



class WorldManagerApp(App):
    def __init__(self, repositories) -> None:
        self.repositories = repositories
        super().__init__()
    
    def build(self):
        layout = MainLayout()
        
        layout.ids['rv'].set_repositories(self.repositories)

        return layout


import asyncio


if __name__ == '__main__':
    local_dir = './worlds_test_dir'

    repositories = RepositoryManager()
    repositories.add_remote_repository('http://localhost:8080/index.json')
    repositories.add_local_dir(local_dir)
    repositories.refresh()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = WorldManagerApp(repositories)
    loop.run_until_complete(app.async_run())
    loop.close()
    