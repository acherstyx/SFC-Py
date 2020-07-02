import base64
import cv2  # in linux conda env
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from io import BytesIO
from PIL import Image


def __decode_base64_image(image_in_base64):
    """
    from base64 string to np.array
    :param image_in_base64:
    :return:
    """
    b_image = base64.b64decode(image_in_base64)
    return cv2.imdecode(np.frombuffer(b_image, np.uint8), cv2.IMREAD_COLOR)


def __encode_image_to_base64(numpy_image):
    """
    from np.array format to base64 string
    :param numpy_image:
    :return:
    """
    buffer = BytesIO()

    pil_image = Image.fromarray(numpy_image)
    pil_image.save(buffer, format="JPEG")
    str_encode = base64.b64encode(buffer.getvalue())

    return str_encode


def base64_histogram(image_base64):
    image_in = __decode_base64_image(image_base64)

    fig = Figure()
    canvas = FigureCanvasAgg(fig)

    plt.title("Color Histogram")
    plt.xlabel("gray Level")
    plt.ylabel("number of pixels")

    colors = ('b', 'g', 'r')
    for (chan, color) in zip(image_in, colors):
        hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
        plt.plot(hist, color=color)
        plt.xlim([0, 256])
        plt.ylim([0, 512])
    canvas.draw()

    buffer = BytesIO()
    plt.savefig(buffer)
    str_encode = base64.b64encode(buffer.getvalue())

    return str_encode


def view_base64_image(image_in_base64):
    org_image = base64.b64decode(image_in_base64)
    image_in = cv2.imdecode(np.frombuffer(org_image, np.uint8), cv2.IMREAD_COLOR)
    cv2.imshow("base64_image_view", image_in)
    cv2.waitKey()


if __name__ == '__main__':
    image = "../image_sample.jpg"
    test_image = open(image, "rb")
    test_image_raw = test_image.read()

    test_image_in_base64 = base64.b64encode(test_image_raw)
    print(test_image_in_base64)

    his = base64_histogram(test_image_in_base64)
    print(his)

    # view_base64_image(his)

    image = __decode_base64_image(test_image_in_base64)
    image = __encode_image_to_base64(image)
    image = __decode_base64_image(image)
    image = __encode_image_to_base64(image)

    view_base64_image(image)
