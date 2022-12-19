import time
import socket
from worlds.la.Items import ItemName, links_awakening_items_by_name
from worlds.la.Common import BASE_ID as LABaseID
from worlds.la.LADXR.checkMetadata import checkMetadataTable
from worlds.la.Locations import get_locations_to_id, meta_to_name
import select
# kbranch you're a hero
# https://github.com/kbranch/Magpie/blob/master/autotracking/checks.py
class Check:
    def __init__(self, id, address, mask, alternateAddress=None):
        self.id = id
        self.address = address
        self.alternateAddress = alternateAddress
        self.mask = mask
        self.value = None
        self.diff = 0
    
    def set(self, bytes):
        oldValue = self.value

        self.value = 0

        for byte in bytes:
            maskedByte = byte
            if self.mask:
                maskedByte &= self.mask
            
            self.value |= int(maskedByte > 0)

        if oldValue != self.value:
            self.diff += self.value - (oldValue or 0)

            #if self.diff != 0:
            #    print(f'Found {self.id}: {"+" if self.diff > 0 else ""}{self.diff}')

class Tracker:
    def __init__(self):
        self.all_checks = []
        
        maskOverrides = {
            '0x106': 0x20,
            '0x12B': 0x20,
            '0x15A': 0x20,
            '0x166': 0x20,
            '0x185': 0x20,
            '0x1E4': 0x20,
            '0x1BC': 0x20,
            '0x1E0': 0x20,
            '0x1E1': 0x20,
            '0x1E2': 0x20,
            '0x223': 0x20,
            '0x234': 0x20,
            '0x2A3': 0x20,
            '0x2FD': 0x20,
            '0x2A1-1': 0x20,
            '0x1F5': 0x06,
            '0x301-0': 0x10,
            '0x301-1': 0x10,
        }

        addressOverrides = {
            '0x30A-Owl': 0xDDEA,
            '0x30F-Owl': 0xDDEF,
            '0x308-Owl': 0xDDE8,
            '0x302': 0xDDE2,
            '0x306': 0xDDE6,
            '0x307': 0xDDE7,
            '0x308': 0xDDE8,
            '0x30F': 0xDDEF,
            '0x311': 0xDDF1,
            '0x314': 0xDDF4,
            '0x1F5': 0xDB7D,
            '0x301-0': 0xDDE1,
            '0x301-1': 0xDDE1,
            '0x223': 0xDA2E,
            '0x169': 0xD97C,
        }

        alternateAddresses = {
            '0x0F2': 0xD8B2,
        }

        blacklist = {'None', '0x2A1-2'}

        # in no dungeons boss shuffle, the d3 boss in d7 set 0x20 in fascade's room (0x1BC)
        # after beating evil eagile in D6, 0x1BC is now 0xAC (other things may have happened in between)
        # entered d3, slime eye flag had already been set (0x15A 0x20). after killing angler fish, bits 0x0C were set

        for check in [x for x in checkMetadataTable if x not in blacklist]:
            room = check.split('-')[0]
            mask = 0x10
            address = addressOverrides[check] if check in addressOverrides else 0xD800 + int(room, 16)
            
            if 'Trade' in check or 'Owl' in check:
                mask = 0x20

            if check in maskOverrides:
                mask = maskOverrides[check]
            
            self.all_checks.append(Check(check, address, mask, alternateAddresses[check] if check in alternateAddresses else None))
            self.remaining_checks = [check for check in self.all_checks]

    async def readChecks(self, read_byte_f, cb):
        for check in self.remaining_checks:
            bytes = [await read_byte_f(check.address)]
            if bytes[0] is None:
                print("not ok")
                return False
            
            if check.alternateAddress != None:
                bytes.append(await read_byte_f(check.alternateAddress))
                if bytes[1] is None:
                    print("not ok")
                    return False
            check.set(bytes)

            if check.value:
                self.remaining_checks.remove(check)
                cb(check)
                break
        return True
