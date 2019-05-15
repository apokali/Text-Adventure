import check

class Thing:
    '''Fields: id (Nat),
               name (Str),
               description (Str)
    '''
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        
    def __repr__(self):
        return '<thing #{0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        
class Player:
    '''Fields: id (Nat),
               name (Str), 
               description (Str),
               location (Room),
               inventory ((listof Thing))
    '''
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        self.location = None
        self.inventory = []
        
    def __repr__(self):
        return '<player #{0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        if len(self.inventory) != 0:
            print('Carrying: {0}.'.format(
                ', '.join(map(lambda x: x.name,self.inventory))))
 
class Room:
    '''Fields: id (Nat),
               name (Str), 
               description (Str),
               contents ((listof Thing)),
               exits ((listof Exit))
    '''    
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        self.contents = []
        self.exits = []
        
    def __repr__(self):
        return '<room {0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        if len(self.contents) != 0:
            print('Contents: {0}.'.format(
                ', '.join(map(lambda x: x.name, self.contents))))
        if len(self.exits) != 0:
            print('Exits: {0}.'.format(
                ', '.join(map(lambda x: x.name, self.exits)))) 
 
class Exit:
    '''Fields: name (Str), 
               destination (Room)
               key (Thing)
               message (Str)
    '''       
    
    def __init__(self,name,dest):
        self.name = name
        self.destination = dest
        self.key = None
        self.message = ''
        
    def __repr__(self):
        return '<exit {0}>'.format(self.name)

