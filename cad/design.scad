// Intelligent Traffic Density Analyzer — generic adjustable mounting bracket.
$fn=48;
difference() {
  cube([60,35,4],center=true);
  for(x=[-22,22]) translate([x,0,0]) cylinder(h=8,d=4.2,center=true);
}
translate([0,14,18]) difference() { cube([40,4,32],center=true); translate([0,0,4]) cylinder(h=10,d=12,center=true, $fn=48); }
