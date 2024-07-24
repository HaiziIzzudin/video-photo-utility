from os import path # dlm code tulis je path.dirname(name)
def fixFileExists(file: str):

  base = path.basename(file)

  f = base.split("_")
  g = f[2].split(".")

  num0 = int(g[0]) - 1

  return path.dirname(file) + "/" + f"{f[0]}_{f[1]}_{num0:06}.{g[1]}"


# print( fixFileExists("C:/IMG_9876542_101213.jpg") )