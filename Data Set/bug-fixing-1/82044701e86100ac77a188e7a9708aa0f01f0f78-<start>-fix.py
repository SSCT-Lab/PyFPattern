

def start(win, ctx):
    from kivy.input.postproc import kivy_postproc_modules
    kivy_postproc_modules['fps'] = StatsInput()
    global _ctx
    ctx.label = Label(text='FPS: 0.0')
    ctx.inputstats = 0
    ctx.stats = []
    ctx.statsr = []
    with win.canvas.after:
        ctx.color = Color(1, 0, 0, 0.5)
        ctx.overlay = Rectangle(pos=(0, (win.height - 25)), size=(win.width, 25))
        ctx.color = Color(1, 1, 1)
        ctx.rectangle = Rectangle(pos=(5, (win.height - 20)))
        ctx.color = Color(1, 1, 1, 0.5)
        for i in range(64):
            ctx.stats.append(0)
            ctx.statsr.append(Rectangle(pos=(((win.width - (64 * 4)) + (i * 4)), (win.height - 25)), size=(4, 0)))
    win.bind(size=partial(_update_monitor_canvas, win, ctx))
    Clock.schedule_interval(partial(update_fps, ctx), 0.5)
    Clock.schedule_interval(partial(update_stats, win, ctx), (1 / 60.0))
