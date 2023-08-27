## Lua Scripting API Documentation

### globals

> modules:
>* math (py)

> objects:
> level (object)
> api (object)
> 
> 

#### API Object
> artibutes:
> * Player:Player
> * Objects:Objects
> * level:Level
> * Version:string
> * uuidTo_EL_ID:dict
> 

> ### The Player object
> The Player Object
> 
> <br>methods:
> * `getPlayer()` returns player position (x,y)
> * `setPlayer(x,y)` sets players absolute position
> * `movePlayer(x,y)` moves player x,y to the relative position


> ### The Objects object
> The Objects is the handler class fore all non player objects in the game object
> <br>methods:
> * `setObject(uuid,x,y)` sets absolute position ot the object
> * `moveObject(uuid,x,y)` moves the object around the relative position




### UUID's and ID's
> the `UUID` is the absolute identifier fo the object it will **stay the same in any session**
> the `ID` in comparison is **only valid for one session it will change** and is only bound to the currant identification in the engen
> the id is only used inside the engine its recommend to not bound any functions on the id and use the uuid instead
> 
