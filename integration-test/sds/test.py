import gdb_util
import os

def testSds5Struct():
    gdb_util.setup()
    str = "abc"
    gdb.execute('start')
    gdb.execute(f'set $obj = sdsnew("{str}")')
    gdb.execute('set $flag = *(((char*)$obj) - 1)')
    gdb.execute('set $type = $flag & 0b111')
    gdb.execute('set $len = $flag >> 3')
    type = gdb.parse_and_eval("$type")
    len = gdb.parse_and_eval("$len")
    code = 0
    if type != 0 or len != 3:
        code = 1
        print(f"Error: type = {type}, len = {len}")
    gdb.execute(f'quit {code}')

def testSds8Struct():
    gdb_util.setup()
    str = "abcdefgh"
    long_str = str * 5 + "abc"
    gdb.execute('start')
    gdb.execute(f'set $obj = sdsnew("{long_str}")')
    gdb.execute('set $hdr = (struct sdshdr8*)(((char*)$obj) - 3)')
    gdb.execute('set $alloc = (*$hdr)->alloc')
    gdb.execute('set $len = (*$hdr)->len')
    gdb.execute('set $flag = (*$hdr)->flags')
    gdb.execute('set $type = $flag & 0b111')
    type = gdb.parse_and_eval("$type")
    len = gdb.parse_and_eval("$len")
    alloc = gdb.parse_and_eval("$alloc")
    code = 0
    if type != 1 or len != 43 or alloc != 44:
        code = 1
        print(f"Error: type = {type}, len = {len}, alloc = {alloc}")
    gdb.execute(f'quit {code}')

def testSdsGrowZero():
    gdb_util.setup()
    str = "abcdefgh"
    gdb.execute('start')
    gdb.execute(f'set $obj = sdsnew("{str}")')
    gdb.execute(f'set $hdr = $obj - 1')
    gdb.execute('set $flag = *$hdr')
    type = gdb.parse_and_eval("$flag & 0b111")
    length = gdb.parse_and_eval("$flag >> 3")
    code = 0
    if type != 0 or length != len(str):
        code = 1
        print(f"Error: type = {type}, len = {length}")
        gdb.execute(f'quit {code}')
    new_len = 100
    gdb.execute(f'set $obj = sdsgrowzero($obj, {new_len})')
    gdb.execute(f'set $hdr = (struct sdshdr8*)($obj - 3)')
    type = gdb.parse_and_eval("$hdr->flags & 0b111")
    length = gdb.parse_and_eval("$hdr->len")
    zero = gdb.parse_and_eval(f"$obj[{length - 1}]")
    code = 0
    if type != 1 or length != new_len or zero != 0:
        code = 1
        print(f"Error: type = {type}, len = {length}, zero = {zero}")
        gdb.execute(f'quit {code}')
    gdb.execute(f'quit')

def testSdscatfmt():
    gdb_util.setup()
    str_val = "abc"
    gdb.execute('start')
    gdb.execute(f'set $obj = sdsnew("{str_val}")')
    val = gdb.parse_and_eval('sdscatfmt($obj, "def%i%%%?%S", 123, sdsnew("ghi"))')
    expected = "abcdef123%?ghi"
    code = 0
    if val.string() != expected:
        code = 1
        print(f"Error: expected '{expected}', got '{val}'")
    gdb.execute(f'quit {code}')

func = os.environ['testFunction']
locals()[func]()

