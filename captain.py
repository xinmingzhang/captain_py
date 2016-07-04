from __future__ import division
from random import choice
from itertools import cycle



import pygame as pg


        
class Captain(object):
    def __init__(self, world_info, ship_info, distances):
        self.world = world_info

        self.all_planets = [name for name in world_info]
        self.home = [name for name in world_info if world_info[name]['resource'] == 'Food'][0]
        self.uranium_mine = [name for name in world_info if world_info[name]['resource'] == 'Uranium'][0]
        self.plastic_mine = [name for name in world_info if world_info[name]['resource'] == 'Plastic'][0]
        self.aluminum_mine = [name for name in world_info if world_info[name]['resource'] == 'Aluminum'][0]
        self.titanium_mine = [name for name in world_info if world_info[name]['resource'] == 'Titanium'][0]
        self.gold_mine = [name for name in world_info if world_info[name]['resource'] == 'Gold'][0]

        self.resource = ['Uranium','Plastic','Aluminum','Titanium','Gold']
        self.route = [self.home,self.uranium_mine,self.plastic_mine,self.aluminum_mine,self.titanium_mine,self.gold_mine]

        self.aim_num = 0
        self.destination = self.route[self.aim_num]

        self.food_num = 0
        self.uranium_num = 0
        self.plastic_num = 0
        self.aluminum_num = 0
        self.titanium_num = 0
        self.gold_num = 0

        self.colonist_num = 0

    def stop_sim(self):
        key_event = pg.event.Event(pg.KEYUP, key = pg.K_SPACE)
        pg.event.post(key_event)

    def check_result(self):
        if sum((self.world[name]['inventory']['Aluminum'] for name in self.world)) < 100000.0:
            return False
        else:
            return True

    def caculus_ratio(self, resource_name,planet):
        resource_planet = [name for name in self.world if self.world[name]['resource'] == resource_name][0]
        if (resource_planet in self.route) and (planet in self.route):
            a = self.route.index(planet)-self.route.index(resource_planet)
            if a < 0:
                return -a/len(self.route)
            elif a >= 0:
                return (len(self.route)-a)/len(self.route)
        else:
            return 0
            

    def get_orders(self, world_info, ship_info, distances):
        """
        Choose cargo, passengers and destination
        for next trip. This method is called once each day
        while the ship is docked on a planet.
        
        Method should return a dict with the following key, value pairs:
        
        "destination": the name of the planet to travel to
        "cargo": a dict of what cargo should be brought on board
        "colonists": the number of colonists to deliver to the next planet
        
        Parameters
        *********
        world_info: a dict of dicts keyed by planet name
                        each planet

        ship_info: a dict of information about the transport ship

        distances: a dict of distances between each planet        
        """

        self.world = world_info
        if self.check_result():
            self.stop_sim()
            orders = {
                "destination": None,
                "cargo": {},
                "colonists": 60}


        elif ship_info['pos'] == world_info[self.home]['pos']:
            self.aim_num = (self.aim_num + 1) % len(self.route)
            self.destination = self.route[self.aim_num % len(self.route)]
            self.food_num = world_info[self.home]['inventory']['Food']*(len(self.route)-1)/len(self.route)
            self.colonist_num = 0

            if world_info[self.gold_mine]['num_colonists'] == 0 and world_info[self.titanium_mine]['num_colonists'] == 0:
                self.colonist_num = world_info[self.home]['num_colonists']
                self.route.remove(self.home)
                orders = {
                    "destination":self.destination,
                    "cargo":world_info[self.home]['inventory'],
                    "colonists":self.colonist_num}

            elif sum((world_info[name]['inventory']['Gold'] for name in self.all_planets)) > 90000:
                self.colonist_num = world_info[self.home]['num_colonists'] - 9
                orders = {
                    "destination":self.destination,
                    "cargo": {'Food':self.food_num,
                              'Uranium':self.uranium_num *self.caculus_ratio('Uranium',self.home),
                              'Plastic':self.plastic_num *self.caculus_ratio('Plastic',self.home),
                              'Aluminum':self.aluminum_num *self.caculus_ratio('Aluminum',self.home),
                              'Titanium':self.titanium_num *self.caculus_ratio('Titanium',self.home),
                              'Gold':self.gold_num *self.caculus_ratio('Gold',self.home)},
                    "colonists":self.colonist_num}

            else:
                orders = {
                    "destination":self.destination,
                    "cargo": {'Food':self.food_num,
                              'Uranium':self.uranium_num *self.caculus_ratio('Uranium',self.home),
                              'Plastic':self.plastic_num *self.caculus_ratio('Plastic',self.home),
                              'Aluminum':self.aluminum_num *self.caculus_ratio('Aluminum',self.home),
                              'Titanium':self.titanium_num *self.caculus_ratio('Titanium',self.home),
                              'Gold':self.gold_num *self.caculus_ratio('Gold',self.home)},
                    "colonists":self.colonist_num}
                
                

        elif ship_info['pos'] == world_info[self.uranium_mine]['pos']:
            self.aim_num = (self.aim_num + 1) % len(self.route)
            self.destination = self.route[self.aim_num % len(self.route)]
            self.uranium_num = world_info[self.uranium_mine]['inventory']['Uranium']*(len(self.route)-1)/len(self.route)
            self.colonist_num = 0
            if sum((world_info[name]['inventory']['Uranium'] for name in self.all_planets)) > 104000:
                self.colonist_num = world_info[self.uranium_mine]['num_colonists']
                self.uranium_num = 0
                self.route.remove(self.uranium_mine)

            orders = {
                "destination":self.destination,
                "cargo": {'Food':self.food_num * self.caculus_ratio('Food',self.uranium_mine) ,
                          'Uranium':self.uranium_num,
                          'Plastic':self.plastic_num *self.caculus_ratio('Plastic',self.uranium_mine),
                          'Aluminum':self.aluminum_num *self.caculus_ratio('Aluminum',self.uranium_mine),
                          'Titanium':self.titanium_num *self.caculus_ratio('Titanium',self.uranium_mine),
                          'Gold':self.gold_num *self.caculus_ratio('Gold',self.uranium_mine)} \
                    if self.colonist_num == 0 else world_info[self.uranium_mine]['inventory'],
                "colonists":self.colonist_num}

        elif ship_info['pos'] == world_info[self.plastic_mine]['pos']:
            try:
                self.aim_num = (self.aim_num + 1) % len(self.route)
                self.destination = self.route[self.aim_num % len(self.route)]
            except:
                self.destination = None
            self.plastic_num = world_info[self.plastic_mine]['inventory']['Plastic']*(len(self.route)-1)/len(self.route)
            self.colonist_num = 0
            if sum((world_info[name]['inventory']['Plastic'] for name in self.all_planets)) > 102000:
                self.colonist_num = world_info[self.plastic_mine]['num_colonists']
                self.plastic_num = 0
                self.route.remove(self.plastic_mine)


            orders = {
                "destination":self.destination,
                "cargo": {'Food':self.food_num * self.caculus_ratio('Food',self.plastic_mine),
                          'Uranium':self.uranium_num *self.caculus_ratio('Uranium',self.plastic_mine),
                          'Plastic':self.plastic_num,
                          'Aluminum':self.aluminum_num *self.caculus_ratio('Aluminum',self.plastic_mine),
                          'Titanium':self.titanium_num *self.caculus_ratio('Titanium',self.plastic_mine),
                          'Gold':self.gold_num *self.caculus_ratio('Gold',self.plastic_mine)}\
                    if self.colonist_num == 0 else world_info[self.plastic_mine]['inventory'],
                "colonists":self.colonist_num}

        elif ship_info['pos'] == world_info[self.aluminum_mine]['pos']:
            try:
                self.aim_num = (self.aim_num + 1) % len(self.route)
                self.destination = self.route[self.aim_num % len(self.route)]
                self.aluminum_num = world_info[self.aluminum_mine]['inventory']['Aluminum']*(len(self.route)-1)/len(self.route)
            except:
                self.destination = None
                self.aluminum_num = 0

            self.colonist_num = 0
            if sum((world_info[name]['inventory']['Aluminum'] for name in self.all_planets)) > 103000:
                self.colonist_num = world_info[self.aluminum_mine]['num_colonists']
                self.aluminum_num = 0
                self.route.remove(self.aluminum_mine)
            orders = {
                "destination":self.destination,
                "cargo": {'Food':self.food_num * self.caculus_ratio('Food',self.aluminum_mine),
                          'Uranium':self.uranium_num *self.caculus_ratio('Uranium',self.aluminum_mine),
                          'Plastic':self.plastic_num *self.caculus_ratio('Plastic',self.aluminum_mine),
                          'Aluminum':self.aluminum_num,
                          'Titanium':self.titanium_num *self.caculus_ratio('Titanium',self.aluminum_mine),
                          'Gold':self.gold_num *self.caculus_ratio('Gold',self.aluminum_mine)}\
                    if self.colonist_num == 0 else world_info[self.aluminum_mine]['inventory'],
                "colonists": self.colonist_num}

        elif ship_info['pos'] == world_info[self.titanium_mine]['pos']:
            self.aim_num = (self.aim_num + 1) % len(self.route)
            self.destination = self.route[self.aim_num % len(self.route)]
            self.titanium_num = world_info[self.titanium_mine]['inventory']['Titanium']*(len(self.route)-1)/len(self.route)
            self.colonist_num = 0
            if sum((world_info[name]['inventory']['Titanium'] for name in self.all_planets)) > 105000:
                self.colonist_num = world_info[self.titanium_mine]['num_colonists']
                self.route.remove(self.titanium_mine)
                self.titanium_num = 0
            orders = {
                "destination":self.destination,
                "cargo": {'Food':self.food_num * self.caculus_ratio('Food',self.titanium_mine),
                          'Uranium':self.uranium_num *self.caculus_ratio('Uranium',self.titanium_mine),
                          'Plastic':self.plastic_num *self.caculus_ratio('Plastic',self.titanium_mine),
                          'Aluminum':self.aluminum_num *self.caculus_ratio('Aluminum',self.titanium_mine),
                          'Titanium':self.titanium_num,
                          'Gold':self.gold_num *self.caculus_ratio('Gold',self.titanium_mine)}\
                    if self.colonist_num == 0 else world_info[self.titanium_mine]['inventory'],
                "colonists": self.colonist_num}

        elif ship_info['pos'] == world_info[self.gold_mine]['pos']:
            self.aim_num = (self.aim_num + 1) % len(self.route)
            self.destination = self.route[self.aim_num % len(self.route)]
            self.gold_num = world_info[self.gold_mine]['inventory']['Gold']*(len(self.route)-1)/len(self.route)
            self.colonist_num = 0
            if sum((world_info[name]['inventory']['Gold'] for name in self.all_planets)) > 106000:
                self.colonist_num = world_info[self.gold_mine]['num_colonists']
                self.gold_num = 0
                self.route.remove(self.gold_mine)

            orders = {
                "destination":self.destination,
                "cargo": {'Food':self.food_num * self.caculus_ratio('Food',self.gold_mine),
                          'Uranium':self.uranium_num *self.caculus_ratio('Uranium',self.gold_mine),
                          'Plastic':self.plastic_num *self.caculus_ratio('Plastic',self.gold_mine),
                          'Aluminum':self.aluminum_num *self.caculus_ratio('Aluminum',self.gold_mine),
                          'Titanium':self.titanium_num *self.caculus_ratio('Titanium',self.gold_mine),
                          'Gold':self.gold_num} \
                    if self.colonist_num == 0 else world_info[self.gold_mine]['inventory'],
                "colonists": self.colonist_num}
        return orders





