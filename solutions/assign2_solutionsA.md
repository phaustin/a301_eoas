diff --git a/solutions/assign2_solutions.md b/solutions/assign2_solutions.md
index 8a8d0b1..4029880 100644
--- a/solutions/assign2_solutions.md
+++ b/solutions/assign2_solutions.md
@@ -177,7 +177,6 @@ Satellite problem setup
 
 +++
 
-
 $$
 \begin{aligned}
 & \phi=\sin ^{-1}\left(\frac{6370}{8370}\right)=0.864\ \mathrm{rad} \approx 49\ deg \\
@@ -186,7 +185,6 @@ $$
 \end{aligned}
 $$
 
-
 +++
 
 ### But what is the flux?
@@ -222,7 +220,7 @@ If the Earth radiates as a blackbody at an equivalent blackbody temperature $T_E
 
 ### Answer
 
-Figure {numref}`zoom_out` shows a section of solid angle at a latitude of about 45 deg on the satellite.  How many Watts is arriving at that area?  We know that the flux (arrow) $F$ is arriving at an angle to the surface so we need to find the projection of the surface normal
+{numref}`zoom_out` shows a section of solid angle at a latitude of about 45 deg on the satellite.  How many Watts is arriving at that area?  We know that the flux (arrow) $F$ is arriving at an angle to the surface so we need to find the projection of the surface normal
 to the flux.  By the definition of solid angle, the surface area of the pixel is:
 
 $$
@@ -230,37 +228,38 @@ dA = r^2 d\omega
 $$
 where $r$ is the radius of the satellite.
 
-
-
 +++
 
 :::{figure} images/zoom_out.png
 :name: zoom_out
 :scale: 10
 
-Demonstration of Kirchoff’s law
+Solid angle of a piece of the satellite surface at 45 deg latitude
 :::
 
 +++
 
-:::{figure} images/zoom_in.png
-:name: zoom_in
-:scale: 10
+{numref}`zoom_in` shows the projected area normal to the incoming flux.  The watts $dE$ illuminating that area is defined by:
 
-Solid angle of a piece of the satellite surfas at 45 deg latitude
-:::
+$$
+dE = F \cos \theta dA = r^2 F \cos \theta \sin \theta d\theta d\phi
+$$
 
 +++
 
+:::{figure} images/zoom_in.png
+:name: zoom_in
+:scale: 10
 
+Solid angle of a piece of the satellite surface at 45 deg latitude
+:::
 
 +++
 
-
+Now do this integral over the 
 
 +++
 
-
 [Hint: Let $d E$ be the amount of radiation flux imparted to the satellite by the flux density $d E$ received within the infinitesimal element of solid angle $d \omega$.] Then,
 
 $$
