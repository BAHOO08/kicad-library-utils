# -*- coding: utf-8 -*-

from rules.rule import *
import re

class Rule(KLCRule):
    """
    Create the methods check and fix to use with the kicad lib files.
    """
    def __init__(self, component):
        super(Rule, self).__init__(component, 'Rule 3.5 - Pin orientation', 'Wherever possible, pins should be arranged by function')
        
    def checkGroundPins(self):
    
        GND = ['^[ad]*g(rou)*nd$']
        
        first = True
        
        for pin in self.component.pins:
            name = str(pin['name'].lower())
            for gnd in GND:
                if re.search(gnd, name, flags=re.IGNORECASE) is not None:
                    # Pin orientation should be "up"
                    if not pin['direction'] == 'U':
                        if first:
                            first = False
                            self.warning("Ground pins should be placed at bottom of symbol")
                        self.warning(" - Pin {name} ({num}) @ ({x}, {y})".format(
                            name = pin['name'],
                            num = pin['num'],
                            x = pin['posx'],
                            y = pin['posy']))
                           
    def checkPowerPins(self):
    
        PWR = ['^[ad]*v(aa|cc|dd|ss|bat|in)$']
    
        first = True
        
        for pin in self.component.pins:
            name = str(pin['name'].lower())
            for pwr in PWR:
                if re.search(pwr, name, flags=re.IGNORECASE) is not None:
                    # Pin orientation should be "down"
                    if not pin['direction'] == 'D':
                        if first:
                            first = False
                            self.warning("Power pins should be placed at top of symbol")
                        self.warning(" - Pin {name} ({num}) @ ({x}, {y})".format(
                            name = pin['name'],
                            num = pin['num'],
                            x = pin['posx'],
                            y = pin['posy']))

    def check(self):
        
        self.checkGroundPins()
        self.checkPowerPins()

        # No errors, only warnings
        return False

    def fix(self):
        """
        Proceeds the fixing of the rule, if possible.
        """
        self.info("Fixing not supported")
