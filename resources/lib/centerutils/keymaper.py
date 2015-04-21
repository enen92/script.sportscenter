# -*- coding: utf-8 -*-
# Copyright (C) 2015 enen92
#
# Base code by takoi changed by anonymous
#
# This program is free software; you can redistribute it and/or modify it under the terms 
# of the GNU General Public License as published by the Free Software Foundation; 
# either version 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program; 
# if not, see <http://www.gnu.org/licenses/>.

import xbmc
import xbmcgui
import xbmcplugin
import xbmcvfs
import os
import shutil
import xml.etree.ElementTree as ET

default = xbmc.translatePath('special://xbmc/system/keymaps/keyboard.xml')
userdata = xbmc.translatePath('special://userdata/keymaps')
gen_file = os.path.join(userdata, 'gen.xml')

### Key mapp			
def run(start):
	## load mappings ##
	try:
		setup_keymap_folder()
	except Exception:
		pass

	defaultkeymap = read_keymap(default)
	userkeymap = []
	if os.path.exists(gen_file):
		try:
			userkeymap = read_keymap(gen_file)
		except Exception:
			pass
	newkey = KeyListener.record_key()

	if newkey:
		if os.path.exists(gen_file):
			shutil.copyfile(gen_file, gen_file + ".old")
			
		if start: new = ('global', u'RunScript(special://home/addons/cona/resources/lib/recs.py, start)', newkey)
		else: new = ('global', u'RunScript(special://home/addons/cona/resources/lib/recs.py, stop)', newkey)
		
		done = False
		if len(userkeymap) !=0:
			_userkeymap = list(userkeymap)
			_u = []
			for u in _userkeymap:
				_u.append(list(u))
			for u in _u:
				if u[2] == newkey:
					u[0] = new[0]
					u[1] = new[1]
					done = True
					break
		if done: 
			final_userkeymap = []
			for u in _u:
				final_userkeymap.append(tuple(u))
			write_keymap(final_userkeymap, gen_file)
		else:
			userkeymap.append(new)
			write_keymap(userkeymap, gen_file)
		xbmc.executebuiltin("Action(reloadkeymaps)")
		xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (traducao(1023), traducao(1024), 1,addonfolder+"/icon.png"))

class KeyListener(WindowXMLDialog):
    TIMEOUT = 5

    def __new__(cls):
        return super(KeyListener, cls).__new__(cls, "DialogKaiToast.xml", "")

    def __init__(self):
        self.key = None

    def onInit(self):
        try:
            self.getControl(401).addLabel(traducao(1021))
            self.getControl(402).addLabel(traducao(1022) % self.TIMEOUT)
        except AttributeError:
            self.getControl(401).setLabel(traducao(1021))
            self.getControl(402).setLabel(traducao(1022) % self.TIMEOUT)

    def onAction(self, action):
        code = action.getButtonCode()
        self.key = None if code == 0 else str(code)
        self.close()

    @staticmethod
    def record_key():
        dialog = KeyListener()
        timeout = Timer(KeyListener.TIMEOUT, dialog.close)
        timeout.start()
        dialog.doModal()
        timeout.cancel()
        key = dialog.key
        del dialog
        return key
        
def read_keymap(filename):
    ret = []
    with open(filename, 'r') as xml:
        tree = ET.iterparse(xml)
        for _, keymap in tree:
            for context in keymap:
                for device in context:
                    for mapping in device:
                        key = mapping.get('id') or mapping.tag
                        action = mapping.text
                        if action:
                            ret.append((context.tag.lower(), action.lower(), key.lower()))
    return ret
    
def setup_keymap_folder():
    if not os.path.exists(userdata):
        os.makedirs(userdata)
    else:
        #make sure there are no user defined keymaps
        for name in os.listdir(userdata):
            if name.endswith('.xml') and name != os.path.basename(gen_file):
                src = os.path.join(userdata, name)
                for i in xrange(100):
                    dst = os.path.join(userdata, "%s.bak.%d" % (name, i))
                    if os.path.exists(dst):
                        continue
                    shutil.move(src, dst)
                    #successfully renamed
                    break
                    
def write_keymap(keymap, filename):
    contexts = list(set([c for c, a, k in keymap]))
    builder = ET.TreeBuilder()
    builder.start("keymap", {})
    for context in contexts:
        builder.start(context, {})
        builder.start("keyboard", {})
        for c, a, k in keymap:
            if c == context:
                builder.start("key", {"id":k})
                builder.data(a)
                builder.end("key")
        builder.end("keyboard")
        builder.end(context)
    builder.end("keymap")
    element = builder.close()
    ET.ElementTree(element).write(filename, 'utf-8')
