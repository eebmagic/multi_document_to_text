from PIL import Image


def makeOutputPath(inputPath):
    SPLITS = inputPath.split('/')
    name = SPLITS[-1]
    container = '/'.join(SPLITS[:-1])
    return container + f"/{name}_output.png"


# Load Image Data #
image_PATH = input("Drag Image Here: ").strip()
im = Image.open(image_PATH)
raw_data = list(im.getdata())

# Invert Color Data #
new_data = []
for point in raw_data:
    one, two, three = point[:3]
    newPoint = (255 - one, 255 - two, 255 - three)
    new_data.append(newPoint)

# Output New Image Data #
newIm = Image.new("RGB", im.size)
newIm.putdata(new_data)
new_PATH = makeOutputPath(image_PATH)
newIm.save(new_PATH)

print("\nFINISHED")
print(f"Exported to: {new_PATH}")