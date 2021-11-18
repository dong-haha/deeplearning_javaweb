import numpy as np


def convert_xyxy_to_xywh(boxes, copy=True):
    """Convert [x_min, y_min, x_max, y_max] format to [x_min, y_min, width, height] format.
    """
    if copy:
        boxes = boxes.copy()
    boxes[:, 2:4] -= boxes[:, 0:2]
    return boxes


def convert_xywh_to_xyxy(boxes, copy=True):
    """Convert [x_min, y_min, width, height] format to [x_min, y_min, x_max, y_max] format.
    """
    if copy:
        boxes = boxes.copy()
    boxes[:, 2:4] += boxes[:, 0:2]
    return boxes


def convert_xywh_to_cxcywh(boxes, copy=True):
    """Convert [x_min, y_min, width, height] format to [cx, cy, width, height] format.
    """
    if copy:
        boxes = boxes.copy()
    boxes[:, 0:2] += boxes[:, 2:4] * 0.5
    return boxes
    
    
def convert_cxcywh_to_xywh(boxes, copy=True):
    """Convert [cx, cy, width, height] format to [x_min, y_min, width, height] format.
    """
    if copy:
        boxes = boxes.copy()
    boxes[:, 0:2] -= boxes[:, 2:4] * 0.5
    return boxes
    
    
def convert_xyxy_to_cxcywh(boxes, copy=True):
    """Convert [x_min, y_min, x_max, y_max] format to [cx, cy, width, height] format.
    """
    boxes = convert_xyxy_to_xywh(boxes, copy)
    boxes = convert_xywh_to_cxcywh(boxes, False)
    return boxes


def convert_cxcywh_to_xyxy(boxes, copy=True):
    """Convert [x_min, y_min, x_max, y_max] format to [cx, cy, width, height] format.
    """
    boxes = convert_cxcywh_to_xywh(boxes, copy)
    boxes = convert_xywh_to_xyxy(boxes, False)
    return boxes


def convert_boxes_format(boxes, in_fmt, out_fmt, copy=True):
    """Converts boxes from given in_fmt to out_fmt.

    Supported in_fmt and out_fmt are:

    'xyxy': boxes are represented via corners, x1, y1 being top left and x2, y2 being bottom right.

    'xywh' : boxes are represented via corner, width and height, x1, y2 being top left, w, h being width and height.

    'cxcywh' : boxes are represented via centre, width and height, cx, cy being center of box, w, h
    being width and height.

    Args:
        boxes: boxes which will be converted.
        in_fmt (str): Input format of given boxes. Supported formats are ['xyxy', 'xywh', 'cxcywh'].
        out_fmt (str): Output format of given boxes. Supported formats are ['xyxy', 'xywh', 'cxcywh']

    Returns:
        boxes: Boxes into converted format.

    References:
        torchvision.ops.box_convert
    """
    allowed_fmts = ("xyxy", "xywh", "cxcywh")
    if in_fmt not in allowed_fmts or out_fmt not in allowed_fmts:
        raise ValueError("Unsupported Bounding Box Conversions for given in_fmt and out_fmt")
    if copy:
        boxes = boxes.copy()
    if in_fmt == out_fmt:
        return boxes

    if (in_fmt, out_fmt) == ("xyxy", "xywh"):
        boxes = convert_xyxy_to_xywh(boxes, copy=False)
    elif (in_fmt, out_fmt) == ("xywh", "xyxy"):
        boxes = convert_xywh_to_xyxy(boxes, copy=False)
    elif (in_fmt, out_fmt) == ("xywh", "cxcywh"):
        boxes = convert_xywh_to_cxcywh(boxes, copy=False)
    elif (in_fmt, out_fmt) == ("cxcywh", "xywh"):
        boxes = convert_cxcywh_to_xywh(boxes, copy=False)
    elif (in_fmt, out_fmt) == ("xyxy", "cxcywh"):
        boxes = convert_xyxy_to_cxcywh(boxes, copy=False)
    elif (in_fmt, out_fmt) == ("cxcywh", "xyxy"):
        boxes = convert_cxcywh_to_xyxy(boxes, copy=False)
    return boxes
    