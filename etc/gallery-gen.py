import vk

request = """
https://vk.com/photo-91388480_456240395
https://vk.com/photo-61844462_456248333
https://vk.com/photo-91388480_456240396

https://vk.com/photo-61844462_456248347
https://vk.com/photo-61844462_456248305
https://vk.com/photo-158861171_456243031

https://vk.com/photo-61844462_456248332
https://vk.com/photo146929524_456242973

https://vk.com/photo146929524_456242974
https://vk.com/photo-158861171_456242916
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

# https://oauth.vk.com/authorize?v=5.85&response_type=token&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,groups,photos&client_id=[INSERT_ID_HERE]
session = vk.Session(access_token='')
VK = vk.API(session)
photos = ",".join(request.replace('https://vk.com/photo', '').split())
response = VK.photos.getById(v='5.85', photos=photos)

portrait_count, landscape_count = 0, 0
result_html = '<div class="gallery"><div class="gallery-block">\n'

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
    html = f'<a href="{full["url"]}" data-lightbox="roadtrip">' \
           f'<img class="gallery-image-{thumb_size}" src="{thumb["url"]}"></a>'
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
