import unittest
from speed_controller import SpeedController


class TestSpeedControllerWhiteBox(unittest.TestCase):
    """Exercise each computation path and each validation failure path."""

    def test_initial_state_and_clear_branch(self):
        controller = SpeedController()
        self.assertEqual(controller.speed_limit, 60)
        self.assertEqual(controller.current_speed, 0)
        self.assertEqual(controller.weather_factor, 1.0)
        self.assertFalse(controller.safety_mode)
        self.assertEqual(controller.update_speed('clear', 0), 60.00)
        self.assertEqual(controller.current_speed, 60.00)

    def test_wet_medium_traffic_uphill_safety_mode(self):
        controller = SpeedController(60)
        controller.set_safety_mode(True)
        self.assertTrue(controller.safety_mode)
        self.assertEqual(controller.update_speed('wet', 50, 1), 40.00)
        self.assertEqual(controller.weather_factor, 0.85)

    def test_icy_high_traffic_downhill(self):
        controller = SpeedController(60)
        self.assertEqual(controller.update_speed('icy', 81, -10), 26.00)
        self.assertEqual(controller.weather_factor, 0.6)

    def test_zero_floor_without_safety_mode(self):
        controller = SpeedController(15)
        self.assertEqual(controller.update_speed('icy', 100, 10), 0.00)

    def test_zero_floor_with_safety_mode(self):
        controller = SpeedController(15)
        controller.set_safety_mode(True)
        self.assertEqual(controller.update_speed('icy', 100, 10), 0.00)
        controller.set_safety_mode(False)
        self.assertFalse(controller.safety_mode)

    def test_safety_speed_ceiling(self):
        controller = SpeedController(60)
        controller.set_safety_mode(True)
        self.assertEqual(controller.update_speed('clear', 0, -10), 50.00)

    def test_invalid_road_branch(self):
        with self.assertRaisesRegex(ValueError, 'road'):
            SpeedController().update_speed('gravel', 20, 0)

    def test_invalid_traffic_branches(self):
        for density in (-1, 101, 35.2, True):
            with self.subTest(density=density):
                with self.assertRaisesRegex(ValueError, 'Traffic density'):
                    SpeedController().update_speed('clear', density, 0)

    def test_invalid_slope_branches(self):
        for slope in (-11, 11, 3.5, True):
            with self.subTest(slope=slope):
                with self.assertRaisesRegex(ValueError, 'Slope angle'):
                    SpeedController().update_speed('clear', 20, slope)


if __name__ == '__main__':
    unittest.main()
