MAX_THEORETICAL_DISTANCE = 400.0


def calculate_distance_meters(power: int, rssi: int) -> float | None:
    """Calculate the distance in meters between the scanner and the device."""
    if rssi == 0 or power == 0:
        return None
    if (ratio := rssi / power) < 1.0:
        distance = ratio**10
    else:
        distance = 0.89976 * ratio**7.7095 + 0.111
    return distance if distance < MAX_THEORETICAL_DISTANCE else MAX_THEORETICAL_DISTANCE
