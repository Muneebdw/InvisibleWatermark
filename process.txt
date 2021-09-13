ENCODING
-Create a empty pixel map (Represents a empty image)
-Convert the two host and secret image to a pixel map.
-Coverts the rgb values of both images into binary bits.
-Takes host image binary and makes them most significant (Starting Bits).
-Takes secret image binary and makes them least significant (Ending bits)
-Combine and Save them , then convert binary to RGB and save inside pixel map.
-Encoded image then saved.

DECODING
-gets the encoded image
-converts it to pixel map
-converts its rgb values to binary bits.
-takes the least significant binary bits (Ending bits).
-Saves them into a empty pixel map
-The extract least signifcant binary bits are saved onto the pixel map.
-Decoded image is then saved.