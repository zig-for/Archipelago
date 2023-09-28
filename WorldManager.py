from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
from kivy.uix.dropdown import DropDown
from kivymd.uix.button import MDFlatButton, MDRaisedButton

from collections import defaultdict
from dataclasses import dataclass
import requests
import json
import os
import typing
import zipfile
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
# Config.set('graphics', 'width', '1600')
Config.write()


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

class ApWorldLayout(MDBoxLayout):
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


class MainLayout(GridLayout):

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.cols = 1

from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen
from kivy.metrics import dp

from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.list import OneLineAvatarListItem

from kivymd.uix.list import OneLineListItem

KV = '''
<Item>
    MDRaisedButton:
        text: root.text
    ImageLeftWidget:
        source: root.source

'''
class Item(OneLineListItem):
    divider = None
    # source = StringProperty()

class WorldManagerApp(MDApp):
    def __init__(self, repositories) -> None:
        self.repositories = repositories
        super().__init__()
    
    def get_world_info(self):
        world_info = []
        self.world_name_to_id = {}
        self.available_versions = {}
        self.descriptions = {}
        for world_id in repositories.all_known_package_ids:
            available_versions = set()
            self.available_versions[world_id] = available_versions
            world_name = world_id
            installed_version = 'N/A'

            for world in self.repositories.packages_by_id_version[world_id].values():
                # Note, probably we need to use actual "properties" here to get good refresh
                world_name = world.name
                #world_info['available.text'] = str(world.world_version)
                available_versions.add(world.world_version)
                installed_version = world.world_version
                self.descriptions[world_id] = world.data['metadata']['description']
                
            if world_id in self.repositories.local_packages_by_id:
                world = self.repositories.local_packages_by_id[world_id]
                world_name = world.name
                #world_info['installed.text'] = str(world.world_version)
                available_versions.add(world.world_version)
                self.descriptions[world_id] = world.data['metadata']['description']


            available_versions.add("1.1.0")
            available_versions.add("1.1.1")
            available_versions.add("1.2.0")
            available_versions.add("1.3.0")


            # Unfortunate
            self.world_name_to_id[world_name] = world_id
            
            world_info.append([
                world_name,
                installed_version,
                list(available_versions)[-1],
                'Info/Set Version...',
            ])
        
        return world_info
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.rows = self.get_world_info()
        self.data_tables = MDDataTable(
            use_pagination=False,
            check=True,
            column_data=[
                ("Game", dp(80)),
                ("Installed Version", dp(30)),
                ("Newest Available", dp(30)),
                ("Set Version...", dp(40)),
            ],
            row_data=self.rows,
            sorted_on="Game",
            sorted_order="ASC",
            # elevation=200,
            rows_num=10000,
        )
        self.data_tables.bind(on_row_press=self.on_row_press)
        # self.data_tables.bind(on_check_press=self.on_check_press)
        screen = MDScreen()
        screen.add_widget(self.data_tables)

        screen.add_widget(MDRaisedButton(text="Update"))
        screen.add_widget(MDRaisedButton(text="Install"))
        screen.add_widget(MDRaisedButton(text="Uninstall"))

        return screen
    
    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''
       
        index = instance_row.index
        cols_num = len(instance_table.column_data)
        row_num = int(index/cols_num)
        col_num = index%cols_num

        cell_row = instance_table.table_data.view_adapter.get_visible_view(row_num*cols_num)
            
        # instance_table.background_color = self.theme_cls.primary_light
        # for id, widget in instance_row.ids.items():
        #     if id == "label":
        #         widget.color = self.theme_cls.primary_color
        
        # instance_row.add_widget(MDFlatButton(text="test"))
        #print(instance_table, instance_row, cell_row)
        #print(instance_row.text)
        if cols_num - 1 == col_num:
            # menu_items = [
            #     {
            #         "text": f"1.{i}.0",
            #         "viewclass": "OneLineListItem",

            #         "on_release": lambda x=f"Item {i}": print(x),
            #     } for i in range(3)
            # ]
            # MDDropdownMenu(
            #     caller=instance_row,
            #     items=menu_items,             
            #     width_mult=2,
            #     opening_time=0,
    
            # ).open()
            from kivymd.uix.dialog import MDDialog

            world_name = cell_row.text
            world_id = self.world_name_to_id[world_name]
            available_versions = self.available_versions[world_id]
            print(available_versions)
            desc = self.descriptions[world_id].replace('\n','')
            dialog = MDDialog(
                    type="simple",
                    # TODO: type="custom", would let us make our own buttons

                    text=f"[b]{cell_row.text}[/b]\n\n{desc}",
                    items = [
                       OneLineAvatarIconListItem(text=f'Install {version}') for version in available_versions
                    ],
                    buttons=[
                        MDRaisedButton(
                            text="Close",
                            on_release=lambda x: dialog.dismiss(force=True),
                        ),
                    ],
                    on_release=lambda x: print(x)
                )
            # dialog.add_widget(
            #         MDRaisedButton(
            #             text="v1.1.0",
            #             on_release=lambda x: dialog.dismiss(force=True))
            #     )
            dialog.open()
        # if cell_row.ids.check.state == 'normal':
        #     instance_table.table_data.select_all('normal')
        #     cell_row.ids.check.state = 'down'
        # else:
        #     cell_row.ids.check.state = 'normal'
        # instance_table.table_data.on_mouse_select(instance_row)

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
    