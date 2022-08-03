# WAVE FUNCTION COLLAPSE

**Be aware that this addons is subject to drastic changes**

This is a simplistic implementation of the wave fuction collapse idea from [mxgmn](https://github.com/mxgmn/WaveFunctionCollapse).

A great [video explanation](https://www.youtube.com/watch?v=2SuvO4Gi7uY) from Martin Donald.

## Installation

Download the repo in the release tab for stable version or on the main page for dev version.

In blender head to edit > Preferences > Add-ons > Install...
locate your .zip file and click install addon.

## Usage

Right now the addon doesn't have an interface although you can use the Operator search [^operator] to get the functions currently implemented :
- Clean Meshes
> This function rounds the vertices location making the meshes matching easier (this might cause some visual changes to your meshes)
- Create database
> This function matches the __selected__ meshes and creates a .json file for later use
- Run the wavefunction
> This function runs the wavefunction

**make sure that the tiles you want to use have a size of 2/2/2 to match**

**make sure that the scale/roation is applied to the mesh before making the database**

## Example

![result]


## TODO

- [ ] create a interface
- [ ] weight for tiles
- [ ] tutorial video
- [ ] improve the database creation process
- [ ] collection managment
- [ ] animation of the collapse
- [ ] custom size and shape grid

## Current limitation and future plans

- Right now the size of the grid is fixed, if you wish to change the size of the grid you must edit the code of the addon (this will be changed when there is an iterface)
- Be aware that for the matching to work the adjacents faces needs the vertices to be at the same local coordinates.
- The dataset creation is a bit picky and can skip meshes that should match together. If this happend to you try using the `clean meshes` function to fix the issue.

[^operator]:
    To enable the operator head to edit > Preferences > Interface and tick Developer Extras. It is located in Edit > Operator Search