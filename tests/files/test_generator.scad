

union() {
	color(alpha = 1.0000000000, c = "gray") {
		difference() {
			translate(v = [-100.0000000000, -100.0000000000, -100.0000000000]) {
				cube(center = false, size = [200.0000000000, 200.0000000000, 200.0000000000]);
			}
			translate(v = [0.,0.,5.]) {
				rotate(a = 0.0, v = [-0.0, 0.0, 0]) {
					cylinder(center = true, h = 10.0, r = 5.0000000000);
				}
			}
		}
	}
	color(alpha = 1.0000000000, c = "blue") {
		translate(v = [0.,0.,5.]) {
			rotate(a = 0.0, v = [-0.0, 0.0, 0]) {
				cylinder(center = true, h = 10.0, r = 5.0000000000);
			}
		}
	}
}