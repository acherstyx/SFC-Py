import base64
import cv2  # in linux conda env
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from io import BytesIO
from PIL import Image


def decode_base64_image(image_in_base64):
    """
    from base64 string to np.array
    :param image_in_base64:
    :return:
    """
    b_image = base64.b64decode(image_in_base64)
    return cv2.imdecode(np.frombuffer(b_image, np.uint8), cv2.IMREAD_COLOR)


def encode_image_to_base64(numpy_image):
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
    image_in = decode_base64_image(image_base64)

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
    plt.savefig(buffer, format="JPEG")
    str_encode = base64.b64encode(buffer.getvalue())

    plt.cla()

    return str_encode


def view_base64_image(image_in_base64):
    plt.cla()
    org_image = base64.b64decode(image_in_base64)
    image_in = cv2.imdecode(np.frombuffer(org_image, np.uint8), cv2.IMREAD_COLOR)
    plt.imshow(image_in[:, :, ::-1])
    # cv2.waitKey()
    plt.show()


def load_image_to_base64(filepath):
    b_image = open(filepath, 'rb')
    image_raw = b_image.read()

    return base64.b64encode(image_raw)


if __name__ == '__main__':
    image = "image_sample.jpg"
    test_image_in_base64 = load_image_to_base64(image)
    print(test_image_in_base64)

    his = base64_histogram(test_image_in_base64)
    print(his)

    view_base64_image(his)

    image = decode_base64_image(test_image_in_base64)
    image = encode_image_to_base64(image)
    image = decode_base64_image(image)
    image = encode_image_to_base64(image)

    view_base64_image(image)
