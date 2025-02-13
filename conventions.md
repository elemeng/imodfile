This document is converted from IMOD official documentation and for coding reference using only. See [https://bio3d.colorado.edu/imod/betaDoc/binspec.html]

# Conventions
IMOD is a set of programs for analyzing, processing, and visualizing 3D images. 

# IMOD Binary File Format

The IMOD binary file format is similar to the IFF format standard in that it uses chunk IDs for data headings. Each chunk ID is 4 bytes long and is defined as a string of 4 characters. This is the format used by IMOD Version 2.0 and onward. All numbers are stored in big-endian format regardless of machine architecture. In the descriptions of flags below, bits are numbered from 0.

## The File Header

All binary model files begin with an 8-byte ID followed by a 232-byte header. The ID format begins with the IMOD file ID, `(IMOD = 0x494d4f44)`, followed by the 4-byte version ID, `(V1.2 = 0x56312e32)`. The end of the file is marked by an end-of-data marker, `(IEOF = 0x49454f46)`.

## Model Coordinate Conventions

Models are generally stored with pixel coordinates rather than coordinates scaled by the pixel size. 3dmod always stores a model with coordinates based upon the volume it is displayed on, or relative to the subset loaded when the full volume is not loaded. Coordinates range from 0 to NX in X and 0 to NY in Y, but from -0.5 to NZ - 0.5 in Z (NX, NY, NZ being the size of the volume loaded). The offset of 0.5 in Z occurs because integer coordinates are used for points drawn on X/Y slices, even though such points are displayed in the middle of the pixel in Z when viewed in X/Z or Y/Z slices. For example, a point with a Z coordinate of 0 will be drawn in the middle of the first pixel in X/Z views; a point at the very bottom of that first pixel has a coordinate of -0.5; and a point exactly in the middle of the volume in X/Z views has a coordinate of NZ / 2 - 0.5. If floating-point coordinates in the volume are considered to run from 0 to NZ in Z, the true volume coordinate is the Z model coordinate plus 0.5.

## The Model Data Structure

The Model structure data is 232 bytes long and contains the following data. A lot of this data is used by the 3dmod program to retain user settings.

| Length | Type  | Name       | Description                                                                                                               |
| ------ | ----- | ---------- | ------------------------------------------------------------------------------------------------------------------------- |
| 128    | char  | name       | Name of model file.                                                                                                       |
| 4      | int   | xmax       | Maximum values for x, y, and z. These are usually set to the image dimensions.                                            |
| 4      | int   | ymax       |                                                                                                                           |
| 4      | int   | zmax       |                                                                                                                           |
| 4      | int   | objsize    | Number of objects in model.                                                                                               |
| 4      | uint  | flags      | Model flags (IMODF_FLAG...) numbered from 0.                                                                              |
| 4      | int   | drawmode   | 1 to draw model, -1 not to.                                                                                               |
| 4      | int   | mousemode  | Mouse editing mode. (0=movie, 1=model)                                                                                    |
| 4      | int   | blacklevel | Contrast adjustment. (0-256) Default = 0.                                                                                 |
| 4      | int   | whitelevel | Contrast adjustment. (0-256) Default = 255.                                                                               |
| 4      | float | xoffset    | Offsets used for display & conversion, should be set to 0.                                                                |
| 4      | float | yoffset    |                                                                                                                           |
| 4      | float | zoffset    | (unused, superceded by MINX information)                                                                                  |
| 4      | float | xscale     | Scaling for pixel size. xscale and yscale should be 1.0 and zscale should be adjusted to account for the image thickness. |
| 4      | float | yscale     |                                                                                                                           |
| 4      | float | zscale     |                                                                                                                           |
| 4      | int   | object     | Current object, contour, and point, used for model editing.                                                               |
| 4      | int   | contour    |                                                                                                                           |
| 4      | int   | point      |                                                                                                                           |
| 4      | int   | res        | Minimum number of pixels between points when adding points by dragging mouse with middle button down.                     |
| 4      | int   | thresh     | Threshold level for auto contour generator.                                                                               |
| 4      | float | pixsize    | Size of one pixel, in the units given next.                                                                               |
| 4      | int   | units      | 0 = pixels, 3 = km, 1 = m, -2 = cm, -3 = mm, -6 = microns, -9 = nm, -10 = Angstroms, -12 = pm                             |
| 4      | int   | csum       | Checksum storage. Used for autosave only.                                                                                 |
| 4      | float | alpha      | Angles used for orientation of the model with image. Should be set to 0.0.                                                |
| 4      | float | beta       |                                                                                                                           |
| 4      | float | gamma      | (unused, superceded by MINX information)                                                                                  |

## The Object Data Structure

Each object in the model will have an object data structure. The ID value is `(OBJT = 0x4f424a54)`. The data structure is 176 bytes long with the following format.

| Length | Type  | Name       | Description                                                                                  |
| ------ | ----- | ---------- | -------------------------------------------------------------------------------------------- |
| 64     | char  | name       | Name of Object. Null terminated string.                                                      |
| 64     | uint  |            | Extra data for future use, indexed by IOBJ_EX_ defines.                                      |
| 4      | int   | contsize   | Number of Contours in object.                                                                |
| 4      | uint  | flags      | Bit flags for object (IMOD_OBJFLAG...), numbered from 0.                                     |
| 4      | int   | axis       | Z = 0, X = 1, Y = 2. (unused)                                                                |
| 4      | int   | drawmode   | Tells type of scattered points to draw (unused)                                              |
| 4      | float | red        | Color values, range is (0.0 - 1.0)                                                           |
| 4      | float | green      |                                                                                              |
| 4      | float | blue       |                                                                                              |
| 4      | int   | pdrawsize  | Default radius in pixels of scattered points in 3D.                                          |
| 1      | uchar | symbol     | Point Draw symbol in 2D, default is 1.                                                       |
| 1      | uchar | symsize    | Size of 2D symbol; radius in pixels.                                                         |
| 1      | uchar | linewidth2 | Linewidth in 2-D view.                                                                       |
| 1      | uchar | linewidth  | Linewidth in 3-D view.                                                                       |
| 1      | uchar | linesty    | Line draw style, 0 = solid; 1 = dashed (unused).                                             |
| 1      | uchar | symflags   | Bit 0 on : Fill the symbol.                                                                  |
| 1      | uchar | sympad     | Set to 0, for future use.                                                                    |
| 1      | uchar | trans      | Transparency, range is (0 to 100), maps to (1.0 to 0.0) in call to glColor4f or glMaterialfv |
| 4      | int   | meshsize   | Number of meshes in object.                                                                  |
| 4      | int   | surfsize   | Max surfaces in object.                                                                      |

## The Contour Data Structure

The contour ID is `(CONT = 0x434f4e54)` and the basic structure is 16 bytes long. Point data follows the contour header. Empty contours are allowed.

| Length   | Type      | Name  | Description                                                                 |
| -------- | --------- | ----- | --------------------------------------------------------------------------- |
| 4        | int       | psize | Number of points in contour.                                                |
| 4        | uint      | flags | Bit 3 on : open, do not connect endpoints.                                  |
|          |           |       | Bit 4 on : wild, not in one Z plane.                                        |
|          |           |       | Bit 5 on : draw stippled lines.                                             |
|          |           |       | Bit 6 on : draw if mouse in window, ignore Z.                               |
|          |           |       | Bit 7 on : draw on all planes, regardless of Z.                             |
|          |           |       | Bit 8 on : draw only in model mode.                                         |
|          |           |       | Bit 17 on : contour has pairs of scan lines.                                |
|          |           |       | Bits 18, 19, 20, 26-31: reserved for temporary use.                         |
| 4        | int       | time  | The time index used by this contour, numbered from 1, or 0 for no time set. |
| 4        | int       | surf  | The surface index used by this contour.                                     |
| 12*psize | float * 3 | pt    | Array of point triplets.                                                    |

## The Mesh Data Structure

The mesh ID is `(MESH = 0x4d455348)` and the basic structure is 20 bytes long. Vertex data and index data follow the mesh header.

| Length   | Type      | Name  | Description                                                          |
| -------- | --------- | ----- | -------------------------------------------------------------------- |
| 4        | int       | vsize | # of elements in vert array (# of triple floats).                    |
| 4        | int       | lsize | # of elements in list array (indexes).                               |
| 4        | uint      | flag  | Bit 16 on : normals have magnitudes.                                 |
|          |           |       | Bits 20-23 are resolution : 0 for high, 1 for lower resolution, etc. |
| 2        | short     | time  | Contains a time index or 0.                                          |
| 2        | short     | surf  | Contains a surface number or 0.                                      |
| 12*vsize | float * 3 | vert  | Array of points.                                                     |
| 4*lsize  | int       | list  | Array of ints.                                                       |

A point can be either a vertex position or a normal vector at a vertex. In current model files, `vert` consists of a sequence of vertex/normal pairs; i.e., vertex, normal, vertex, normal... The list array has a list of indices into the `vert` array plus negative index values with the following meanings:

- `-1`   end of list array                
- `-20`  next item on list is normal vector.
- `-21`  begin polygon with vertices and vertex indices only
- `-22`  end polygon
- `-23`  begin vertex,normal polygon pairs with normal,vertex indices
- `-24`  begin large convex polygon with normals
- `-25`  begin vertex,normal polygon pairs with vertex indices

Currently, meshes in model files consist only of polygons with vertex, normal pairs, starting with `-23` or `-25` and ending with `-22`. In polygons starting with `-23`, each set of 6 indices describes a triangle as follows:

- index to normal 1
- index to vertex 1
- index to normal 2
- index to vertex 2
- index to normal 3
- index to vertex 3

In polygons starting with `-25`, each normal is assumed to follow its corresponding vertex, and each triangle is described by only 3 indices:

- index to vertex 1
- index to vertex 2
- index to vertex 3

In polygons starting with `-21`, there are only vertices, no normals, and each triangle is described by the 3 indices as shown above for polygons starting with `-25`. Polygons have never started with `-24`, but if they did, normals would follow vertices and the indices would be to the vertices only.

## Optional Extra Data Chunks

Optional chunks can be put at the end of any data structure that the information is intended for, or at the end of the file. Unknown data chunks can be skipped since the size is included after the ID.

| Length | Type | Description                                |
| ------ | ---- | ------------------------------------------ |
| 4      | int  | (Chunk ID)                                 |
| 4      | int  | (Chunk Size)                               |
| size   |      | (Chunk Data) length of (Chunk Size) bytes. |

### Description of Current Optional Data Chunks

#### MINX - Model to Image Transformation Information (72 bytes data)

Coordinates are stored in an IMOD model file as image index coordinates relative to the last subset of the image file that the model was displayed on. The information here has two main uses:

1. It is used by 3dmod to display the model correctly when going between having a subset or the full image file loaded, or when displaying on an image file with different origin, scaling, or rotation angles in its header.
2. It is used by other programs to get back to the index coordinates of the full image file.

These data consist of 9 floats for old transformation values followed by 9 floats for current transformation values.

| Length | Type      | Name   | Description                                         |
| ------ | --------- | ------ | --------------------------------------------------- |
| 12     | float * 3 | oscale | Old scale values (unused in file).                  |
| 12     | float * 3 | otrans | Old translations (file stores image origin values). |
| 12     | float * 3 | orot   | Old rotations around X, Y, Z axes (unused in file). |
| 12     | float * 3 | cscale | New scale values in X, Y, Z.                        |
| 12     | float * 3 | ctrans | New translations in X, Y, Z.                        |
| 12     | float * 3 | crot   | New rotations around X, Y, Z axes.                  |

These values are based on the header information in the last image that the model was displayed on:

- `cscale` is pixel spacing (cell size over grid size, xlen/mx, etc.).
- `crot` is taken from the current tilt angles.
- `ctrans` is based on the origin of the image file minus the scale times the starting index coordinate of the image loaded into 3dmod. If a loaded subvolume were extracted into a separate file, it would have this same origin value. These origins have the original IMOD sign convention (subareas having more negative values).
- `otrans` has the origin values of the image file if the `OTRANS_ORIGIN` flag is set, again with the original IMOD sign convention.

To get from coordinates in a model file to an image file coordinate system, first Y and Z are exchanged if the `FLIPYZ` flag is set, then coordinates are multiplied by the scale values, translation values are subtracted, then points are rotated by the negative of the rotation angles around X, then Y then Z. In the simple case of no rotation, to get from an X coordinate in the model to the X pixel coordinate in the full image file, one would add `(otrans.x - ctrans.x) / cscale.x`. When 3dmod loads a model onto an image file, it first transforms coordinates as just described to fit the coordinate system of the file it was last loaded on, then it does a forward rotation by the current Z, Y, and X angles of the new file, adds the translation values for the loaded subvolume of the new file, and divides by its scale values. (Rotation is skipped if the old and new angles match.)

#### LABL - Label Contour and Point Data (Variable data size)

Each contour has a pointer to a label structure.

| Length | Type | Description                                   |
| ------ | ---- | --------------------------------------------- |
| 4      | int  | # of label items for points in contour.       |
| 4      | int  | size of contour label.                        |
| size   | char | contour label string padded to 4 byte chunks. |

For each point label item:

| Length | Type | Description                                 |
| ------ | ---- | ------------------------------------------- |
| 4      | int  | point index.                                |
| 4      | int  | size of label string.                       |
| size   | char | point label string padded to 4 byte chunks. |

#### OLBL - Label Surfaces in Object (Variable data size)

Each object has a pointer to a label structure.

| Length | Type | Description                              |
| ------ | ---- | ---------------------------------------- |
| 4      | int  | # of label items for surfaces in object. |
| 4      | int  | size of top-level label = 0 (unused).    |
| size   | char | unused.                                  |

For each surface label item:

| Length | Type | Description                                   |
| ------ | ---- | --------------------------------------------- |
| 4      | int  | surface index.                                |
| 4      | int  | size of label string.                         |
| size   | char | surface label string padded to 4 byte chunks. |

#### CLIP - Clipping Planes for Object (Variable data size)

#### MCLP - Global Clipping Planes for Model (Variable data size)

As of IMOD 2.4.9, the object structure, model view structure, and object view structure each has a clipping planes structure as a member, named `clips`. The latter structures are currently defined to hold 6 clipping planes, but these chunks are written with only the number of planes that exist, so their size is `4 + 24 * (# of planes stored)`.

Prior to IMOD 4.2.18, when there was only one plane and it was turned off, count was written as 0 for backwards compatibility to IMOD 2.4. Thus, the number of planes to read must be determined from `(chunk size - 4) / 24` rather than from the value of count that is read in, and if count is read in as zero it should be set to 1.

| Length   | Type      | Name   | Description                                                                                     |
| -------- | --------- | ------ | ----------------------------------------------------------------------------------------------- |
| 1        | uchar     | count  | Number of clipping planes stored, or 0 if one turned-off plane was stored prior to IMOD 4.2.18. |
| 1        | uchar     | flags  | Which clipping planes are on; for object planes, bit 7 means ignore global planes.              |
| 1        | uchar     | trans  | Transparency for clipped area. (future)                                                         |
| 1        | uchar     | plane  | Current clipping plane.                                                                         |
| 12*count | float * 3 | normal | Normals to clipping planes.                                                                     |
| 12*count | float * 3 | point  | Point values of clipping planes.                                                                |

#### IMAT - Material Definition for Object (16 bytes data)

| Length | Type  | Description |
| ------ | ----- | ----------- |
| 1      | uchar | ambient     | Ambient property. Range 0-255, scaled to 0-1, multiplied by red, green and blue to set the GL_AMBIENT property.                                     |
| 1      | uchar | diffuse     | Diffuse property. Range 0-255, scaled to 0-1, multiplied by red, green and blue to set the GL_DIFFUSE property.                                     |
| 1      | uchar | specular    | Specular property. Range 0-255, scaled to 0-1, added to red, green and blue to set the GL_SPECULAR property.                                        |
| 1      | uchar | shininess   | Shininess exponent in specular term. Range 0-255, scaled to 6.1 to 1.1 to set the GL_SHININESS property.                                            |
| 1      | uchar | fillred     | Fill color red.                                                                                                                                     |
| 1      | uchar | fillgreen   | Fill color green.                                                                                                                                   |
| 1      | uchar | fillblue    | Fill color blue.                                                                                                                                    |
| 1      | uchar | quality     | Sphere quality.                                                                                                                                     |
| 4      | uint  | mat2        | Set to 0, use as flags. Unused.                                                                                                                     |
| 1      | uchar | valblack    | Black level for showing stored values.                                                                                                              |
| 1      | uchar | valwhite    | White level for showing stored values.                                                                                                              |
| 1      | uchar | matflags2   | Flags: bit 0 on: skip low end data in value draw. bit 1 on: skip high end data in value draw. bit 2 on: keep color constant, not varied with value. |
| 1      | uchar | mat3b3      | Unused.                                                                                                                                             |

Prior to IMOD 2.7.1, the 4 bytes of `mat1` (fillred to quality) and the 4 bytes of `mat3` (valblack to mat3b3) were stored as a UINT (big-endian, thus reversed from the current definition). If bit 13 of model flags is off, `mat1` and `mat3` are assumed to be UINTs.

#### SIZE - Sizes for Each Point in a Contour (4 bytes per point)

| Length  | Type  | Description                |
| ------- | ----- | -------------------------- |
| 4*psize | float | Size value for each point. |

#### VIEW - Stored Model and Object View Data Structures (Variable size)

This chunk can be only 4 bytes, in which case it contains just the value of an INT for the current view number, which is stored as `cview` in the model structure. Otherwise, it contains stored view data. Various versions of 3dmod have stored 56, 156, or 176 bytes; after stored views began to contain properties for each object, this chunk became larger than that and variable-sized.

| Length | Type       | Name      | Description                                           |
| ------ | ---------- | --------- | ----------------------------------------------------- |
| 4      | float      | fovy      | Field of view of camera, perspective in degrees.      |
| 4      | float      | rad       | Viewing radius of sphere encloseing bounding box.     |
| 4      | float      | aspect    | Aspect ratio.                                         |
| 4      | float      | cnear     | Clip near: range 0.0 to 1.0, default 0.0.             |
| 4      | float      | cfar      | Clip far: range 0.0 to 1.0.                           |
| 12     | float * 3  | rot       | Model transformation values for model view: rotation. |
| 12     | float * 3  | trans     | Translation.                                          |
| 12     | float * 3  | scale     | Scale.                                                |
| 64     | float * 16 | mat       | World OpenGL transformation matrix (Unused).          |
| 4      | int        | world     | Flags for lighting and transformation properties.     |
| 32     | char       | label     | Name for the view.                                    |
| 4      | float      | dcstart   | Fog starting distance.                                |
| 4      | float      | dcend     | Fog ending distance.                                  |
| 4      | float      | lightx    | X coordinate of light.                                |
| 4      | float      | lighty    | Y coordinate of light.                                |
| 4      | float      | plax      | Parallax angle for stereo.                            |
| 4      | int        | objvsize  | Number of Iobjview structures following.              |
| 4      | int        | bytesObjv | Bytes per Iobjview structure.                         |

Currently, there are 187 bytes per object view, as follows:

| Length | Type      | Name         | Description                                                                                   |
| ------ | --------- | ------------ | --------------------------------------------------------------------------------------------- |
| 4      | uint      | flags        | Bit flags IMOD_OBJFLAG... (see above).                                                        |
| 4      | float     | red          | Red (0 - 1.0).                                                                                |
| 4      | float     | green        | Green (0 - 1.0).                                                                              |
| 4      | float     | blue         | Blue (0 - 1.0).                                                                               |
| 4      | int       | pdrawsize    | Size to draw scattered objs.                                                                  |
| 1      | uchar     | linewidth    | Linewidth in 3-D.                                                                             |
| 1      | uchar     | linesty      | Line draw style.                                                                              |
| 1      | uchar     | trans        | Transparency.                                                                                 |
| 1      | uchar     | clips.count  | Number of additional clip planes.                                                             |
| 1      | uchar     | clips.flags  | Which clip planes are on.                                                                     |
| 1      | uchar     | clips.trans  | Transparency for clipped area.                                                                |
| 1      | uchar     | clips.plane  | Current clip plane.                                                                           |
| 12     | float * 3 | clips.normal | Normal for first clipping plane.                                                              |
| 12     | float * 3 | clips.point  | Point value for first clipping plane.                                                         |
| 1      | uchar     | ambient      | Ambient property. (see above)                                                                 |
| 1      | uchar     | diffuse      | Diffuse property. (see above)                                                                 |
| 1      | uchar     | specular     | Specular property. (see above)                                                                |
| 1      | uchar     | shininess    | Shininess exponent in specular term. (see above)                                              |
| 1      | uchar     | fillred      | Fill color red.                                                                               |
| 1      | uchar     | fillgreen    | Fill color green.                                                                             |
| 1      | uchar     | fillblue     | Fill color blue.                                                                              |
| 1      | uchar     | quality      | Sphere quality.                                                                               |
| 4      | uint      | mat2         | Set to 0, use as flags. Unused.                                                               |
| 1      | uchar     | valblack     | Black level for showing stored values.                                                        |
| 1      | uchar     | valwhite     | White level for showing stored values.                                                        |
| 1      | uchar     | mat3b2       | Flags: bit 0 on: skip low end data in value draw. bit 1 on: skip high end data in value draw. |
| 1      | uchar     | mat3b3       | Unused.                                                                                       |
| 60     | float * 3 | clips.normal | Normals for clipping planes 2-6.                                                              |
| 60     | float * 3 | clips.point  | Point values for clipping planes 2-6.                                                         |

Prior to IMOD 2.7.1, the 4 bytes of a variable called `mat1` (now the uchars fillred to quality) and the 4 bytes of a variable called `mat3` (now the uchars valblack to mat3b3) were stored as a UINT (big-endian, thus reversed from the current definition). If bit 13 of model flags is off, `mat1` and `mat3` are assumed to be UINTs.

#### MOST - General Storage Information for Model (Variable size)

#### OBST - General Storage Information for Object (Variable size)

#### COST - General Storage Information for Contour (Variable size)

#### MEST - General Storage Information for Mesh (Variable size)

These chunks contain extra information for their respective entities. They were designed to hold fine-grained display properties for objects, contours, and meshes, but could be used for any kind of additional information that will fit in the Store data structure. The chunk consists of a series of Store entries, each 12 bytes long:

| Length | Type  | Name  | Description                                                                                                                                                                                                                                                                                                   |
| ------ | ----- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2      | short | type  | Type of information. Currently defined types are:                                                                                                                                                                                                                                                             |
|        |       |       | 1  Color change                                                                                                                                                                                                                                                                                               |
|        |       |       | 2  Fill color change                                                                                                                                                                                                                                                                                          |
|        |       |       | 3  Transparency change                                                                                                                                                                                                                                                                                        |
|        |       |       | 4  Do not connect to next point or do not display                                                                                                                                                                                                                                                             |
|        |       |       | 5  A connection number for meshing                                                                                                                                                                                                                                                                            |
|        |       |       | 6  3D line width change                                                                                                                                                                                                                                                                                       |
|        |       |       | 7  2D line width change                                                                                                                                                                                                                                                                                       |
|        |       |       | 8  Symbol type                                                                                                                                                                                                                                                                                                |
|        |       |       | 9  Symbol size                                                                                                                                                                                                                                                                                                |
|        |       |       | 10 General floating point value                                                                                                                                                                                                                                                                               |
|        |       |       | 11 Min and max of general values                                                                                                                                                                                                                                                                              |
| 2      | short | flags | 16 bits of flags. Currently defined flags are:                                                                                                                                                                                                                                                                |
|        |       |       | Bits 0 and 1 indicate type of "index" and 2 and 3 indicate type of "value", with 0 for int, 1 for float, 2 for short and 3 for byte                                                                                                                                                                           |
|        |       |       | Bit 4 on : "index" is not really an index                                                                                                                                                                                                                                                                     |
|        |       |       | Bit 5 on : Revert to default value                                                                                                                                                                                                                                                                            |
|        |       |       | Bit 6 on : Index is surface number, not contour                                                                                                                                                                                                                                                               |
|        |       |       | Bit 7 on : The change applies to only one point                                                                                                                                                                                                                                                               |
| 4      | union | index | Can contain one int or float, 2 shorts, or 4 bytes, generally has index of point or contour, or surface # has minimum for the min/max type                                                                                                                                                                    |
| 4      | union | value | Can contain one int or float, 2 shorts, or 4 bytes. For colors, 3 bytes hold red, green, and blue. Transparency is stored as an int from 0 to 255. Symbol type is 0, 2, 3 for open circles, squares, or triangles, -1, -3, -4 for closed circles, squares, or triangles. For min/max type, this holds the max |

#### SLAN - Slicer Angles and Positions (60 bytes)

These chunks contain time-specific slicer angles and positions as managed by the Slicer Angles dialog box. (Added IMOD 3.10.10)

| Length | Type    | Name   | Description                                     |
| ------ | ------- | ------ | ----------------------------------------------- |
| 4      | int     | time   | Time value of image file to which angles apply. |
| 12     | float*3 | angles | Rotation angles around X, Y, and Z axes.        |
| 12     | float*3 | center | Center coordinate of volume in slicer display.  |
| 32     | char    | label  | Text label.                                     |

#### MEPA - Meshing Parameters (76 bytes)

This chunk contains parameters used in meshing an object. If `capSkipNz` is nonzero, there needs to be an `SKLI` chunk with the Z values listed.

| Length | Type  | Name         | Description                                                           |
| ------ | ----- | ------------ | --------------------------------------------------------------------- |
| 4      | uint  | flags        | Bit flags for meshing.                                                |
|        |       |              | Bit 2 on : Do things sloppy and fast.                                 |
|        |       |              | Bit 3 on : Join data that skips sections.                             |
|        |       |              | Bit 4 on : Calculate normals.                                         |
|        |       |              | Bit 5 on : Force connection of stray contours.                        |
|        |       |              | Bit 6 on : Connect to same surface only.                              |
|        |       |              | Bit 7 on : Open contours are tubes.                                   |
|        |       |              | Bit 8 on : Connect to same time (type) only.                          |
|        |       |              | Bit 9 on : Cap ends of tubes.                                         |
|        |       |              | Bit 10 on : Object is already a copy.                                 |
|        |       |              | Bit 11 on : Use mean Z not starting Z to flatten.                     |
|        |       |              | Bit 12 on : Turn off overlap warnings.                                |
|        |       |              | Bit 13 on : Cap ends of tubes with domes.                             |
| 4      | int   | cap          | Capping parameter: 1 to cap just min and max ends, 2 to cap all ends. |
| 4      | int   | passes       | Number of passes for skipped sections.                                |
| 4      | int   | capSkipNz    | Number of Z values not to cap to.                                     |
| 4      | int   | inczLowRes   | Z increment for low resolution mesh.                                  |
| 4      | int   | inczHighRes  | Z increment for high resolution mesh.                                 |
| 4      | int   | minz         | Starting Z to mesh.                                                   |
| 4      | int   | maxz         | Ending Z to mesh.                                                     |
| 4      | int   | reserved     | Reserved.                                                             |
| 4      | float | overlaps     | Fractional overlap required if nonzero.                               |
| 4      | float | tubeDiameter | Diameter when meshing tubes.                                          |
| 4      | float | xmin         | X and Y limits for triangle output.                                   |
| 4      | float | xmax         |                                                                       |
| 4      | float | ymin         |                                                                       |
| 4      | float | ymax         |                                                                       |
| 4      | float | tolLowRes    | Point reduction tolerance for low and high resolution.                |
| 4      | float | tolHighRes   |                                                                       |
| 4      | float | flatCrit     | Criterion Z difference for rotating contours.                         |
| 4      | float | reserved     | Reserved.                                                             |

#### SKLI - Z Values Not to Cap to When Meshing (Variable data size)

This chunk contains the list of Z values not to cap to when meshing an object. The size in bytes is 4 times the number of values.

| Length | Type  | Name         | Description                     |
| ------ | ----- | ------------ | ------------------------------- |
| 4 * n  | float | capSkipZlist | List of Z values not to cap to. |

#### OGRP - Object Group List (Variable data size)

This chunk contains a name and list of object numbers for one object group. The size in bytes is 32 plus 4 times the number of objects in the group.

| Length | Type | Name    | Description                            |
| ------ | ---- | ------- | -------------------------------------- |
| 32     | char | name    | String with user's name for the group. |
| 4 * n  | int  | objList | Set of object numbers in the group.    |