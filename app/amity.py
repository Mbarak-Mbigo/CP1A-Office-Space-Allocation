"""Amity main module.

app/amity.py

"""
# imports
from random import choice
import os

# local imports
from app.room import Office, Living
from app.person import Staff, Fellow


class Amity(object):
    """Docstring for Amity."""

    rooms = {
        'offices': {},
        'livingspaces': {}
    }

    persons = {
        'staff': {},
        'fellows': {}
    }

    def create_room(self, rooms, room_type='OFFICE'):
        """Create room(s).

        create_room <room_name>... - Creates rooms in Amity.
        Using this command I should be able to create as
        many rooms as possible by specifying multiple room
         names after the create_room command.
        Args:
            type: type of room (office|living).
            rooms: A list of room names (any string)
        Returns:
            Room(s) created.
        Raises:
            TypeError: if rooms not a list.
            ValueError: if rooms not strings
            ValueError: if room_type type not in (office| living).
        """
        try:
            # check room type within domain
            if room_type not in ["office", "living", "OFFICE", "LIVING"]:
                raise ValueError("Invalid room type, should be office or\
                 living")
            # check room names given as a list
            elif not isinstance(rooms, list):
                print(rooms)
                raise TypeError("Provide a list of room name(s)")
            # check room names are strings
            elif len(rooms) == 0 or not all(isinstance(x, str) for x in rooms):
                raise ValueError("Invalid room name, only strings accepted")

        except (ValueError, TypeError) as e:
            return e
        else:

            return self.add_room(rooms, room_type)

    def add_room(self, rooms, room_type):
        """Create and add room(s) to Amity."""
        status = []
        if room_type.upper() == "OFFICE":
            for room in rooms:
                if room not in self.rooms['offices'].keys():
                    self.rooms['offices'][room] = Office(room.title())
                else:
                    status.append(room.title())
            if len(status) == 0:
                return 'Room(s) ' + ', '.join(rooms) + ' Created successfully'
            else:
                return 'Rooms(s) ' + ', '.join(status) + ' already exists'
        else:
            for room in rooms:
                if room not in self.rooms['livingspaces'].keys():
                    self.rooms['livingspaces'][room] = Living(room.title())
                else:
                    status.append(room.title())
            if len(status) == 0:
                return 'Room(s) ' + ', '.join(rooms) + ' Created successfully'
            else:
                return 'Rooms(s) ' + ', '.join(status) + ' already exists'

    def add_person(self, name, type='FELLOW', accommodation='N'):
        """Create a person, add to system, allocate to random room.

        add_person <person_name> <FELLOW|STAFF> [wants_accommodation] -
        Adds a person to the system and allocates the person to a random room.
        wants_accommodation here is an optional argument which can be
        either Y or N.
        The default value if it is not provided is N.
        Args:
            name: person name (string)
            type: person type (FELLOW | STAFF)
            wants_accommodation: ('Y' | 'N')
        Returns:
            Name of person added
        Raises:
            ValueError: if name not string
            ValueError: if type not in specified domain
            ValueError: if wants_accommodation not in specified domain
            PermissonError: if type is STAFF and wants_accommodation is 'Y'
        """
        try:
            # name given not string
            if not isinstance(name, str):
                raise ValueError('Person name can only be a string')
            # person already exists
            elif name in (self.persons['staff'].keys()) or name in\
                    (self.persons['fellows'].keys()):
                raise ValueError('Person: {0} already exists'.format(name))
            # person type not in domain
            elif type not in ['staff', 'fellow', 'STAFF', 'FELLOW']:
                raise ValueError('Person type can either be STAFF or FELLOW')
            # accommodation not within specified domain
            elif accommodation not in ['y', 'Y', 'n', 'N']:
                raise ValueError("Accommodation can either be 'Y' or 'N' ")
            # staff wants accommodation
            elif type in ['staff', 'STAFF'] and accommodation in\
                    ['y', 'Y']:
                raise PermissionError("Staff cannot request for accommodation")
        except (ValueError, PermissionError) as e:
            return e
        else:
            # create person
            if type.upper() == 'STAFF':
                self.persons['staff'][name] = Staff(name)
            else:
                self.persons['fellows'][name] = Fellow(name, accommodation)
            # allocate room

            return self.allocate_room(name, type)

    def reallocate_person(self, person_id, new_room_name):
        """Reallocate a person from one room to another.

        reallocate_person <person_identifier> <new_room_name> -
        Reallocate the person with person_identifier to new_room_name.

        Args:
            person_id: a valid person id
            new_room_name: a valid room

        Returns:
            Reallocation status
        """
        try:
            current_room = None
            # get new room
            all_rooms = dict(self.rooms['offices'], **self.rooms['livingspaces'])
            reallocate_room = all_rooms.get(new_room_name)
            # get person
            all_pple = dict(self.persons['staff'], **self.persons['fellows'])
            person = next((p for p in list(all_pple.values()) if p.id ==
                           person_id), None)
            # room to reallocate not found
            if not reallocate_room:
                raise ValueError('No room {0} in the system'.format(new_room_name))
            # person not found
            if not person:
                raise ValueError('No person with id {0}'.format(person_id))

        except ValueError as e:
            return e

        else:
            if reallocate_room.type == 'LIVING' and person.type == 'STAFF':
                return "Cannot reallocate staff to living space"

            if reallocate_room.type == 'OFFICE' and not person.office_space:
                return "Allocate office space before reallocating"
            else:
                current_room = self.rooms['offices'][person.office_space]
                current_room.occupants.remove(person.name)
                reallocate_room.occupants.append(person.name)
                person.office_space = (reallocate_room.name)
                return "Reallocation of office space successful."

            if reallocate_room.type == 'LIVING' and not person.living_space:
                return "Allocate living space before reallocating"
            else:
                current_room = self.rooms['livingspaces'][person.living_space]
                current_room.occupants.remove(person.name)
                reallocate_room.occupants.append(person.name)
                person.living_space = reallocate_room.name
                return "Reallocation of living space successful."

    def load_people(self, filename="data/load.txt"):
        """"Add people to rooms from a txt file.

        filename: txt file  values: person names and details
        Scenario:
            File does not exist
                raise exception file not exist
            File Exists
                file type not txt
                    raise exception
                file type txt
                    No data
                        Raise exception
                    Data exists
                            Unkown format
                                raise exception
                            data format okay
                                perform load operation

        """
        try:
            if not os.path.exists("data/load.txt"):
                raise FileNotFoundError("Loading file not found")
            elif os.stat("data/load.txt").st_size == 0:
                return "File is empty"

        except FileNotFoundError as e:
            return e
        else:
            with open("data/load.txt") as f:
                for line in f:
                    line = line.strip()
                    person_details = line.split(' ')
                    name = person_details[0] + ' ' + person_details[1]
                    person_type = person_details[2]
                    if person_details[-1] == "Y":
                        self.add_person(name, person_type, person_details[-1])
                    else:
                        self.add_person(name, person_type)
                return "Loading operation successful"

    def print_allocations(self, outfile=None):
        """"Print to the screen a list of rooms and the people allocated.

        if outfile provided output list to the file  as well
        Scenario:
        No rooms or rooms available but no allocations yet
            raise exception
        Rooms available allocations okay
            outfile provided
                print to screen and file
            outfile not provided
                print to screen

        """
        try:
            if not any(self.rooms):
                raise ValueError("No rooms available")
            else:
                occupied_offices = [o for o in list(self.rooms['offices'].values()) if len(o.occupants) > 0]
                if len(occupied_offices) == 0:
                    print("There are no office allocations")
                occupied_living = [l for l in list(self.rooms['livingspaces'].values()) if len(o.occupants) > 0]
                if len(occupied_living) == 0:
                    print("There are no living space allocations")

        except ValueError as e:
            return e
        else:
            if outfile:
                with open(outfile, "w") as f:
                    for room in (occupied_offices + occupied_living):
                        f.write(room.name + '\n')
                        f.write(", ".join(room.occupants))
                        f.write('\n')
            print("ALLOCATIONS")
            for room in (occupied_offices + occupied_living):
                print("Room: {0}".format(room.name))
                print("--------------------------------")
                print(", ".join(room.occupants))
                print("\n")

    def print_unallocated(self, outfile=None):
        """"
        print a list of all unallocated people on the screen
        if outfile is provided, output the list to the file

        Scenario:
        No person
            respond accordingly
        People available
            No one unallocated
                handle accordingly
            office
                fellows
                staff
            living
                fellows

        outfile provided
            output to file too.
        """
        try:
            unallocated = None
            if not any(self.persons):
                raise ValueError("No people in the system")

        except ValueError as e:
            raise
        else:
            all_persons = list(self.persons['staff'].values()) + list(self.persons['fellows'].values())
            unallocated_office = [p for p in all_persons if p.office_space == None]
            unallocated_living = [l for l in list(self.rooms['livingspaces'].values()) if l.living_space is not None ]
            if outfile:
                with open(outfile, 'w') as f:
                    if len(unallocated_office) > 0:
                        f.write("UNALLOCATED OFFICE SPACE \n")
                        for person in unallocated_office:
                            f.write(str(person))
                            f.write('\n')
                    if len(unallocated_living) > 0:
                        f.write("UNALLOCATED LIVING SPACE \n")
                        for person in unallocated_living:
                            f.write(str(person))
                            f.write('\n')

            print("UNALLOCATED OFFICE SPACE")
            print("-----------------------------------")
            for person in unallocated_office:
                print(person)
            print("\nUNALLOCATED LIVING SPACE")
            print("-----------------------------------")
            for person in unallocated_living:
                print(person)

    def print_room(self, room_name):
        """"Given a room name, print all the people allocated to that room.

        Scenarios:
        room not in pool
            raise exception
        room in pool
            no allocations
                handle accordingly
            allocations available
                display allocations
        """
        try:
            all_rooms = dict(self.rooms['offices'], **self.rooms['livingspaces'])
            if not all_rooms.get(room_name):
                raise ValueError("No room with name: {0}".format(room_name))
        except ValueError as e:
            return
        else:
            room = all_rooms[room_name]
            print(room.occupants)

    # def save_state(self, database="default-db"):
    #     """"Persists all that in the application onto an
    #         SQLite database"""
    #     pass

    # def load_state(self, database=None):
    #     """"Loads data from the provided database into the
    #     application for use
    #     Scenarios:
    #     db provided does not exist
    #         raise exception
    #     db exists
    #         no data
    #             raise exception
    #         data exists
    #             unkown format
    #                 raise exception
    #             known format
    #                 load data
    #                     unsuccessful
    #                         raise error
    #                     successful
    #                         load data
    #     """
    #     pass

    # #added functionality
    # def print_available_space(self):
    #     """
    #     print all rooms and spaces available on each room (unallocated space)
    #     args: None
    #     Returns: un allocated space
    #     Raise:
    #         ValueError: if no room space available

    #     """
    #     try:
    #         if len(self.all_rooms) == 0:
    #             raise ValueError("No room space available")

    #     except ValueError as e:
    #         return e
    #     else:
    #         office_space = [room for room in self.all_rooms if room.type == "office"]
    #         living_space = [room for room in self.all_rooms if room.type == "living"]
    #         print("AVAILABLE ROOMS:")
    #         for room in office_space:
    #            print(room)
    #         for room in living_space:
    #             print(room)
    #     finally:
    #         pass

    # # Helper functions

    def allocate_room(self, name, type):
        """"Allocate room to person."""
        # get person
        if type.upper() == 'STAFF':
            person = self.persons['staff'][name]
        else:
            person = self.persons['fellows'][name]

        # get office room
        room_key = self.get_random_room('office')
        if room_key:
            room = self.rooms['offices'][room_key]
            if room:
                # room capacity not exceeded
                if not room.is_full():
                    person.office_space = room_key
                    room.occupants.append(person.name)

        # get living room
        if person.type == 'FELLOW' and person.accommodation == 'Y':
            room_key = self.get_random_room('living')
            if room_key:
                room = self.rooms['livingspaces'][room_key]
                if room:
                    # living room capacity not exceeded
                    if not room.is_full():
                        person.living_space = room_key
                        room.occupants.append(person.name)

        if person.type == 'STAFF' and person.office_space:
            return "Office space allocated successfully"
        elif person.type == 'FELLOW' and person.office_space and person.living_space:
            return "Office and Living spaces allocated successfullly"
        elif person.type == 'FELLOW' and person.office_space and not person.living_space:
            return "Only office space allocated"
        elif person.type == 'FELLOW' and not person.office_space and not person.living_space:
            return "Person added but no rooms to allocate office or living space"
        elif person.type == 'FELLOW' and not person.office_space and person.living_space:
            return "Fellow assigned living space only, No office space available"
        elif person.type == 'STAFF' and not person.office_space:
            return "Could not allocate Office space"

    def get_random_room(self, type, current_room=None):
        """Return a room name or None."""
        try:
            # room type not  in domain
            if type not in ['office', 'living', 'OFFICE', 'LIVING']:
                raise ValueError("Room type can only be office or living")
            # room name not string
            elif not isinstance(current_room, str) and\
                    current_room is not None:
                raise ValueError("Room name must be a string")
        except ValueError as e:
            return e
        else:
            # check if there are rooms
            rooms = None
            if type.upper() == 'OFFICE':
                if not any(self.rooms['offices']):
                    return None
                else:
                    rooms = list(self.rooms['offices'].keys())
                    if current_room:
                        rooms.remove(current_room)
                    return choice(rooms)
            else:
                if not any(self.rooms['livingspaces']):
                    return None
                else:
                    rooms = list(self.rooms['livingspaces'].keys())
                    if current_room:
                        rooms.remove(current_room)
                    return choice(rooms)
