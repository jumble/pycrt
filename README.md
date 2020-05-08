# PyCRT 

A demo of a CR beamsweep emulation. Pretty cursory atm.

## to use 
 - install all the requirements (`pip install -f requirements.txt`, in a virtualenv or not, i'm not your dad)
 - get an image of your choice in this directory, then replace the image path in `crt.py`'s `main` function with the name of your image
 - if you want, edit the `CRTDrawerConfig` there too:
   - `rgbarray`: the image loaded above 
   - `dim_delay`: number of frames between screen dims (int)
   - `dim_amount`: screen dim amount (int)
   - `beam_sweep_amount`: number of pixels traversed by the beam in a single update
 - run `crt.py`

## todo
 - More realtime sweeping
   - Rewrite in a more suitable language, or at least more performant Python
 - Actually target pixels with a vector "beam" that can be distorted by emulated fields!
   - like when you hold a magnet up to a real crt
 - through the above, or via another way : various fuzzing effects (haha tv go bzz)