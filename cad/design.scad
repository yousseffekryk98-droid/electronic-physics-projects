// Wearable Health Monitor — parametric electronics enclosure base.
$fn=48;
L=90; W=60; H=28; wall=2.4;
difference() {
  cube([L,W,H]);
  translate([wall,wall,wall]) cube([L-2*wall,W-2*wall,H]);
  translate([L/2-14,-1,10]) cube([28,wall+2,10]);
}
for(x=[8,L-8], y=[8,W-8]) translate([x,y,wall]) difference() { cylinder(h=7,d=7); cylinder(h=8,d=3); }
