// Autonomous Line Following Robot — parametric demo chassis/base
$fn=48;
L=150; W=90; T=3; axle=3.2;
difference() {
  cube([L,W,T], center=true);
  for (x=[-55,55], y=[-32,32]) translate([x,y,0]) cylinder(h=10,d=3.4,center=true);
  for (x=[-60,60]) translate([x,0,0]) cylinder(h=10,d=axle,center=true);
}
translate([0,0,T/2]) linear_extrude(0.8) text("mostafa-10-line-following-ro", size=6, halign="center");
