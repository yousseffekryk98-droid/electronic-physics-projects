// Simple servo bracket for educational robotic arm.
$fn=48;
difference(){ cube([45,24,4],center=true); for(x=[-16,16]) translate([x,0,0]) cylinder(h=8,d=3.2,center=true); }
translate([0,0,12]) difference(){ cube([24,24,20],center=true); cube([20,14,18],center=true); }
