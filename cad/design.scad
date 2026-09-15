// Clip-on sensor pod for glasses temple; tune dimensions to the real frame.
$fn=48;
difference() { cube([42,20,12],center=true); translate([0,0,2]) cube([36,14,10],center=true); }
translate([-25,0,0]) difference() { cube([12,8,10],center=true); cube([14,3.2,5],center=true); }