class World:
    '''Fields: rooms ((listof Room)), 
               player (Player)
    '''       
    
    msg_look_fail= "You don't see that here."
    msg_no_inventory = "You aren't carrying anything."
    msg_take_succ = "Taken."
    msg_take_fail = "You can't take that."
    msg_drop_succ = "Dropped."
    msg_drop_fail = "You aren't carrying that."
    msg_go_fail = "You can't go that way."
    
    msg_quit = "Goodbye."
    msg_verb_fail = "I don't understand that."
    
    def __init__(self, rooms, player):
        self.rooms = rooms
        self.player = player

    def look(self, noun):
        '''
        prints the name and description of the passed-in noun
        or prints the error message otherwise, given the World self
        Effect:
        * Two strings are printed or one string is printed
        
        look: World Str -> None
        requires: when there is a match, it is always unique
        '''
        list_of_inventory = self.player.inventory
        list_of_contents = self.player.location.contents
        if noun == 'me':
            self.player.look()
        elif noun == 'here':
            self.player.location.look()
        elif noun in list(map(lambda x: x.name,list_of_inventory)):
            i = 0
            while i < len(list_of_inventory):
                if list_of_inventory[i].name == noun:
                    list_of_inventory[i].look()
                i = i + 1
        elif noun in list(map(lambda x: x.name,list_of_contents)):
            i = 0
            while i < len(list_of_contents):
                if list_of_contentss[i].name == noun:
                    list_of_contents[i].look()
                i = i + 1
        else:
            print(self.msg_look_fail)
            
    def inventory(self):
        '''
        prints a formatted list of names of things that the player
        is currently carrying or prints the error message if the player's
        inventory is empty
        Effect: 
        * one string is printed
        
        inventory: World -> None
        '''
        
        if self.player.inventory != []:
            i = 0
            msg = "Inventory: "
            while i < len(self.player.inventory):
                msg = msg +self.player.inventory[i].name + ", "
                i = i +1
            msg = msg[:len(msg)-2]
            print(msg)
        else:
            print(self.msg_no_inventory)
            
    def take(self, noun):
        '''
        mutates the self.player.inventory and player's current room's content
        if the noun corrsponds to a thing in the player's 
        current room and prints "Taken." or prints error message otherwise.
        Effects:
        * self.player.inventory and self.player.location.contents are
        mutated and one string is printed
        or one string is printed
        
        take: World Str -> None
        '''
        list_of_contents = self.player.location.contents
        if noun in list(map(lambda x: x.name,list_of_contents)):
            i = 0
            while i < len(list_of_contents):
                if list_of_contents[i].name == noun:
                    self.player.inventory.append(list_of_contents[i])
                    self.player.location.contents.pop(i)
                    print(self.msg_take_succ)
                i = i +1
        else:
            print(self.msg_take_fail)
                                  
    def drop(self, noun):
        '''
        mutates the self.player.inventory and the player's current room
        if the noun corresponds to a thing in the player's inventory and 
        prints "Dropped." or prints the error message otherwise
        Effects:
        * self.player.inventory and self.player.location.contents are
        mutated and one string is printed
        or one string is printed
        
        drop: World Str -> None
        '''
        list_of_contents = self.player.inventory
        if noun in list(map(lambda x: x.name,list_of_contents)):
            i = 0
            while i < len(list_of_contents):
                if noun == list_of_contents[i].name:
                    self.player.location.contents.append(list_of_contents[i])
                    self.player.inventory.pop(i)
                    print(self.msg_drop_succ)
                i = i + 1
        else:
            print(self.msg_drop_fail)
                        
        
    def go(self, noun):
        '''
        mutates the contents of self so that the player moves to the room
        at the other end of that exit if noun corresponds to the name 
        of one of the exits in the player's current room
        or prints error message otherwise
        Effect:
        * the content of self.player.location is mutated 
        or one string is printed
        
        go: World Str -> None
        '''
        list_of_exits = self.player.location.exits
        if noun in list(map(lambda x: x.name,list_of_exits)):
            i = 0
            while i < len(list_of_exits):
                if list_of_exits[i].name == noun:
                    if list_of_exits[i].key == None or\
                       list_of_exits[i].key in self.player.inventory:
                        self.player.location = list_of_exits[i].destination
                        list_of_exits[i].destination.look()
                    else:
                        print(list_of_exits[i].message)
                i = i + 1
        else:
            print(self.msg_go_fail)
                
    def play(self):
        player = self.player
        
        player.location.look()
        
        while True:
            line = input( "- " )
            
            wds = line.split()
            verb = wds[0]
            noun = ' '.join( wds[1:] )
            
            if verb == 'quit':
                print( self.msg_quit )
                return
            elif verb == 'look':
                if len(noun) > 0:
                    self.look(noun)  
                else:
                    self.look('here')
            elif verb == 'inventory':
                self.inventory()     
            elif verb == 'take':
                self.take(noun)    
            elif verb == 'drop':
                self.drop(noun)
            elif verb == 'go':
                self.go(noun)   
            else:
                print(self.msg_verb_fail)

    ## Q3
    def save(self, fname):
        '''
        writes the world self to a file called fname
        Effetc: writes the file called fname
        
        save: World Str -> None
        '''
        out_data = open(fname,"w")
        for thing in self.player.inventory:
            line1 = "thing #{0.id} {0.name}\n"
            out_data.write(line1.format(thing))
            line2 = thing.description + "\n" 
            out_data.write(line2)
        for room in self.rooms:
            if room.contents !=[]:
                for content in room.contents:
                    line1 = "thing #{0.id} {0.name}\n"
                    out_data.write(line1.format(content))
                    line2= content.description + "\n"
                    out_data.write(line2)
        for room in self.rooms:
            line1= "room #{0.id} {0.name}\n"
            out_data.write(line1.format(room))
            line2 = room.description +"\n"
            out_data.write(line2.format(room))
            line3 = "contents\n"
            if room.contents !=[]:
                continuing = list(map(lambda x: str(x.id), room.contents))
                line3 = "contents #" + " #".join(continuing) +"\n"
            out_data.write(line3)
        #player
        line1 = "player #{0.id} {0.name}\n"
        out_data.write(line1.format(self.player))
        line2 = self.player.description + "\n"
        out_data.write(line2)
        if self.player.inventory !=[]:
            continuing = list(map(lambda x: str(x.id), self.player.inventory))
            line3 = "inventory #" + " #".join(continuing) + "\n"
        out_data.write(line3)        
        line4 = self.player.location
        out_data.write("location #{0.id}\n".format(line4))
        #exits
        for room in self.rooms:
            if room.exits !=[]:
                for exit in room.exits:
                    if exit.key == None:
                        line1 ="exit #{0.id} #{1.destination.id} {1.name}\n"
                        out_data.write(line1.format(room,exit))
                    else:
                        line1 = "keyexit #{0.id} #{1.destination.id} {1.name}\n"
                        out_data.write(line1.format(room,exit))
                        line2 = "#{0.key.id} {0.message}\n"
                        out_data.write(line2.format(exit))
        out_data.close()
        

## Q2
def find(lst,identity):
    '''
    returns Thing in the lst given the name of a Thing's name
    
    find: (anyof (listof Thing) (listof Room) Str -> (anyof Thing Room)
    '''
    i = 0
    while i < len(lst):
        if lst[i].id == int(identity):
            return lst[i]
        i = i + 1
    
    
