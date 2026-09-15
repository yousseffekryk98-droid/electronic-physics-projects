// Tabletop solar charging station enclosure — scale before fabrication.
$fn=48;
difference() {
  cube([160,100,90], center=true);
  translate([0,0,3]) cube([154,94,86], center=true);
  translate([0,-51,5]) cube([90,8,28], center=true); // port/display face opening
}
