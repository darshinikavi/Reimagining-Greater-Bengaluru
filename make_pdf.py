import asyncio
import os
from playwright.async_api import async_playwright

async def generate_pdf():
    file_path = f"file:///{os.path.abspath('index 24.html').replace('\\\\', '/')}"
    output_pdf = "Malgudi_Antigravity_Presentation.pdf"
    
    print(f"Opening {file_path}...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # 16:9 ratio for a good landscape PDF
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        
        # We emulate "screen" so we get the dark backgrounds and exact colors,
        # instead of the browser applying default print styles
        await page.emulate_media(media="screen")
        
        await page.goto(file_path, wait_until="networkidle")
        
        print("Page loaded. Scrolling to trigger animations and lazy load videos...")
        
        # Scroll down smoothly to trigger GSAP animations
        # We scroll down in increments of 1000px, waiting a bit
        last_scroll_y = 0
        scroll_height = await page.evaluate("document.body.scrollHeight")
        while last_scroll_y < scroll_height:
            last_scroll_y += 1000
            await page.evaluate(f"window.scrollTo(0, {last_scroll_y})")
            await page.wait_for_timeout(500)
            # update scroll height in case it expanded
            scroll_height = await page.evaluate("document.body.scrollHeight")
            
        print("Waiting for animations to settle...")
        await page.wait_for_timeout(2000)
        
        print("Converting videos to static images for the PDF...")
        # A known issue with PDFs is that <video> tags often render blank.
        # This JS snippet replaces videos with canvas images showing their current frame!
        await page.evaluate("""
            const videos = document.querySelectorAll('video');
            videos.forEach(v => {
                const canvas = document.createElement('canvas');
                canvas.width = v.videoWidth || v.clientWidth;
                canvas.height = v.videoHeight || v.clientHeight;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(v, 0, 0, canvas.width, canvas.height);
                canvas.style.cssText = v.style.cssText;
                canvas.className = v.className;
                canvas.style.objectFit = 'cover';
                v.parentNode.insertBefore(canvas, v);
                v.style.display = 'none';
            });
        """)
        
        # Inject custom CSS to make it print beautifully across pages
        # This attempts to fix pinned GSAP sections stretching too much
        await page.add_style_tag(content="""
            /* Hide UI elements you don't want in the PDF */
            #panel-toggle, .map-controls { display: none !important; }
            
            /* Break sections onto new pages nicely */
            section {
                page-break-after: always;
                break-after: page;
            }
        """)

        print(f"Generating {output_pdf}... This may take a moment.")
        
        # Generate the PDF in Landscape mode, A4 or custom size
        await page.pdf(
            path=output_pdf,
            format="A4",
            landscape=True,
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}
        )
        
        await browser.close()
        print(f"Done! PDF saved to {os.path.abspath(output_pdf)}")

if __name__ == "__main__":
    asyncio.run(generate_pdf())
