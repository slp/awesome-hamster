#!/usr/bin/env python2
import os
import dbus
import gtk

class AwesomeHamsterGui():
    def __init__(self):
        self.activitiesList = [ ]

        bus = dbus.SessionBus()

        proxyHamster = bus.get_object('org.gnome.Hamster', '/org/gnome/Hamster')
        self.ifaceHamster = dbus.Interface(proxyHamster, 'org.gnome.Hamster')

        activities = self.ifaceHamster.GetActivities('')

        for act in activities:
            if act[1] != '':
                self.activitiesList.append(act[0] + '@' + act[1])
            else:
                self.activitiesList.append(act[0])


    def _match_anywhere(self, completion, entrystr, iter, data):
        modelstr = completion.get_model()[iter][0]
        return entrystr in modelstr


    def _on_entry_activate(self, entry):
        text = entry.get_text()
        if text != '':
            self.ifaceHamster.AddFact(text, 0, 0, False)
            self.dialog.destroy()

    def run(self):
        listStore = gtk.ListStore(str)
        maxLen = 0
        for act in self.activitiesList:
            if len(act) > maxLen:
                maxLen = len(act)
            listStore.append([act])

        label = gtk.Label("New activity: ")
        hBox = gtk.HBox()

        entryCompletion = gtk.EntryCompletion()
        entryCompletion.set_model(listStore)
        entryCompletion.set_text_column(0)
        entryCompletion.set_match_func(self._match_anywhere, None)

        entry = gtk.Entry()
        entry.set_completion(entryCompletion)
        entry.set_width_chars(maxLen + 5)
        entry.connect("activate", self._on_entry_activate)

        self.dialog = gtk.Dialog("New activity",
                                 None,
                                 gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                 (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

        hBox.pack_start(label)
        hBox.pack_start(entry)
        self.dialog.vbox.pack_start(hBox)
        label.show()
        entry.show()
        hBox.show()
        self.dialog.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.dialog.run()

ahgui = AwesomeHamsterGui()
ahgui.run()
