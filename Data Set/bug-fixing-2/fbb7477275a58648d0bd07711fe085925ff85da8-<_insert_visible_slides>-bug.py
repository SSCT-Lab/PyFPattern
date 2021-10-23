

def _insert_visible_slides(self, _next_slide=None, _prev_slide=None):
    get_slide_container = self.get_slide_container
    previous_slide = (_prev_slide if _prev_slide else self.previous_slide)
    if previous_slide:
        self._prev = get_slide_container(previous_slide)
    else:
        self._prev = None
    current_slide = self.current_slide
    if current_slide:
        self._current = get_slide_container(current_slide)
    else:
        self._current = None
    next_slide = (_next_slide if _next_slide else self.next_slide)
    if next_slide:
        self._next = get_slide_container(next_slide)
    else:
        self._next = None
    super_remove = super(Carousel, self).remove_widget
    for container in self.slides_container:
        super_remove(container)
    if self._prev:
        super(Carousel, self).add_widget(self._prev)
    if self._next:
        super(Carousel, self).add_widget(self._next)
    if self._current:
        super(Carousel, self).add_widget(self._current)
