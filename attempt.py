import cv2
path_to_img = "Convergence.jpg"
img = cv2.imread(path_to_img)
img_h, img_w, _ = img.shape
tiles_per_axis = 2
split_width = img_h // tiles_per_axis
split_height = img_w // tiles_per_axis


def start_points(size, split_size, overlap=0):
    points = [0]
    stride = int(split_size * (1-overlap))
    counter = 1
    while True:
        pt = stride * counter
        if pt + split_size >= size:
            points.append(size - split_size)
            break
        else:
            points.append(pt)
        counter += 1
    return points


X_points = start_points(img_w, split_width, 0.2)
Y_points = start_points(img_h, split_height, 0.2)

count = 0
name = 'splitted'
frmt = 'jpeg'
all_tiles = []

for i in Y_points:
    for j in X_points:
        split = img[i:i+split_height, j:j+split_width]
        if 0 == len(split) or 0 == len(split[0]):
            continue
        cv2.imwrite('{}_{}.{}'.format(name, count, frmt), split)
        split = cv2.imread('{}_{}.{}'.format(name, count, frmt))
        all_tiles.append(split)
        count += 1

print("Reached the stitcher, num of imgs = {}".format(len(all_tiles)))
stitcher = cv2.Stitcher_create(0)
stitcher.setPanoConfidenceThresh(0.01)
status, final_img = stitcher.stitch(all_tiles)
print(status)
if 0 == status:
    cv2.imwrite('FINAL_IMAGE.{}'.format(frmt), final_img)
