

union() {
	color(alpha = 1.0000000000, c = "gray") {
		translate(v = [5.,5.,5.]) {
			rotate(a = 54.735610317245346, v = [-10.0, 10.0, 0]) {
				cylinder(center = true, h = 17.320508075688775, r = 0.5000000000);
			}
		}
	}
	color(alpha = 1.0000000000, c = "blue") {
		translate(v = [20.0000000000, -10.0000000000, -10.0000000000]) {
			cube(center = false, size = [10.0000000000, 20.0000000000, 20.0000000000]);
		}
	}
}