import asyncio
import logging
import select
import socket
import time
import urllib
from datetime import datetime

import colorama
from worlds.ladx import LADXDeltaPatch
import Utils
from CommonClient import (ClientCommandProcessor, CommonContext,
                          get_base_parser, gui_enabled, logger, server_loop)
from worlds.ladx.Common import BASE_ID as LABaseID
from worlds.ladx.Items import ItemName, links_awakening_items_by_name
from worlds.ladx.LADXR.checkMetadata import checkMetadataTable
from worlds.ladx.Locations import get_locations_to_id, meta_to_name


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
    all_checks = []

    def __init__(self, gameboy):
        self.gameboy = gameboy
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
        lowest_check = 0xffff
        highest_check = 0

        for check in [x for x in checkMetadataTable if x not in blacklist]:
            room = check.split('-')[0]
            mask = 0x10
            address = addressOverrides[check] if check in addressOverrides else 0xD800 + int(room, 16)
            
            if 'Trade' in check or 'Owl' in check:
                    mask = 0x20

            if check in maskOverrides:
                mask = maskOverrides[check]
            
            lowest_check = min(lowest_check, address)
            highest_check = max(highest_check, address)
            if check in alternateAddresses:
                lowest_check = min(lowest_check, alternateAddresses[check])
                highest_check = max(highest_check, alternateAddresses[check])

            self.all_checks.append(Check(check, address, mask, alternateAddresses[check] if check in alternateAddresses else None))
            self.remaining_checks = [check for check in self.all_checks]
        self.gameboy.set_cache_limits(lowest_check, highest_check - lowest_check + 1)

        
    async def readChecks(self, read_byte_f, cb):
        for check in self.remaining_checks:

            addresses = [check.address]
            if check.alternateAddress:
                addresses.append(check.alternateAddress)
            bytes = await self.gameboy.read_memory_cache(addresses)
            if not bytes:
                return False
            check.set(list(bytes.values()))

            if check.value:
                self.remaining_checks.remove(check)
                cb(check)
                break
        return True

class LAClientConstants:
    # Connector version
    VERSION = 0x01
    #
    # Memory locations of LADXR
    ROMGameID = 0x0051 # 4 bytes
    #ROMWorldID = 0x0055
    #ROMConnectorVersion = 0x0056
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
    # wLinkSendShopItem = 0xDDFE # RO, which item to send (1 based, order of the shop items)
    wLinkSendShopTarget = 0xDDFF # RO, which player to send to, but it's just the X position of the NPC used, so 0x18 is player 0

    wRecvIndex = 0xDDFE # 0xDB58

    wCheckAddress = 0xD155
    WRamCheckSize = 0x13
    WRamSafetyValue = bytearray([0]*WRamCheckSize)
    
    MinGameplayValue = 0x06
    MaxGameplayValue = 0x1A
    VictoryGameplayAndSub = 0x0201

all_check_addresses = {}

for data in checkMetadataTable:
    if "-" not in data and data != "None":
        all_check_addresses[int(data, 16)] = checkMetadataTable[data]



class RAGameboy():
    cache = []
    cache_start = 0
    cache_size = 0
    last_cache_read = None
    socket = None
    def __init__(self, address, port) -> None:
        self.address = address
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(False)
        assert(self.socket)

    def set_cache_limits(self, cache_start, cache_size):
        self.cache_start = cache_start
        self.cache_size = cache_size
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

    async def is_in_gameplay(self):
        async def check_wram():
            check_values = await self.async_read_memory(LAClientConstants.wCheckAddress, LAClientConstants.WRamCheckSize)

            if check_values != LAClientConstants.WRamSafetyValue:
                return False
            return True

        if not await check_wram():
            return False

        gameplay_value = await self.async_read_memory(LAClientConstants.wGameplayType)
        gameplay_value = gameplay_value[0]
        if not (LAClientConstants.MinGameplayValue <= gameplay_value <= LAClientConstants.MaxGameplayValue):
            return False
        if not await check_wram():
            return False
        return True

    # We're sadly unable to update the whole cache at once 
    # as RetroArch only gives back some number of bytes at a time
    # So instead read as big as chunks at a time as we can manage
    async def update_cache(self):
        # First read the safety address - if it's invalid, bail
        self.cache = []
        
        if not await self.is_in_gameplay():
            return

        cache = []
        remaining_size = self.cache_size
        while remaining_size:
            block = await self.async_read_memory(self.cache_start + len(cache), remaining_size)
            remaining_size -= len(block)
            cache += block

        if not await self.is_in_gameplay():
            return

        self.cache = cache
        self.last_cache_read = time.time()

    async def read_memory_cache(self, addresses):
        # TODO: can we just update once per frame?
        if not self.last_cache_read or self.last_cache_read + 0.1 < time.time():
            await self.update_cache()
        if not self.cache:
            return None
        assert(len(self.cache) == self.cache_size)
        for address in addresses:
            assert self.cache_start <= address <= self.cache_start + self.cache_size
        r = {address: self.cache[address - self.cache_start] for address in addresses}
        return r

    async def async_read_memory_safe(self, address, size=1):
        # whenever we do a read for a check, we need to make sure that we aren't reading
        # garbage memory values - we also need to protect against reading a value, then the emulator resetting
        # 
        # ...actually, we probably _only_ need the post check 

        # Check before read
        if not self.is_in_gameplay():
            return None

        # Do read
        r = await self.async_read_memory(address, size)

        # Check after read
        if not self.is_in_gameplay():
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
        print(splits)
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


