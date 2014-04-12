#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import dbus, dbus.mainloop.glib
import gobject
import time
import calendar

class AwesomeHamster(gobject.GObject):
    def __init__(self):
        gobject.GObject.__init__(self)

        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.bus = dbus.SessionBus()
        self.bus.add_signal_receiver(self._on_facts_changed, 'FactsChanged', 'org.gnome.Hamster')

        proxyHamster = self.bus.get_object('org.gnome.Hamster', '/org/gnome/Hamster')
        proxyAwesome = self.bus.get_object('org.naquadah.awesome.awful', '/')

        self.ifaceHamster = dbus.Interface(proxyHamster, 'org.gnome.Hamster')
        self.ifaceAwesome = dbus.Interface(proxyAwesome, 'org.naquadah.awesome.awful.Remote')


    def _pretty_format(self, number):
        if number < 10:
            return "0" + str(number)
        else:
            return str(number)

    def _on_facts_changed(self):
        self._refresh()

    def _refresh(self):
        startTime = 0
        facts = self.ifaceHamster.GetTodaysFacts()

        if len(facts) > 0:
            f = facts[-1]
            startTime = f[1]
            endTime = f[2]
            currentTime = calendar.timegm(time.localtime())
            elapsedTime = currentTime - startTime

        if startTime == 0 or endTime != 0:
            print "No activity"
            self.ifaceAwesome.Eval('myawehamsterbox:set_text("No activity")')
        else:
            minutes = elapsedTime / 60
            hours = minutes / 60
            minutes = minutes - (hours * 60)
            activity = (f[4]).encode("utf-8")
            category = (f[6]).encode("utf-8")
            print "%s@%s %s:%s" % (activity, category, self._pretty_format(hours), self._pretty_format(minutes))
            self.ifaceAwesome.Eval('myawehamsterbox:set_text("%s@%s %s:%s")' % (activity, category, self._pretty_format(hours), self._pretty_format(minutes)))

        return True

    def run(self):
        gobject.timeout_add_seconds(60, self._refresh)
        self._refresh()
        loop = gobject.MainLoop()
        loop.run()


awehamster = AwesomeHamster()
awehamster.run()
