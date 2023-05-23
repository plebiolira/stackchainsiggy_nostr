def extract_image_url_from_content(content, image_filetypes):
    for image_filetype in image_filetypes:
        if content.rfind(image_filetype) > 0:
            first_image_filetype_rfound = image_filetype
            filetype_len = len(first_image_filetype_rfound)
    image_url = content[:content.rfind(first_image_filetype_rfound)+filetype_len]
    # http_or_https = image_url[image_url.rfind("://")-:]
    # print(image_url[image_url.rfind("://")-5:])
    if image_url[image_url.rfind("://")-5:][:5] == "https":
        https_or_http = 5
    else:
        https_or_http = 4
    image_url = image_url[image_url.rfind("://")-https_or_http:]
    filename = image_url[1+image_url.rfind("/"):]

    return image_url, filename
