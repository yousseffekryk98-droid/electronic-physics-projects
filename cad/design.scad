// Mini Weather Satellite (CubeSat Prototype) — 1U-style educational frame (not flight hardware)
$fn=40; S=100; rail=6;
for (x=[0,S-rail], y=[0,S-rail]) translate([x,y,0]) cube([rail,rail,S]);
for (z=[0,S-rail]) {
  translate([0,0,z]) cube([S,rail,rail]);
  translate([0,S-rail,z]) cube([S,rail,rail]);
  translate([0,0,z]) cube([rail,S,rail]);
  translate([S-rail,0,z]) cube([rail,S,rail]);
}
