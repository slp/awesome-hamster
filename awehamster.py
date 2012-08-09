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
        facts = self.ifaceHamster.GetFacts(0,0,"")

        if len(facts) > 0:
            f = facts[-1]
            startTime = f[1]
            endTime = f[2]
            currentTime = calendar.timegm(time.localtime())
            elapsedTime = currentTime - startTime

        if startTime == 0 or endTime != 0:
            print "No activity"
            self.ifaceAwesome.Eval('mytextbox.text = \'<span color=\"white\">  No activity  </span>\'')
        else:
            minutes = elapsedTime / 60
            hours = minutes / 60
            minutes = minutes - (hours * 60)
            print "%s@%s %s:%s" % (f[4], f[6], self._pretty_format(hours), self._pretty_format(minutes))
            self.ifaceAwesome.Eval('mytextbox.text = \'<span color=\"white\">  %s@%s %s:%s  </span>\'' % (f[4], f[6], self._pretty_format(hours), self._pretty_format(minutes)))

        return True

    def run(self):
        gobject.timeout_add_seconds(60, self._refresh)
        self._refresh()
        loop = gobject.MainLoop()
        loop.run()


prueba = AwesomeHamster()
prueba.run()
