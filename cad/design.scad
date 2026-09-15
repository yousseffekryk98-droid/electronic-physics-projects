// Medication demo carousel; educational prototype only.
$fn=96; pockets=8;
difference() {
  cylinder(h=8,d=120);
  cylinder(h=12,d=8);
  for(i=[0:pockets-1]) rotate([0,0,i*360/pockets]) translate([40,0,-1]) cylinder(h=12,d=24);
}