class LAClientConstants():
    # Connector version
    VERSION = 0x01
    #
    # Memory locations of LADXR
    ROMGameID = 0x0051 # 4 bytes
    ROMWorldID = 0x0055
    ROMConnectorVersion = 0x0056
    wGameplayType = 0xDB95            # RO: We should only act if this is higher then 6, as it indicates that the game is running normally
    wLinkSyncSequenceNumber = 0xDDF6  # RO: Starts at 0, increases every time an item is received from the server and processed
    wLinkStatusBits = 0xDDF7          # RW:
    #      Bit0: wLinkGive* contains valid data, set from script cleared from ROM.
    #      Bit1: wLinkSendItem* contains valid data, set from ROM cleared from lua
    #      Bit2: wLinkSendShop* contains valid data, set from ROM cleared from lua
    wLinkGiveItem = 0xDDF8 # RW
    wLinkGiveItemFrom = 0xDDF9 # RW
    wLinkSendItemRoomHigh = 0xDDFA # RO
    wLinkSendItemRoomLow = 0xDDFB # RO
    wLinkSendItemTarget = 0xDDFC # RO
    wLinkSendItemItem = 0xDDFD # RO
    wLinkSendShopItem = 0xDDFE # RO, which item to send (1 based, order of the shop items)
    wLinkSendShopTarget = 0xDDFF # RO, which player to send to, but it's just the X position of the NPC used, so 0x18 is player 0

all_check_addresses = {}

for data in checkMetadataTable:
    if "-" not in data and data != "None":
        all_check_addresses[int(data, 16)] = checkMetadataTable[data]


wRecvIndex = 0xDB58


class LinksAwakeningClient():
    socket = None
    address = "127.0.0.1"
    port = 55355
    

    def msg(self, m):
        print(m)
        s = f"SHOW_MSG {m}\n"
        self.send(s)

    def __init__(self, address="127.0.0.1", port=55355):
        self.address = address
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(False) 
        print(f"Connected to Retroarch {self.get_retroarch_version()}")
        self.msg("AP Client connected")
        print(self.read_memory(LAClientConstants.ROMGameID, 4))
        print(self.read_memory(LAClientConstants.ROMConnectorVersion, 1))
        
    tracker = None

    async def wait_and_init_tracker(self):
        await self.wait_for_game_ready()
        self.tracker = Tracker()

    def send(self, b):
        if type(b) is str:
            b = b.encode('ascii')
        self.socket.sendto(b, (self.address, self.port))

    def recv(self):
        select.select([self.socket], [], [])
        response, _ = self.socket.recvfrom(4096)
        return response
    async def async_recv(self):
        response = await asyncio.get_event_loop().sock_recv(self.socket, 4096)
        return response
    # TODO: this needs to be async and queueing
    def recved_item_from_ap(self, item_id, from_player, index):
        # TODO: the game breaks if you haven't talked to anyone before doing this
        
        next_index = self.read_memory(wRecvIndex)[0]
        
        if index != next_index:
            print("bailing")
            return
        next_index += 1
        next_index = self.write_memory(wRecvIndex, [next_index])

        # TODO: this needs to read and count current progressive item state
        item_id -= LABaseID
        
        if from_player > 255:
            from_player = 255

        # 2. write
        status = self.read_memory(LAClientConstants.wLinkStatusBits)[0]
        while status & 1 == 1:
            time.sleep(0.1)
            status = self.read_memory(LAClientConstants.wLinkStatusBits)[0]
        print(from_player)
        self.write_memory(LAClientConstants.wLinkGiveItem, [item_id, from_player])
        status |= 1
        status = self.write_memory(LAClientConstants.wLinkStatusBits, [status])
        

    def get_retroarch_version(self):
        self.send(b'VERSION\n')
        select.select([self.socket], [], [])
        response_str, addr = self.socket.recvfrom(16)
        return response_str.rstrip()
    
    safety_address = 0xDB95 
    min_safe_value=0xB
    async def wait_for_game_ready(self):
        check_value = 0
        while not self.safety_is_safe(check_value):
            check_value = (await self.async_read_memory(self.safety_address))[0]
    def safety_is_safe(self, value):
        #if not 6 <= value < 0x1A:
        #    print(value)
        return 6 <= value < 0x1A
        #return value in [0xB, 0xC]
    
    async def async_read_memory_safe(self, address, size=1):
        # whenever we do a read for a check, we need to make sure that we aren't reading
        # garbage memory values - we also need to protect against reading a value, then the emulator resetting
        # 
        # ...actually, we probably _only_ need the post check 

        # Check before read
        check_value = await self.async_read_memory(self.safety_address, size)

        if not self.safety_is_safe(check_value[0]):
            return None

        # Do read
        r = await self.async_read_memory(address, size)

        # Check after read
        check_value = await self.async_read_memory(self.safety_address, size)
        if not self.safety_is_safe(check_value[0]):
            return None
        
        return r
    def read_memory(self, address, size = 1):
        command = "READ_CORE_MEMORY"
        
        self.send(f'{command} {hex(address)} {size}\n')
        response = self.recv()
        
        splits = response.decode().split(" ", 2)

        assert(splits[0] == command)
        # Ignore the address for now

        # TODO: transform to bytes
        return bytearray.fromhex(splits[2])
    
    async def async_read_memory(self, address, size = 1):
        command = "READ_CORE_MEMORY"
        
        self.send(f'{command} {hex(address)} {size}\n')
        response = await self.async_recv()
        response = response[:-1]
        splits = response.decode().split(" ", 2)

        assert(splits[0] == command)
        # Ignore the address for now

        # TODO: transform to bytes
        return bytearray.fromhex(splits[2])

    def write_memory(self, address, bytes):
        command = "WRITE_CORE_MEMORY"
        
        self.send(f'{command} {hex(address)} {" ".join(hex(b) for b in bytes)}')
        select.select([self.socket], [], [])
        response, _ = self.socket.recvfrom(4096)
        
        splits = response.decode().split(" ", 3)

        assert(splits[0] == command)

        if splits[2] == "-1":
            print(splits[3])
    
    
    async def main_tick(self, cb):
        if not self.tracker:
            await self.wait_and_init_tracker()

        async def read_byte(b):
            mem = await self.async_read_memory_safe(b)
            if mem is None:
                return None
            return mem[0]

        ok = await self.tracker.readChecks(read_byte, cb)
        if not ok:
            self.msg("Invalid game state detected, resetting tracker")
            await self.wait_and_init_tracker()
        #time.sleep(1)
