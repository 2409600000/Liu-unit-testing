class SpeedController:
    """Compute safe target speeds under road, traffic, and slope conditions."""

    def __init__(self, speed_limit=60):
        self.speed_limit = speed_limit
        self.current_speed = 0
        self.weather_factor = 1.0
        self.safety_mode = False

    def set_safety_mode(self, enabled: bool):
        """Enable or disable the extra speed cap."""
        self.safety_mode = enabled

    def update_speed(self, road_condition: str, traffic_density: int,
                     slope_angle: int = 0) -> float:
        """Return target speed in km/h, rounded to two decimal places."""
        # The README defines valid values and is the test oracle.
        if road_condition not in ('clear', 'wet', 'icy'):
            raise ValueError("Invalid road condition")
        if type(traffic_density) is not int or not 0 <= traffic_density <= 100:
            raise ValueError("Traffic density must be an integer from 0 to 100")
        if type(slope_angle) is not int or not -10 <= slope_angle <= 10:
            raise ValueError("Slope angle must be an integer from -10 to 10")

        base_speed = self.speed_limit

        if road_condition == 'wet':
            self.weather_factor = 0.85
        elif road_condition == 'icy':
            self.weather_factor = 0.6
        else:
            self.weather_factor = 1.0
        base_speed *= self.weather_factor

        if traffic_density >= 50:
            if traffic_density > 80:
                base_speed -= 20
            else:
                base_speed -= 10

        if slope_angle > 0:  # Uphill
            base_speed -= slope_angle
        elif slope_angle < 0:  # Downhill
            base_speed += abs(slope_angle)

        # Speeds cannot be negative. Safety mode additionally enforces
        # the (speed_limit - 10) ceiling specified by the requirements.
        base_speed = max(base_speed, 0)
        if self.safety_mode:
            base_speed = min(base_speed, max(self.speed_limit - 10, 0))

        self.current_speed = round(base_speed, 2)
        return self.current_speed
