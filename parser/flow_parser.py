import cv2
import numpy as np
import pytesseract
import math

pytesseract.pytesseract.tesseract_cmd = r"tesseract"  # Use full path if needed

def get_shape_type(approx, contour):
    """
    Determines the type of shape using the approximated contour.
    For 4-vertex shapes, uses the rotation angle to decide if it’s a decision (diamond) or rectangle.
    """
    if len(approx) == 3:
        return "triangle"
    elif len(approx) == 4:
        # Use the minimum area rectangle to get rotation information.
        rect = cv2.minAreaRect(contour)
        angle = rect[-1]
        # Adjust angle into a common range.
        if angle < -45:
            angle = 90 + angle
        # Heuristic: if the angle deviates notably from 0, consider it a diamond (decision).
        if abs(angle) > 20:
            return "decision"
        else:
            return "rectangle"
    elif len(approx) > 4:
        return "ellipse"
    else:
        return "unknown"

def detect_shapes_and_text(image):
    """
    Detect shapes in the image and extract text within them.
    Returns a list of dictionaries with shape details.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5,5), 0)
    edged = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    shapes = []
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        x, y, w, h = cv2.boundingRect(approx)
        if w < 30 or h < 30:  # Skip small/noisy regions
            continue
        roi = image[y:y + h, x:x + w]
        text = pytesseract.image_to_string(roi, config='--psm 6').strip()
        shape_type = get_shape_type(approx, cnt)
        if text:
            shapes.append({
                "type": shape_type,
                "text": text,
                "bbox": (x, y, w, h),
                "center": (x + w // 2, y + h // 2)
            })
    return shapes

def detect_arrows(image):
    """
    Detect arrows using Hough Line Transform.
    For each detected line, extract a small region around its midpoint to OCR any label (such as Yes/No).
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=80, minLineLength=30, maxLineGap=10)
    arrows = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            mid_x = (x1 + x2) // 2
            mid_y = (y1 + y2) // 2
            # Define a small ROI around the midpoint
            roi = image[max(0, mid_y - 10): mid_y + 10, max(0, mid_x - 20): mid_x + 20]
            label = pytesseract.image_to_string(roi, config='--psm 7').strip()
            arrows.append({
                "from": (x1, y1),
                "to": (x2, y2),
                "label": label  # May be empty if no text is detected.
            })
    return arrows

def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def match_arrows_to_shapes(shapes, arrows):
    """
    For each detected arrow, find the nearest shape centers for its start and end points.
    Returns a list of connections with arrow labels if any.
    """
    connections = []
    for arrow in arrows:
        start_pt = arrow["from"]
        end_pt = arrow["to"]
        start_shape = min(shapes, key=lambda s: distance(start_pt, s["center"]))
        end_shape = min(shapes, key=lambda s: distance(end_pt, s["center"]))
        if start_shape != end_shape:
            connections.append({
                "start": start_shape,
                "end": end_shape,
                "label": arrow.get("label", "")
            })
    return connections

def build_flow_with_decisions(connections):
    """
    Build a list of readable instructions representing the flow.
    - For decision nodes, include the arrow label in the condition.
    - For regular transitions, display a simple connection.
    """
    instructions = []
    for conn in connections:
        start_text = conn["start"]["text"]
        end_text = conn["end"]["text"]
        label = conn["label"]
        if conn["start"]["type"] == "decision":
            # If the start is a decision box, include its condition.
            instr = f"IF '{start_text}' == '{label}' THEN '{end_text}'"
        else:
            if label:
                instr = f"From '{start_text}' via '{label}' to '{end_text}'"
            else:
                instr = f"From '{start_text}' to '{end_text}'"
        instructions.append(instr)
    return instructions

def parse_flowchart_steps(image_path):
    """
    Main function to parse a flowchart image.
    Returns a list of flow instructions including all detected texts,
    decisions (diamond shapes), and arrow labels.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image could not be read")
    
    shapes = detect_shapes_and_text(image)
    if not shapes:
        return ["No recognizable shapes or text found."]
    
    arrows = detect_arrows(image)
    connections = match_arrows_to_shapes(shapes, arrows)
    instructions = build_flow_with_decisions(connections)
    
    # Add any isolated shapes (not connected via arrows)
    connected_texts = set()
    for conn in connections:
        connected_texts.add(conn["start"]["text"])
        connected_texts.add(conn["end"]["text"])
    for shape in shapes:
        if shape["text"] not in connected_texts:
            instructions.append(shape["text"])
    
    return instructions