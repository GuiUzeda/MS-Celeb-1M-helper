import os
import base64
import struct
import argparse

def main(args):
  base_path = args.dir
  if not os.path.exists(base_path):
    os.mkdir(base_path)
  bbox_file = open(base_path + '/bboxes.txt', 'w')

  files = [os.path.join(args.path,f) for f in os.listdir(args.path) if f.endswith(".tsv") ]

  for file in files:
      
    print "working on file {}".format(file.split("/")[-1])
    fid = open(file, "r")
    
  
    while True:
      
      line = fid.readline()
      
      if line:
        data_info = line.split('\t')
        # 0: Freebase MID (unique key for each entity)
        # 1: ImageSearchRank
        # 4: FaceID
        # 5: bbox
        # 6: img_data
        filename = data_info[0] + "/" + data_info[1] + "_" + data_info[4] + ".jpg"
        bbox = struct.unpack('ffff', data_info[5].decode("base64"))
        bbox_file.write(filename + " "+ (" ".join(str(bbox_value) for bbox_value  in bbox)) + "\n")

        img_data = data_info[6].decode("base64")
        output_file_path = base_path + "/" + filename 
        if os.path.exists(output_file_path):
          print  output_file_path + " exists"
        else:
          print  output_file_path
        output_path = os.path.dirname(output_file_path)
        if not os.path.exists(output_path):
          os.mkdir(output_path)

        img_file = open(output_file_path, 'w')
        img_file.write(img_data)
        img_file.close()
      else:
        break

    bbox_file.close()
    fid.close()


if __name__ == "__main__":
    cwd = os.getcwd()
    parser = argparse.ArgumentParser(description="A extractor script for the MS-Celeb-1M's croped DB")
    parser.add_argument("-p", "--path", help="Path to the downloaded data data",
                        default=os.path.join(cwd, "data"))
    parser.add_argument("-d","--dir", help="Directory where the images will be saved",
                    default=os.path.join(cwd, "images"))                    
    args = parser.parse_args()

    main(args)