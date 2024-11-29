def calculate_displacement(base_landmarks, current_landmarks, reference_point):
    """Calculate displacement of landmarks relative to the reference point."""
    relative_base = [(x - reference_point[0], y - reference_point[1]) for x, y in base_landmarks]
    relative_current = [(x - reference_point[0], y - reference_point[1]) for x, y in current_landmarks]
    displacements = {
        idx: (current[0] - base[0], current[1] - base[1])
        for idx, (base, current) in enumerate(zip(relative_base, relative_current))
    }
    return displacements

def detect_expression(displacements, thresholds):
    """Determine the facial expression based on displacements."""
    # Example conditions for each expression; adjust thresholds as needed
    if abs(displacements[61][0]) < thresholds["neutral"] and abs(displacements[61][1]) < thresholds["neutral"]:
        return "A"  # Neutral Face
    elif displacements[13][1] > thresholds["open_mouth"]:
        return "B"  # Open Mouth
    elif abs(displacements[291][0]) > thresholds["scrunch_mouth_right"]:
        return "E"  # Scrunch Mouth Right
    elif abs(displacements[61][0]) > thresholds["scrunch_mouth_left"]:
        return "F"  # Scrunch Mouth Left
    elif displacements[13][1] > thresholds["puffed_right_cheek"]:
        return "G"  # Puffed Right Cheek
    elif displacements[5][1] < -thresholds["eyebrows_furrowed"]:
        return "I"  # Eyebrows Furrowed
    return "A"
