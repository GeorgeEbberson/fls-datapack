FLS Datapack Generator
======================
A thrown-together bit of code which generates one datapack (rather than several
haphazard ones that we previously had) for the FLS Minecraft server (IYKYK).

Features
--------
* **Universal Dyeing.** Whilst Vanilla Tweaks implements universal dyeing (and,
  to be clear, this implementation is very heavily based on their version), this
  pack builds upon that to include two extra changes: wool can be dyed 1:8 like
  other materials,and concrete can be dyed just like concrete powder.
* **Honeycomb Storage.** To make honeycomb blocks useful as a storage block,
  breaking them will yield honeycomb rather than honeycomb blocks. Silk Touch
  still works as normal so you can still get honeycomb back if you want.

Development
-----------
Tested in Python 3.11 but should work in most Python 3 versions. Has no
dependencies outside the standard library so I haven't worried about a virtual
environment at this time.

To regenerate the pack, run `python -m build_pack` which will generate the
`output` folder. `output` will contain the `.zip` datapack (as well as the
uncompressed files to aid development).

Testing
-------
A list of things that should be tested before "releasing" (in the loosest sense
of the word). Should be run on the same version of Minceraft as the server.
* Redye items of mixed colours, should get 8 items of the desired colour
* Redye wool, should work at 1:8 ratio
* Redye concrete, should work
* Redye an item to black, should work (checks tagged dyes work)
* Revoke all advancements and recipes, give yourself 8+ wool and a dye, you
  should get all wool redye recipes (checks advancements are working)
* Break a honeycomb block with an unenchanted tool, should get 2-4 honeycomb
* Break a honeycomb block with silk touch, should get a honeycomb block
