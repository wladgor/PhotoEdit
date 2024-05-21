from PIL import Image, ImageFilter, ImageDraw, ImageFont


# Тут методы по редактированию изображения
def met1rot(val, sohrn, name, direc):  # Метод поворота изображения
    im = Image.open(name)
    if val == 1:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)  # С лева направо

    if val == 2:
        im = im.transpose(Image.FLIP_TOP_BOTTOM)  # Сверху вниз

    if val == 3:
        im = im.transpose(Image.ROTATE_90)  # На 90

    if val == 4:
        im = im.transpose(Image.ROTATE_180)  # На 180

    if val == 5:
        im = im.transpose(Image.ROTATE_270)  # На 270

    im.save(direc + '/' + sohrn)


def met2nas(val, sohrn, name, direc):  # Метод общей настройки изображения
    im = Image.open(name)
    if val == 1:
        im = im.filter(ImageFilter.BLUR)  # Блюр
    if val == 2:
        im = im.filter(ImageFilter.DETAIL)  # Детализация
    if val == 3:
        im = im.filter(ImageFilter.EDGE_ENHANCE)  # Подчёркивание границ
    if val == 4:
        im = im.filter(ImageFilter.EDGE_ENHANCE_MORE)  # Более сильное подчёркивание границ
    if val == 5:
        im = im.filter(ImageFilter.EMBOSS)  # Рельеф
    if val == 6:
        im = im.filter(ImageFilter.SMOOTH)  # Сглаживание изображения
    if val == 7:
        im = im.filter(ImageFilter.SMOOTH_MORE)  # Сглаживание изображения сильнее
    if val == 8:
        im = im.filter(ImageFilter.SHARPEN)  # Повышение резкости

    im.save(direc + '/' + sohrn)


def met3gran(sohrn, name, direc):  # Метод нахождения границ, их выделения и тиснения
    im = Image.open(name)
    im = im.filter(ImageFilter.SMOOTH)
    im = im.filter(ImageFilter.FIND_EDGES)
    im.save(direc + '/' + sohrn)


def met4ava(sohrn, name, direc): # Метод скругления изображения
    image = Image.open(name)
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    width, height = image.size
    border_radius = min(width, height) // 2
    draw.ellipse((0, 0, border_radius * 2, border_radius * 2), fill=255)
    result = Image.new('RGBA', image.size)
    result.paste(image, (0, 0), mask=mask)
    result.save(direc + '/' + sohrn)


def met5txt(val, razmtext, shrift, text, sohrn, name, direc): # Метод наложения текста
    img = Image.open(name)
    draw = ImageDraw.Draw(img)
    width, height = img.size

    x, y, align = 0, 0, ""

    if val == 1:  # Левый верхний угол
        x = 10
        y = 10
        align = "left"
    elif val == 2:  # Правый верхний угол
        x = width - 10
        y = 10
        align = "right"
    elif val == 3:  # Левый нижний угол
        x = 10
        y = height - 10
        align = "left"
    elif val == 4:  # Правый нижний угол
        x = width - 10
        y = height - 10
        align = "right"
    elif val == 5:  # По середине
        x = width // 2
        y = height // 2
        align = "center"

    font = ImageFont.truetype(shrift, razmtext)
    text_bbox = draw.textbbox((x, y), text, font=font)

    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    text_x, text_y = 0, 0

    if align == "left":
        text_x = x
        text_y = y
    elif align == "right":
        text_x = x - text_width
        text_y = y
    elif align == "center":
        text_x = x - text_width // 2
        text_y = y - text_height // 2

    draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255))
    img.save(direc + '/' + sohrn)


def met6nal(val, op, sohrn, name, direc):  # Метод наложения водяного знака, где op он сам
    image = Image.open(name).convert("RGBA")
    watermark = Image.open(op).convert("RGBA")
    mask = watermark.convert("L").point(lambda x: 255 if x < 128 else 0, mode='1')
    image_width, image_height = image.size
    watermark_width, watermark_height = watermark.size
    position = 0
    if val == 1:
        # Верхний левый угол
        position = (0, 0)
    elif val == 2:
        # Левый нижний угол
        position = (0, image_height - watermark_height)
    elif val == 3:
        # Правый верхний угол
        position = (image_width - watermark_width, 0)
    elif val == 4:
        # Правый нижний угол
        position = (image_width - watermark_width, image_height - watermark_height)
    elif val == 5:
        # По середине
        position = ((image_width - watermark_width) // 2, (image_height - watermark_height) // 2)

    image.paste(watermark, position, mask)
    image.save(direc + '/' + sohrn)


def met7rgb(val, sohrn, name, direc): # Извлечение каналов и изменения их порядка
    im = Image.open(name)

    if val == 1:
        r, g, b = im.split()
        im = r
    elif val == 2:
        r, g, b = im.split()
        im = g
    elif val == 3:
        r, g, b = im.split()
        im = b
    elif val == 4:
        # GBR
        r, g, b = im.split()
        im = Image.merge('RGB', (g, b, r))
    elif val == 5:
        # GRB
        r, g, b = im.split()
        im = Image.merge('RGB', (g, r, b))
    elif val == 6:
        # BRG
        r, g, b = im.split()
        im = Image.merge('RGB', (b, r, g))
    elif val == 7:
        # BGR
        r, g, b = im.split()
        im = Image.merge('RGB', (b, g, r))
    elif val == 8:
        # RBG
        r, g, b = im.split()
        im = Image.merge('RGB', (r, b, g))

    im.save(direc + '/' + sohrn)

