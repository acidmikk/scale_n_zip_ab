import os
from typing import Never

from PIL import Image, ImageEnhance
import img2pdf

from pdf_compressor import compress


def compress_to_jpeg(image_name: str, new_size_ratio=1, quality=10) -> Never:
    img = Image.open(image_name)
    print("Image shape:", img.size)
    image_size = os.path.getsize(image_name)
    print("Size before compression:", image_size)
    if new_size_ratio < 1.0:
        img = img.resize((int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)), Image.ANTIALIAS)
        print("New Image shape:", img.size)
    new_filename = f"jpeg_compressed.jpeg"
    try:
        # save the image with the corresponding quality and optimize set to True
        img.save(new_filename, quality=quality, optimize=True)
    except OSError:
        # convert the image to RGB mode first
        img = img.convert("RGB")
        # save the image with the corresponding quality and optimize set to True
        img.save(new_filename, quality=quality, optimize=True)
    print("New file saved:", new_filename)
    # get the new image size in bytes
    new_image_size = os.path.getsize(new_filename)
    # print the new size in a good format
    print("Size after compression:", new_image_size)
    # calculate the saving bytes
    saving_diff = new_image_size - image_size
    # print the saving percentage
    print(f"Image size change: {saving_diff/image_size*100:.2f}%.")


def to_pdf_BW(image_name: str) -> Never:
    image_size = os.path.getsize(image_name)
    img = Image.open(image_name)
    img_data = img.getdata()
    lst = []
    for i in img_data:
        lst.append(i[0] * 0.2125 + i[1] * 0.7174 + i[2] * 0.0721)

    new_img = Image.new("L", img.size)
    new_img.putdata(lst)
    new_filename = "png_bw.png"
    new_img.save(new_filename, quality=1)
    print("New file saved:", new_filename)
    new_image_size = os.path.getsize(new_filename)
    print("Size after compression:", new_image_size)
    saving_diff = new_image_size - image_size
    print(f"Image size change: {saving_diff / image_size * 100:.2f}%.")


def pdf(image_name: str) -> Never:
    image_size = os.path.getsize(image_name)
    img = Image.open(image_name)
    pdf_bytes = img2pdf.convert(img.filename)
    file = open('wo_scale.pdf', "wb")
    file.write(pdf_bytes)
    img.close()
    file.close()
    new_size = os.path.getsize('wo_scale.pdf')
    print("Size after compression:", new_size)
    saving_diff = new_size - image_size
    print(f"Image size change: {saving_diff / image_size * 100:.2f}%.")


def pdf_with_scale(image_name: str) -> Never:
    out_file = os.path.join('pdfcompressor4.pdf')
    compress(image_name, out_file, power=4)
    image_size = os.path.getsize(image_name)
    new_size = os.path.getsize('pdfcompressor4.pdf')
    print("Size after compression:", new_size)
    saving_diff = new_size - image_size
    print(f"Image size change: {saving_diff / image_size * 100:.2f}%.")


if __name__ == '__main__':
    # compress_to_jpeg("orig.jpg")
    # to_pdf_BW("orig.jpg")
    # pdf('orig.jpg')
    pdf_with_scale("wo_scale.pdf")
