

def paintEvent(self, event):
    'Copy the image from the Agg canvas to the qt.drawable.\n\n        In Qt, all drawing should be done inside of here when a widget is\n        shown onscreen.\n        '
    if self._update_dpi():
        return
    self._draw_idle()
    if (not hasattr(self, 'renderer')):
        return
    painter = QtGui.QPainter(self)
    if self._erase_before_paint:
        painter.eraseRect(self.rect())
        self._erase_before_paint = False
    rect = event.rect()
    left = rect.left()
    top = rect.top()
    width = rect.width()
    height = rect.height()
    bbox = Bbox([[left, (self.renderer.height - (top + (height * self._dpi_ratio)))], [(left + (width * self._dpi_ratio)), (self.renderer.height - top)]])
    reg = self.copy_from_bbox(bbox)
    buf = reg.to_string_argb()
    qimage = QtGui.QImage(buf, (width * self._dpi_ratio), (height * self._dpi_ratio), QtGui.QImage.Format_ARGB32)
    if hasattr(qimage, 'setDevicePixelRatio'):
        qimage.setDevicePixelRatio(self._dpi_ratio)
    origin = QtCore.QPoint(left, top)
    painter.drawImage((origin / self._dpi_ratio), qimage)
    if (QT_API == 'PySide'):
        ctypes.c_long.from_address(id(buf)).value = 1
    self._draw_rect_callback(painter)
    painter.end()