import binascii
class LinksAwakeningClient():
    socket = None
    gameboy = None
    tracker = None
    auth = None

    def msg(self, m):
        print(m)
        s = f"SHOW_MSG {m}\n"
        self.gameboy.send(s)

    def __init__(self, address="127.0.0.1", port=55355):
        print(port)
        self.gameboy = RAGameboy(address, port)
        print(f"Connected to Retroarch {self.get_retroarch_version()}")
        self.msg("AP Client connected")
        #for i in range(1, 1024):
        #    print(self.gameboy.read_memory(i * 1024, 1024))
        IMMEDIATELY_SEND_ITEM_TEST = False
        if IMMEDIATELY_SEND_ITEM_TEST:
            self.gameboy.write_memory(LAClientConstants.wLinkGiveItem, [3, 100])
            self.gameboy.write_memory(LAClientConstants.wLinkStatusBits, [1])

        self.reset_auth()


    def reset_auth(self):

        auth = binascii.hexlify(self.gameboy.read_memory(0x0134, 12)).decode()

        if self.auth:
            assert(auth == self.auth)
        
        self.auth = auth
        

    async def wait_and_init_tracker(self):
        await self.wait_for_game_ready()
        self.tracker = Tracker(self.gameboy)

    
    # TODO: this needs to be async and queueing
    def recved_item_from_ap(self, item_id, from_player, index):
        # TODO: the game breaks if you haven't talked to anyone before doing this
        
        next_index = self.gameboy.read_memory(LAClientConstants.wRecvIndex)[0]
        print(f"next index was {next_index}")
        if index != next_index:
            return


        # TODO: this needs to read and count current progressive item state??
        item_id -= LABaseID
        
        # The player name table only goes up to 100, so don't go past that
        # Even if it didn't, the remote player _index_ byte is just a byte, so 255 max
        if from_player > 100:
            from_player = 100

        # 2. write
        status = self.gameboy.read_memory(LAClientConstants.wLinkStatusBits)[0]
        while status & 1 == 1:
            time.sleep(0.1)
            status = self.gameboy.read_memory(LAClientConstants.wLinkStatusBits)[0]
        
        next_index += 1
        self.gameboy.write_memory(LAClientConstants.wLinkGiveItem, [item_id, from_player])
        status |= 1
        status = self.gameboy.write_memory(LAClientConstants.wLinkStatusBits, [status])
        self.gameboy.write_memory(LAClientConstants.wRecvIndex, [next_index]) 
        

    def get_retroarch_version(self):
        self.gameboy.send(b'VERSION\n')
        select.select([self.gameboy.socket], [], [])
        response_str, addr = self.gameboy.socket.recvfrom(16)
        return response_str.rstrip()
    
    min_safe_value=0xB
    async def wait_for_game_ready(self):
        while not self.gameboy.is_in_gameplay():
            pass
    
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
            await self.wait_and_init_tracker()


def create_task_log_exception(awaitable) -> asyncio.Task:
    async def _log_exception(awaitable):
        try:
            return await awaitable
        except Exception as e:
            logger.exception(e)
    return asyncio.create_task(_log_exception(awaitable))
import typing
class LinksAwakeningContext(CommonContext):
    tags = {"AP"}
    game = "Links Awakening DX"  # empty matches any game since 0.3.2
    items_handling = 0b101  # receive all items for /received
    want_slot_data = True  # Can't use game specific slot_data
    #slot = 1
    la_task = None
    client = None
    # TODO: this needs to re-read on reset
    found_checks = []
    last_resend = time.time()
    recvd_checks = {}
    def __init__(self, server_address: typing.Optional[str], password: typing.Optional[str]) -> None:
        self.client = LinksAwakeningClient()
        super().__init__(server_address, password)
    async def send_checks(self):
        message = [{"cmd": 'LocationChecks', "locations": self.found_checks}]
        await self.send_msgs(message)

    def found_check(self, item_id):
        self.found_checks.append(item_id)
        asyncio.create_task(self.send_checks())
        

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(LinksAwakeningContext, self).server_auth(password_requested)
        self.auth = self.client.auth
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.game = self.slot_info[self.slot].game
        # TODO - use watcher_event
        if cmd == "ReceivedItems":
            logging.info(f"Got items starting at {args['index']} of count {len(args['items'])}")
            for index, item in enumerate(args["items"], args["index"]):
                self.recvd_checks[index] = item
            logging.info(f"{self.recvd_checks}")
            index = self.client.gameboy.read_memory(LAClientConstants.wRecvIndex)[0]
            logging.info(f"Playing back from {index}")
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

async def main():
    parser = get_base_parser(description="Link's Awakening Client.")
    parser.add_argument("--url", help="Archipelago connection url")

    parser.add_argument('diff_file', default="", type=str, nargs="?",
                        help='Path to a .apladx Archipelago Binary Patch file')
    args = parser.parse_args()
    print(args)


    if args.diff_file:
        import Patch
        logger.info("patch file was supplied - creating rom...")
        meta, rom_file = Patch.create_rom_file(args.diff_file)
        if "server" in meta:
            args.url = meta["server"]
        logger.info(f"wrote rom file to {rom_file}")


    if args.url:
        url = urllib.parse.urlparse(args.url)
        args.connect = url.netloc
        if url.password:
            args.password = urllib.parse.unquote(url.password)

    ctx = LinksAwakeningContext(args.connect, args.password)
    
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    item_id_lookup = get_locations_to_id()

    def on_item_get(check):
        meta = checkMetadataTable[check.id]
        name = meta_to_name(meta)
        print(name)
        ap_id = item_id_lookup[name]
        ctx.found_check(ap_id)
        
    ctx.la_task = create_task_log_exception(ctx.run_game_loop(on_item_get))
    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    await ctx.exit_event.wait()
    await ctx.shutdown()

if __name__ == '__main__':    
    Utils.init_logging("LinksAwakeningContext", exception_logger="Client")

    colorama.init()    
    asyncio.run(main())
    colorama.deinit()


