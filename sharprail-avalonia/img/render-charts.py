from playwright.sync_api import sync_playwright
src = "file:///Users/commandertvis/.thinkrail/worktrees/thinkrail/riirn/apps/native/benchmark-report.html"
out = "/Users/commandertvis/writing/sharprail-avalonia/img"
PAD = 24
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    for scheme in ("dark", "light"):
        pg = b.new_page(viewport={"width": 1300, "height": 1400}, device_scale_factor=2, color_scheme=scheme)
        pg.goto(src)
        box = lambda sel: pg.locator(sel).bounding_box()
        lg, ov, mem = box("div.legend"), box("section.overview"), box("section.mem")
        vw = pg.evaluate("document.documentElement.scrollWidth")
        # legend + timeline, full page width so the right axis labels are not cut
        top = lg["y"] - 6
        pg.screenshot(path=f"{out}/benchmark-startup-{scheme}.png", full_page=True,
                      clip={"x": 0, "y": top, "width": vw, "height": ov["y"] + ov["height"] + PAD - top})
        pg.screenshot(path=f"{out}/benchmark-footprint-{scheme}.png", full_page=True,
                      clip={"x": 0, "y": mem["y"] - 4, "width": vw, "height": mem["height"] + PAD + 4})
        pg.close()
    b.close()
