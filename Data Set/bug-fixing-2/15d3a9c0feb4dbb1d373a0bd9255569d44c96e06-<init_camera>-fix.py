

def init_camera(self):
    if (self.opencvMajorVersion == 3):
        PROPERTY_WIDTH = cv2.CAP_PROP_FRAME_WIDTH
        PROPERTY_HEIGHT = cv2.CAP_PROP_FRAME_HEIGHT
        PROPERTY_FPS = cv2.CAP_PROP_FPS
    elif (self.opencvMajorVersion == 2):
        PROPERTY_WIDTH = cv2.cv.CV_CAP_PROP_FRAME_WIDTH
        PROPERTY_HEIGHT = cv2.cv.CV_CAP_PROP_FRAME_HEIGHT
        PROPERTY_FPS = cv2.cv.CV_CAP_PROP_FPS
    elif (self.opencvMajorVersion == 1):
        PROPERTY_WIDTH = cv.CV_CAP_PROP_FRAME_WIDTH
        PROPERTY_HEIGHT = cv.CV_CAP_PROP_FRAME_HEIGHT
        PROPERTY_FPS = cv.CV_CAP_PROP_FPS
    Logger.debug(('Using opencv ver.' + str(self.opencvMajorVersion)))
    if (self.opencvMajorVersion == 1):
        self._device = hg.cvCreateCameraCapture(self._index)
        cv.SetCaptureProperty(self._device, cv.CV_CAP_PROP_FRAME_WIDTH, self.resolution[0])
        cv.SetCaptureProperty(self._device, cv.CV_CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        frame = hg.cvQueryFrame(self._device)
        self._resolution = (int(frame.width), int(frame.height))
        self.fps = cv.GetCaptureProperty(self._device, cv.CV_CAP_PROP_FPS)
    elif ((self.opencvMajorVersion == 2) or (self.opencvMajorVersion == 3)):
        self._device = cv2.VideoCapture(self._index)
        self._device.set(PROPERTY_WIDTH, self.resolution[0])
        self._device.set(PROPERTY_HEIGHT, self.resolution[1])
        (ret, frame) = self._device.read()
        self._resolution = (int(frame.shape[1]), int(frame.shape[0]))
        self.fps = self._device.get(PROPERTY_FPS)
    if ((self.fps == 0) or (self.fps == 1)):
        self.fps = (1 / 30)
    elif (self.fps > 1):
        self.fps = (1 / self.fps)
    if (not self.stopped):
        self.start()
