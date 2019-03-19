import cv2
import os

def extractFrames(pathIn, filename):

    cap = cv2.VideoCapture(pathIn)
    count = 1

    while (cap.isOpened()):

        # Capture frame-by-frame
        ret, frame = cap.read()

        if ret == True and count%24==0 :
            #print('Read %d frame: ' % count, ret)
            cv2.imwrite("{}{}frame{:d}.jpg".format(filename, "_" , count), frame)  # save frame as JPEG file
            count+=1
        else:
            count+=1

        if ret == False:
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def main():
    root = "Video"
    filepaths = [os.path.join(root,i) for i in os.listdir(root)]
    for path in filepaths:
        nama_video = os.path.basename(path)
        nama_video = os.path.splitext(nama_video)[0]
        extractFrames(path, nama_video)

if __name__=="__main__":
    main()