def load(fname):
    '''
    opens the file fname, reads eac lines
    returns a World constructed from the information in the text file
    given the name of the text file to read from
    Effects: Reads the file called fname
    
    load: Str -> World
    '''
    data = open(fname,"r")
    next_line = data.readline().split()
    list_of_things = []
    list_of_rooms = []
    while next_line != []:
        if next_line[0] == 'thing':
            curr = Thing(int(next_line[1][1:]))
            los = next_line[2:]
            curr.name = " ".join(los) 
            next_line = data.readline()
            curr.description = next_line[:len(next_line)-1]
            list_of_things.append(curr)
        elif next_line[0] == "room":
            curr = Room(int(next_line[1][1:]))
            los = next_line[2:]
            curr.name = " ".join(los)
            next_line = data.readline()
            curr.description = next_line[:len(next_line)-1]
            next_line = data.readline().split()[1:]
            for i in next_line:
                item = find(list_of_things,i[1:])
                curr.contents.append(item)
            list_of_rooms.append(curr)
        elif next_line[0] == "player":
            player = Player(int(next_line[1][1:]))
            los = next_line[2:]
            player.name = " ".join(los)
            next_line = data.readline()
            player.description = next_line[:len(next_line)-1]
            next_line = data.readline().split()[1:]
            for i in next_line:
                player.inventory.append(find(list_of_things,i[1:]))
            next_line = data.readline().split()[1:]
            for i in next_line:
                player.location = find(list_of_rooms,i[1:])
        else:
            los = next_line[3:]
            name = " ".join(los)
            room_has_exit = find(list_of_rooms,next_line[1][1:])
            exit_leads_to = find(list_of_rooms,next_line[2][1:])
            ex = Exit(name,exit_leads_to)
            if next_line[0] == "keyexit":
                next_line = data.readline().split()
                ex.key = find(list_of_things,next_line[0][1:])
                ex.message = " ".join(next_line[1:])
            room_has_exit.exits.append(ex)
   
        next_line = data.readline().split()
    return World(list_of_rooms, player)

     
    
def makeTestWorld(usekey):
    wallet = Thing(1)
    wallet.name = 'wallet'
    wallet.description = 'A black leather wallet containing a WatCard.'
    
    keys = Thing(2)
    keys.name = 'keys'
    keys.description = 'A metal keyring holding a number of office and home keys.'
    
    phone = Thing(3)
    phone.name = 'phone'
    phone.description = 'A late-model smartphone in a Hello Kitty protective case.'
    
    coffee = Thing(4)
    coffee.name = 'cup of coffee'
    coffee.description = 'A steaming cup of black coffee.'
    
    hallway = Room(5)
    hallway.name = 'Hallway'
    hallway.description = 'You are in the hallway of a university building. \
Students are coming and going every which way.'
    
    c_and_d = Room(6)
    c_and_d.name = 'Coffee Shop'
    c_and_d.description = 'You are in the student-run coffee shop. Your mouth \
waters as you scan the room, seeing many fine foodstuffs available for purchase.'
    
    classroom = Room(7)
    classroom.name = 'Classroom'
    classroom.description = 'You are in a nondescript university classroom. \
Students sit in rows at tables, pointedly ignoring the professor, who\'s \
shouting and waving his arms about at the front of the room.'
    
    player = Player(8)
    player.name = 'Stu Dent'
    player.description = 'Stu Dent is an undergraduate Math student at the \
University of Waterloo, who is excelling at this studies despite the fact that \
his name is a terrible pun.'
    
    c_and_d.contents.append(coffee)
    player.inventory.extend([wallet,keys,phone])
    player.location = hallway
    
    hallway.exits.append(Exit('shop', c_and_d))
    ex = Exit('west', classroom)
    if usekey:
        ex.key = coffee
        ex.message = 'On second thought, it might be better to grab a \
cup of coffee before heading to class.'
    hallway.exits.append(ex)
    c_and_d.exits.append(Exit('hall', hallway))
    classroom.exits.append(Exit('hall', hallway))
    
    return World([hallway,c_and_d,classroom], player)

testworld = makeTestWorld(False)
testworld_key = makeTestWorld(True)



check.set_file_exact("why.txt","123.txt")          
check.expect("t1", load("why.txt").save("123.txt"),None)

a =load("testworld_key.txt")