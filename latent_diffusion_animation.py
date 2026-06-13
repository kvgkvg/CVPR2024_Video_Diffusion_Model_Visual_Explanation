from manim import *

class LatentDiffusionScene(Scene):
    def construct(self):
        # Background color
        self.camera.background_color = WHITE

        # 1. Top Banner & Title
        banner = Rectangle(width=config.frame_width, height=1.0, fill_color="#1D4370", fill_opacity=1, stroke_width=0)
        banner.to_edge(UP, buff=0)
        
        title = Text("Latent Diffusion", font_size=40, color=WHITE, font="sans-serif")
        title.move_to(banner.get_left() + RIGHT * 0.5, aligned_edge=LEFT)
        
        self.play(FadeIn(banner, shift=DOWN), Write(title))
        self.wait(0.5)

        # 2. Backdrops
        pixel_bg = RoundedRectangle(width=13.0, height=6.5, corner_radius=1.0, fill_color="#F8D4D4", fill_opacity=1, stroke_width=0)
        pixel_bg.move_to(DOWN * 0.2)
        
        pixel_text = Text("Pixel Space", font_size=28, color=BLACK, font="sans-serif")
        pixel_text.move_to(pixel_bg.get_top() + DOWN * 0.5)

        latent_bg = RoundedRectangle(width=6.5, height=3.0, corner_radius=1.0, fill_color="#D2EEDB", fill_opacity=1, stroke_width=0)
        latent_bg.move_to(DOWN * 1.5)
        
        latent_text = Text("Latent Space", font_size=24, color=BLACK, font="sans-serif")
        latent_text.move_to(latent_bg.get_top() + DOWN * 0.4)

        self.play(FadeIn(pixel_bg), FadeIn(pixel_text))
        self.wait(0.5)

        # Helper to create a pill node
        def create_pill(text, width=2.2, height=1.0):
            bg = RoundedRectangle(width=width, height=height, corner_radius=height/2, fill_color="#D3E3F3", fill_opacity=1, stroke_color="#A9C2DB", stroke_width=2)
            lbl = Text(text, font_size=20, color=BLACK, font="sans-serif").move_to(bg)
            return VGroup(bg, lbl)

        # Helper to create encoder/decoder
        def create_trapezoid(text, is_encoder=True):
            h1, h2 = (2.0, 0.8) if is_encoder else (0.8, 2.0)
            poly = Polygon(
                [-1.0, h1/2, 0], [1.0, h2/2, 0], [1.0, -h2/2, 0], [-1.0, -h1/2, 0],
                fill_color="#1D4370", fill_opacity=1, stroke_width=0
            )
            lbl = Text(text, font_size=20, color=WHITE, font="sans-serif").move_to(poly)
            return VGroup(poly, lbl)

        # Helper to create image box
        def create_image(path):
            img = ImageMobject(path)
            img.height = 1.8
            # Add a subtle border
            border = Rectangle(width=img.width, height=img.height, stroke_color=BLACK, stroke_width=1)
            return Group(img, border)

        # Y Coordinates
        y_pixel = 1.2
        y_latent = -1.5

        # 3. Upper Stream (Pixel Space)
        img_p1 = create_image("cat_image.png").move_to([-5.2, y_pixel, 0])
        noise_p = create_pill("Add Noise").move_to([-1.5, y_pixel, 0])
        denoise_p = create_pill("Denoise").move_to([1.5, y_pixel, 0])
        img_p2 = create_image("cat_image.png").move_to([5.2, y_pixel, 0])

        arr_p1 = Arrow(img_p1.get_right(), noise_p.get_left(), buff=0.1, color="#1D4370", stroke_width=4, max_tip_length_to_length_ratio=0.1)
        arr_p2 = Arrow(noise_p.get_right(), denoise_p.get_left(), buff=0.1, color="#1D4370", stroke_width=4, max_tip_length_to_length_ratio=0.1)
        arr_p3 = Arrow(denoise_p.get_right(), img_p2.get_left(), buff=0.1, color="#1D4370", stroke_width=4, max_tip_length_to_length_ratio=0.05)

        self.play(FadeIn(img_p1))
        self.play(GrowArrow(arr_p1))
        self.play(FadeIn(noise_p))
        self.play(GrowArrow(arr_p2))
        self.play(FadeIn(denoise_p))
        self.play(GrowArrow(arr_p3))
        self.play(FadeIn(img_p2))
        self.wait(1)

        # 4. Lower Stream (Latent Space)
        self.play(FadeIn(latent_bg), FadeIn(latent_text))
        
        img_l1 = create_image("cat_image.png").move_to([-5.2, y_latent, 0])
        enc = create_trapezoid("Encoder", is_encoder=True).move_to([-3.2, y_latent, 0])
        noise_l = create_pill("Add Noise").move_to([-1.5, y_latent, 0])
        denoise_l = create_pill("Denoise").move_to([1.5, y_latent, 0])
        dec = create_trapezoid("Decoder", is_encoder=False).move_to([3.2, y_latent, 0])
        img_l2 = create_image("cat_image.png").move_to([5.2, y_latent, 0])

        arr_l1 = Arrow(img_l1.get_right(), enc.get_left(), buff=0.1, color="#1D4370", stroke_width=4, max_tip_length_to_length_ratio=0.15)
        arr_l2 = Arrow(enc.get_right(), noise_l.get_left(), buff=0.1, color="#1D4370", stroke_width=4, max_tip_length_to_length_ratio=0.15)
        arr_l3 = Arrow(noise_l.get_right(), denoise_l.get_left(), buff=0.1, color="#1D4370", stroke_width=4, max_tip_length_to_length_ratio=0.1)
        arr_l4 = Arrow(denoise_l.get_right(), dec.get_left(), buff=0.1, color="#1D4370", stroke_width=4, max_tip_length_to_length_ratio=0.15)
        arr_l5 = Arrow(dec.get_right(), img_l2.get_left(), buff=0.1, color="#1D4370", stroke_width=4, max_tip_length_to_length_ratio=0.15)

        self.play(FadeIn(img_l1))
        self.play(GrowArrow(arr_l1))
        self.play(FadeIn(enc))
        self.play(GrowArrow(arr_l2))
        self.play(FadeIn(noise_l))
        self.play(GrowArrow(arr_l3))
        self.play(FadeIn(denoise_l))
        self.play(GrowArrow(arr_l4))
        self.play(FadeIn(dec))
        self.play(GrowArrow(arr_l5))
        self.play(FadeIn(img_l2))
        self.wait(2)

        # 5. Outro
        all_mobs = Group(
            banner, title, pixel_bg, pixel_text, latent_bg, latent_text,
            img_p1, noise_p, denoise_p, img_p2, arr_p1, arr_p2, arr_p3,
            img_l1, enc, noise_l, denoise_l, dec, img_l2, arr_l1, arr_l2, arr_l3, arr_l4, arr_l5
        )
        self.play(FadeOut(all_mobs))
        self.wait(1)

# Run this specific scene:
# manim -pql latent_diffusion_animation.py LatentDiffusionScene