import colorama
import asyncio
import urllib
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, \
    CommonContext, server_loop
from CommonClient import CommonContext
import Utils

if __name__ == '__main__':    
    Utils.init_logging("LinksAwakeningContext", exception_logger="Client")
    # Text Mode to use !hint and such with games that have no text entry

    class LinksAwakeningContext(CommonContext):
        tags = {"AP"}
        game = "Links Awakening"  # empty matches any game since 0.3.2
        items_handling = 0b101  # receive all items for /received
        want_slot_data = True  # Can't use game specific slot_data
        #slot = 1
        la_task = None
        client = LinksAwakeningClient()
        found_checks = []
        last_resend = time.time()
        recvd_checks = {}
        async def send_checks(self):
            message = [{"cmd": 'LocationChecks', "locations": self.found_checks}]
            await self.send_msgs(message)

        def found_check(self, item_id):
            self.found_checks.append(item_id)
            asyncio.create_task(self.send_checks())
            

        async def server_auth(self, password_requested: bool = False):
            if password_requested and not self.password:
                await super(LinksAwakeningContext, self).server_auth(password_requested)
            await self.get_username()
            await self.send_connect()

        def on_package(self, cmd: str, args: dict):
            if cmd == "Connected":
                self.game = self.slot_info[self.slot].game
            # TODO - use watcher_event
            if cmd == "ReceivedItems":
                for index, item in enumerate(args["items"], args["index"]):
                    print(item)
                    self.recvd_checks[index] = item
                print(self.recvd_checks)
                index = self.client.read_memory(wRecvIndex)[0]
                while index in self.recvd_checks:
                    item = self.recvd_checks[index]
                    self.client.recved_item_from_ap(item.item, item.player, index)
                    index += 1

        async def run_game_loop(self, item_get_cb):
            while True:
                await self.client.main_tick(item_get_cb)
                await asyncio.sleep(0.1)
                now = time.time()
                if self.last_resend + 5.0 < now:
                    self.last_resend = now
                    await self.send_checks()

    async def main(args):
        ctx = LinksAwakeningContext(args.connect, args.password)
        ctx.auth = args.name
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

        item_id_lookup = get_locations_to_id()

        def on_item_get(check):
            meta = checkMetadataTable[check.id]
            name = meta_to_name(meta)
            print(name)
            ap_id = item_id_lookup[name]
            ctx.found_check(ap_id)
            
        ctx.la_task = asyncio.create_task(ctx.run_game_loop(on_item_get))
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    parser = get_base_parser(description="Gameless Archipelago Client, for text interfacing.")
    parser.add_argument('--name', default=None, help="Slot Name to connect as.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")
    args = parser.parse_args()

    if args.url:
        url = urllib.parse.urlparse(args.url)
        args.connect = url.netloc
        if url.username:
            args.name = urllib.parse.unquote(url.username)
        if url.password:
            args.password = urllib.parse.unquote(url.password)

    colorama.init()    
    asyncio.run(main(args))
    colorama.deinit()


