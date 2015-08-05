#!/usr/bin/env python
# encoding: utf-8

import sys
import subprocess, re, time
from Xlib import X, display, error
import notify2

def get_winid(window_name):
    XWININFO_ID_PATTERN = re.compile(r'xwininfo: Window id: (0x[0-9a-f]+)')
    proc = subprocess.Popen(['xwininfo', '-name', window_name],
                                stdout=subprocess.PIPE)
    stdout = proc.communicate()[0].decode("utf8")
    if proc.returncode != 0:
        return None

    # extract the window id
    match = XWININFO_ID_PATTERN.search(stdout)
    if not match:
        raise ValueError('Could not extract window ID')

    return int(match.group(1), 16)

def main():
    notify2.init("monitor QQ")

    window_name = sys.argv[1]
    wid = get_winid(window_name)

    if wid:
        notify2.Notification("find chat window", "%s" % wid, "qq.png").show()
    else:
        notify2.Notification("can not find chat window", "", "dialog-warning").show()
        sys.exit(1)

    dpy = display.Display()
    window = dpy.create_resource_object('window', wid)

    data = ''
    while 1:
        try:
            raw = window.get_image(5, 260, 410, 110, X.ZPixmap, 0xffffffff)
        except error.BadDrawable:
            notify2.Notification("can not find chat window", "", "dialog-warning").show()
            sys.exit()

        if not data == raw.data:
            data = raw.data
            #msg_note = notify2.Notification("QQ message coming", "dialog-information")
            #msg_note.show()
            focused_id = dpy.get_input_focus()._data['focus'].id
            if not wid == focused_id:
                notify2.Notification("QQ message coming", "{}".format(datetime.today()), "/home/skt/.local/share/icons/qq.png").show()
            else:
                print("window active")
                # notify2.Notification("QQ message coming", "", "dialog-warning").show()
                pass
        else:
            # print("same")
            pass

        time.sleep(1)

if __name__ == '__main__':
    main()

