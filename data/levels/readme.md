Level description is a .csv format file which is written by the rules
below.

Level file name is the same as its order in game.

Level description starts with character name that it uses and it's coords:
#character#, #coord_x#, #coord_y#

There are 5 possible characters available for playing:
* Human (in file as hum) - no special abilities;
* Diavolo (in file as dia) - can vanish his existence for 5 seconds.
Events that should have happened to him are passing him instead, but
the result they do remains the same;
* Pucci (in file as puc) - can change gravity at will;
* Jonathan (in file as jon) - jumps 1.5x times higher than human, can take
up to three hits before dying
* Joseph (in file as jos) - can dash (highly increases speed for a small amount of time).


Coords are described with non-negative integers and mean coordinates of
cell that this block uses on plane.

Then level objects are described.

Objects in level files are described as:
#object type#, #coord_x#, #coord_y#

Object types use signatures.
What does every signature mean:
* b - Solid block;
* bc - Corner block;
* bs - Side block;
* bp - Pillar block;
* bcs - Point corner and side block;
* bcp - Point version of corner block;
* bl - Ledge block
* s - Spike;
* o - Orb

Signatures may have suffixes:
* _t - top;
* _b - bottom;
* _r - right;
* _l - left;
* _tr - top-right;
* _tl - top-left;
* _br - bottom-right;
* _bl - bottom-left

Suffixes specify which texture version of the block should be used.
For example, bc_tr means 'corner block with texture pointed at top-right'
Block signature is the same as its image name in '/images/textures' folder

If the cell is not specified, it left empty
