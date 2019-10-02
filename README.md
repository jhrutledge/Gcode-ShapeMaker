# Gcode-ShapeMaker
Python GUI to build basic shapes and display cutting parameters.

README:
 Basics
 - input check, calculate kerf, build code, write file, define cutting parameters, popup result
 - always allow for touch at origin
 
 Rectangle
 - rectangle with corner that starts at origin and extends in specified dimensions
  X-width : final part x dimension
  Y-height : final part y dimension
  Material : for kerf and parameters
  Thickness : for kerf and parameters
  Amperage : for kerf and parameters
  Entry Cut : start pierce off of cut path to preserve part
  
 Circle
 - circle with edge on origin that extends in direction specified
  Diameter : final part diameter
  Direction : axis direction of part
  Material : for kerf and parameters
  Thickness : for kerf and parameters
  Amperage : for kerf and parameters
  Entry Cut : start pierce off of cut path to preserve part
 
 Donut
 - donut part with outer edge on origin that extends in direction and can offset center hole
  Outside Diameter : final part outer diameter
  Inside Diameter : final part inner hole diameter
  Direction : axis direction of part
  Offset : spacing from centerline to offset inner hole
  Material : for kerf and parameters
  Thickness : for kerf and parameters
  Amperage : for kerf and parameters
  Entry Cut : start pierce off of cut path to preserve part
 
 Line
 - simple line cut starting at origin
  Length : length of cut
  Direction : axis direction of cut
  Material : for kerf and parameters
  Thickness : for kerf and parameters
  Amperage : for kerf and parameters
  
 Class : rdmeTab
  Method : init
   - 
   - 
 
 Class : shapeTab
   - 
  Method : init
   - 
  Method : update_build
   - 
  Method : fileWrite
   - 
  Method : update_par
   - 
  Method : errorMsg
   - 
  Method : finalMsg
   - 
 
 Class : N/A
  Method : get_params
  Method : getKerf
  Method : middleRectangle
  Method : middleCircle
  Method : middleDonut
  Method : middleLine
  var : master
  var : tabControl
