from yaml import load, FullLoader
import os
import vk
from urllib import request
from tempfile import mkdtemp
import webbrowser

# https://tulafest11.cosplay2.ru/orgs/setup/design
fest_id = 695

photos = """
https://vk.com/photo-20362122_457250238
https://vk.com/photo-20362122_457248898
https://vk.com/photo-20362122_456247664

https://vk.com/photo-20362122_456240113
https://vk.com/photo-20362122_457248700
https://vk.com/photo-20362122_456244737

https://vk.com/photo-20362122_456239614
https://vk.com/photo-20362122_457250237

https://vk.com/photo-20362122_456240089
https://vk.com/photo-20362122_457249979
"""

# m: 87 x 130
# o: 130 x 195
# p: 200 x 300
# q: 320 x 480
# r: 510 x 765
# s: 50 x 75
# w: 1000 x 1500
# x: 403 x 604
# y: 538 x 807
# z: 720 x 1080

portrait_thumb_size = 'o'
landscape_thumb_size = 'p'
full_size = 'w'

root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
config = load(
    open(os.path.join(root_dir, 'config.yml'), 'r', encoding='utf-8').read(),
    Loader=FullLoader)
vk_token = config['vk_token']

session = vk.Session(access_token=vk_token)
VK = vk.API(session)
photos = ",".join(photos.replace('https://vk.com/photo', '').split())
response = VK.photos.getById(v='5.85', photos=photos)

portrait_count, landscape_count = 0, 0
result_html = '<div class="gallery"><div class="gallery-block">\n'

img_dir = mkdtemp()

for i, photo in enumerate(response):
    try:
        full = filter(lambda size: size['type'] == full_size, photo['sizes']).__next__()
    except StopIteration:
        print(f"No size '{full_size}' for photo {i}")
        full = filter(lambda size: size['type'] == 'z', photo['sizes']).__next__()
    if full['width'] > full['height']:
        thumb_size = landscape_thumb_size
        landscape_count += 1
    else:
        thumb_size = portrait_thumb_size
        portrait_count += 1
    thumb = filter(lambda size: size['type'] == thumb_size, photo['sizes']).__next__()

    request.urlretrieve(full["url"], os.path.join(img_dir, f"gallery_full_{i}.jpg"))
    request.urlretrieve(thumb["url"], os.path.join(img_dir, f"gallery_thumb_{i}.jpg"))

    html = f'<a href="/files/{fest_id}/gallery_full_{i}.jpg" data-lightbox="roadtrip">' \
           f'<img class="gallery-image-{thumb_size}" src="/files/{fest_id}/gallery_thumb_{i}.jpg"></a>'

    result_html += html
    if i != len(response) - 1:
        if landscape_count >= 2:
            landscape_count = 0
            result_html += '\n</div><div class="gallery-block">\n'
        if portrait_count >= 3:
            portrait_count = 0
            result_html += '\n</div><div class="gallery-block">\n'
result_html += '\n</div></div>'

print(result_html)
webbrowser.open(img_dir)


# .gallery {
#     margin-left: -5px;
#     margin-right: -5px;
# }
# div.gallery-block {
#     display: inline-block;
# }
# img.gallery-image-o, img.gallery-image-p {
#     margin: 5px;
#     border-radius: 5px;
# }
# div.video {
# 	position: relative;
# 	padding-bottom: 56.25%; /* 16:9 */
# 	padding-top: 25px;
# 	height: 0;
# }
# iframe.video {
# 	position: absolute;
# 	top: 0;
# 	left: 0;
# 	width: 100%;
# 	height: 100%;
# }
# @media (max-width: 467px) and (min-width: 310px) {
#     .gallery {
#         display: block;
#         margin-left: -2px;
#         margin-right: -2px;
#     }
#     img.gallery-image-o {
#         width: 31.7%;
#         height: auto;
#         margin: 2px;
#     }
#     img.gallery-image-p {
#         width: 48.1%;
#         height: auto;
#         margin: 2px;
#     }
# }
