import unittest
from speed_controller import SpeedController


class TestSpeedControllerBlackBox(unittest.TestCase):
    """Cases chosen from requirement categories and nominal boundaries."""

    def setUp(self):
        self.controller = SpeedController(speed_limit=60)

    def test_clear_road_with_no_adjustments(self):
        self.assertEqual(self.controller.update_speed('clear', 0, 0), 60.00)

    def test_safety_mode_caps_downhill_speed(self):
        self.controller.set_safety_mode(True)
        self.assertEqual(self.controller.update_speed('clear', 0, -10), 50.00)

    def test_wet_road_below_traffic_boundary(self):
        self.assertEqual(self.controller.update_speed('wet', 49, -1), 52.00)

    def test_wet_road_at_traffic_boundary(self):
        self.controller.set_safety_mode(True)
        self.assertEqual(self.controller.update_speed('wet', 50, 0), 41.00)

    def test_icy_road_at_eighty_traffic(self):
        self.assertEqual(self.controller.update_speed('icy', 80, 10), 16.00)

    def test_icy_road_above_eighty_traffic(self):
        self.assertEqual(self.controller.update_speed('icy', 81, 0), 16.00)

    def test_maximum_traffic_and_downhill(self):
        self.assertEqual(self.controller.update_speed('clear', 100, -10), 50.00)

    def test_clear_road_at_fifty_traffic(self):
        self.assertEqual(self.controller.update_speed('clear', 50, 0), 50.00)

    def test_clear_road_just_below_fifty_traffic(self):
        self.assertEqual(self.controller.update_speed('clear', 49, 1), 59.00)

    def test_wet_road_upper_medium_traffic_boundary(self):
        self.assertEqual(self.controller.update_speed('wet', 80, -9), 50.00)

    def test_icy_road_with_safety_mode(self):
        self.controller.set_safety_mode(True)
        self.assertEqual(self.controller.update_speed('icy', 100, 10), 6.00)

    def test_uphill_and_safety_mode(self):
        self.controller.set_safety_mode(True)
        self.assertEqual(self.controller.update_speed('clear', 0, 10), 50.00)

    def test_invalid_road_condition(self):
        with self.assertRaises(ValueError):
            self.controller.update_speed('snowy', 20, 0)

    def test_invalid_traffic_density_boundaries(self):
        for density in (-1, 101, 50.5, True):
            with self.subTest(density=density):
                with self.assertRaises(ValueError):
                    self.controller.update_speed('clear', density, 0)

    def test_invalid_slope_boundaries(self):
        for slope in (-11, 11, 1.5, True):
            with self.subTest(slope=slope):
                with self.assertRaises(ValueError):
                    self.controller.update_speed('clear', 20, slope)


if __name__ == '__main__':
    unittest.main()
