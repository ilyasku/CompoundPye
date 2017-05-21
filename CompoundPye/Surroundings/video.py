## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 01.12.14

"""
@package CompoundPye.src.Surroundings.video
VIDEO SUPPORT?
@todo comment file
"""

import cv2

from . import surroundings


class VideoSurroundings(surroundings.Surroundings):

    def __init__(self, video_file, intensity_dimension=1,
                 show=False, debug=False):
        self.cap = cv2.VideoCapture(str(video_file))

        self.ret, self.first_frame = self.cap.read()

        if debug:
            s = ""
            s += "Opening file `" + str(video_file) + "` for VideoSurroundings.\n"
            s += "self.ret = " + str(self.ret) + "\n"
            s += "self.first_frame = " + self.first_frame.__str__() + "\n"

            import sys
            sys.stdout.write(s)

        w = self.first_frame.shape[1]
        h = self.first_frame.shape[0]

        # fps = self.cap.get(5)

        self.t = 0

        self.ret = None
        self.show = show

        self.n_frame = 0

        self.intensity_dim = intensity_dimension

        surroundings.Surroundings.__init__(self, [w, h], intensity_dimension)

    def update(self, dt):

        self.t += dt

        if self.t > (self.cap.get(0)/1000.):
            self.n_frame += 1
            if self.first_frame is not None:
                self.ret, frame = self.cap.read()
            else:
                frame = self.first_frame
                self.first_frame = None

            if self.intensity_dim == 1:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            else:
                raise NotImplementedError("No color support so far (in VideoSurroundings.update)")
            if self.show:
                cv2.imshow('frame_input', gray)
            self.intensities[:, :, 0] = gray.transpose()/255.
            if self.show:
                cv2.waitKey(1)
            del frame
            del gray

    def close_file(self):
        if self.show:
            self.cap.release()

    def set_t(self, t):
        self.t = t
        self._update_reader_position()

    def _update_reader_position(self):
        raise NotImplementedError()
