# SqueakBake V2

This is an addon for blender that helps you to automate the squeaks and screeches of rotating objects to get 3d soundFx.

  Instead of adding the tracks manually and trying to match the movement to the sound use this addon. It duplicates the NLA soundtrack for every change in rotation direction or after a brake in the euler rotation for the specified axis.

Basic Tutorial here for version 1:
https://youtu.be/puugbwrAoEw

The interface is simple
          


You can find the tool in the Speaker Properties
1 - just chose the name of the NLA tracks (it will replace all the tracks with that name, just don't name it "SoundTrack")

2 - chose the object that you are referencing, from the list or with the picker

3 - chose deformation to be monitored 

4 - chose the axis

5 - type of sqeaks (after lower or higher values of the deformation or when it stops)

and Bake



I hope you enjoy it. :)




there is also a pannel for the Sequencer that is still experimental:
      add your sound, select it and "Squeak Sequences". 
      the bake doesn't overide the previous bake and the initial sound clip is moved at the end of the timeline
      the script gives errors when the selected clip is deleted and you try to "Squeak Sequences"
      other than that it works great


The addon will soon have more options to add sound while in action or on changes of action, to ad tracks for movement (best for sliders, actuators, hydraulics).


Upcoming Updates:


options to link the speaker object to the target and move it in position
support for different rotation type like Quaternion(WXYZ)
ability to get the deformation from bones and fcurve animations
speed improvements on heavy scenes 

With your support i will be able to ad all this to the addon.

If you whant to support this project you can donate via gumroad:
https://gumroad.com/l/Sq_Bk

Enjoy
