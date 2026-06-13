from manim import *

class StableDiffusionScene(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # 1. Transition from Latent Diffusion
        banner = Rectangle(width=config.frame_width, height=1.0, fill_color="#1D4370", fill_opacity=1, stroke_width=0)
        banner.to_edge(UP, buff=0)
        
        # Start with Latent Diffusion Title, then transform to Stable Diffusion
        title_ld = Text("Latent Diffusion", font_size=40, color=WHITE, font="sans-serif")
        title_ld.move_to(banner.get_left() + RIGHT * 0.5, aligned_edge=LEFT)
        
        self.play(FadeIn(banner, shift=DOWN), Write(title_ld))
        self.wait(0.5)

        title_sd = Text("Stable Diffusion", font_size=40, color=WHITE, font="sans-serif")
        title_sd.move_to(banner.get_left() + RIGHT * 0.5, aligned_edge=LEFT)
        
        self.play(ReplacementTransform(title_ld, title_sd))
        self.wait(0.5)

        subtitle = Text("Conditional/unconditional image generation", font_size=24, color="#1D4370", font="sans-serif")
        subtitle.next_to(banner, DOWN, buff=0.2).align_to(title_sd, LEFT)
        self.play(Write(subtitle))

        # 2. Pipeline Construction
        # Pixel Space (Left)
        pixel_bg = RoundedRectangle(width=2.5, height=5.0, corner_radius=0.5, fill_color="#F8D4D4", fill_opacity=1, stroke_color="#E0A0A0", stroke_width=3)
        pixel_bg.move_to(LEFT * 4.5 + DOWN * 0.5)
        pixel_text = Text("Pixel Space", font_size=20, color=BLACK, font="sans-serif", weight=BOLD).move_to(pixel_bg.get_bottom() + UP * 0.4)

        # Latent Space (Middle)
        latent_bg = RoundedRectangle(width=6.5, height=5.0, corner_radius=0.5, fill_color="#D2EEDB", fill_opacity=1, stroke_color="#A0CBA0", stroke_width=3)
        latent_bg.move_to(ORIGIN + DOWN * 0.5)
        latent_text = Text("Latent Space", font_size=24, color=BLACK, font="sans-serif", weight=BOLD).move_to(latent_bg.get_top() + DOWN * 0.4)

        self.play(FadeIn(pixel_bg), FadeIn(pixel_text), FadeIn(latent_bg), FadeIn(latent_text))

        # Encoders in Pixel Space
        def create_block(text, color, width=0.8, height=1.0):
            box = Rectangle(width=width, height=height, fill_color=color, fill_opacity=0.3, stroke_color=color, stroke_width=2)
            lbl = Text(text, font_size=24, color=BLACK, font="sans-serif").move_to(box)
            return VGroup(box, lbl)

        def create_trapezoid(text, is_encoder=True):
            h1, h2 = (1.5, 0.8) if is_encoder else (0.8, 1.5)
            poly = Polygon(
                [-0.6, h1/2, 0], [0.6, h2/2, 0], [0.6, -h2/2, 0], [-0.6, -h1/2, 0],
                fill_color="#D3E3F3", fill_opacity=1, stroke_color="#1D4370", stroke_width=2
            )
            lbl = Text(text, font_size=24, color=BLACK, font="sans-serif", slant=ITALIC).move_to(poly)
            return VGroup(poly, lbl)

        x_in = create_block("x", "#E0A0A0").move_to(pixel_bg.get_center() + UP * 1.5 + LEFT * 0.6)
        enc_e = create_trapezoid("E", is_encoder=True).next_to(x_in, RIGHT, buff=0.1)
        
        x_out = create_block("~x", "#E0A0A0").move_to(pixel_bg.get_center() + DOWN * 1.0 + LEFT * 0.6)
        dec_d = create_trapezoid("D", is_encoder=False).next_to(x_out, RIGHT, buff=0.1)
        dec_d.flip() # Point left
        x_out.next_to(dec_d, LEFT, buff=0.1)

        pixel_group = VGroup(x_in, enc_e, x_out, dec_d)
        self.play(FadeIn(pixel_group))

        # Latent Space internals
        diff_proc = RoundedRectangle(width=2.5, height=0.6, corner_radius=0.3, fill_color="#D2EEDB", fill_opacity=1, stroke_color=BLACK, stroke_width=1)
        diff_text = Text("Diffusion Process", font_size=18, color=BLACK, font="sans-serif").move_to(diff_proc)
        diff_group = VGroup(diff_proc, diff_text).move_to(latent_bg.get_center() + UP * 1.5)

        z_label = Text("z", font_size=20, color=BLACK, font="sans-serif", slant=ITALIC).next_to(latent_bg.get_left() + UP * 1.5, RIGHT, buff=0.1)
        zT_label = Text("zT", font_size=20, color=BLACK, font="sans-serif", slant=ITALIC).next_to(latent_bg.get_right() + UP * 1.5, LEFT, buff=0.1)
        
        arr_z1 = Arrow(z_label.get_right(), diff_group.get_left(), buff=0.1, color=BLACK, stroke_width=2, max_tip_length_to_length_ratio=0.1)
        arr_z2 = Arrow(diff_group.get_right(), zT_label.get_left(), buff=0.1, color=BLACK, stroke_width=2, max_tip_length_to_length_ratio=0.1)
        
        # Link from E to z
        arr_ez = Arrow(enc_e.get_right(), z_label.get_left(), buff=0.1, color=BLACK, stroke_width=2, max_tip_length_to_length_ratio=0.1)

        self.play(GrowArrow(arr_ez), FadeIn(z_label), GrowArrow(arr_z1), FadeIn(diff_group), GrowArrow(arr_z2), FadeIn(zT_label))

        # Denoising U-Net
        unet_bg = RoundedRectangle(width=6.0, height=2.2, corner_radius=0.2, fill_color="#E8F4E8", fill_opacity=1, stroke_color="#A0CBA0", stroke_width=2)
        unet_bg.move_to(latent_bg.get_center() + DOWN * 0.8)
        unet_text = Text("Denoising U-Net", font_size=20, color=BLACK, font="sans-serif").move_to(unet_bg.get_top() + DOWN * 0.3)
        
        self.play(FadeIn(unet_bg), FadeIn(unet_text))

        # QKV blocks inside U-Net
        qkv_blocks = VGroup()
        for i in range(4):
            qkv_bg = Rectangle(width=0.8, height=1.0, fill_color="#FFF0C0", fill_opacity=1, stroke_color="#E0B040", stroke_width=2)
            q_txt = Text("Q", font_size=16, color=BLACK, font="sans-serif", weight=BOLD).move_to(qkv_bg.get_top() + DOWN * 0.25)
            kv_txt = Text("K V", font_size=16, color=BLACK, font="sans-serif", weight=BOLD).move_to(qkv_bg.get_bottom() + UP * 0.25)
            qkv_blocks.add(VGroup(qkv_bg, q_txt, kv_txt))
        
        qkv_blocks.arrange(RIGHT, buff=0.25).move_to(unet_bg.get_center() + DOWN * 0.2)
        self.play(FadeIn(qkv_blocks))

        # Reverse arrows through U-Net
        zT_bot = Text("zT", font_size=20, color=BLACK, font="sans-serif", slant=ITALIC).move_to(unet_bg.get_right() + LEFT * 0.3)
        arr_zT_down = Arrow(zT_label.get_bottom(), zT_bot.get_top(), buff=0.1, color=BLACK, stroke_width=2, max_tip_length_to_length_ratio=0.1)
        self.play(GrowArrow(arr_zT_down), FadeIn(zT_bot))

        # Arrow path backwards through QKVs
        path_arrows = VGroup()
        prev_left = zT_bot.get_left()
        for block in reversed(qkv_blocks):
            arr = Arrow(prev_left, block.get_right(), buff=0, color=BLACK, stroke_width=2, max_tip_length_to_length_ratio=0.15)
            path_arrows.add(arr)
            prev_left = block.get_left()
        
        z_out = Text("z", font_size=20, color=BLACK, font="sans-serif", slant=ITALIC).move_to(unet_bg.get_left() + RIGHT * 0.3)
        arr_final = Arrow(prev_left, z_out.get_right(), buff=0, color=BLACK, stroke_width=2, max_tip_length_to_length_ratio=0.15)
        path_arrows.add(arr_final)

        self.play(*[GrowArrow(arr) for arr in path_arrows])
        self.play(FadeIn(z_out))

        # Feedback loop outside U-Net
        loop_arr = Arrow(z_out.get_top(), qkv_blocks[0].get_top() + LEFT*0.5, buff=0, color=BLACK, stroke_width=2)
        self.play(Create(loop_arr))
        
        # Connect z_out to Decoder
        arr_zD = Arrow(z_out.get_left(), dec_d.get_right(), buff=0.1, color=BLACK, stroke_width=2, max_tip_length_to_length_ratio=0.1)
        self.play(GrowArrow(arr_zD))

        # Conditioning Block (Right)
        cond_bg = RoundedRectangle(width=2.5, height=5.0, corner_radius=0.5, fill_color="#F0F0F0", fill_opacity=1, stroke_color=BLACK, stroke_width=2)
        cond_bg.move_to(RIGHT * 5.0 + DOWN * 0.5)
        cond_text = Text("Conditioning", font_size=20, color=BLACK, font="sans-serif", weight=BOLD).move_to(cond_bg.get_top() + DOWN * 0.4)
        
        self.play(FadeIn(cond_bg), FadeIn(cond_text))

        # Cond Inputs
        sem_map = RoundedRectangle(width=1.5, height=0.6, corner_radius=0.2, fill_color="#F8D4D4", fill_opacity=1, stroke_color="#E0A0A0")
        sem_txt = Text("Semantic\nMap", font_size=14, color=BLACK, font="sans-serif").move_to(sem_map)
        sem_grp = VGroup(sem_map, sem_txt)

        txt_map = RoundedRectangle(width=1.0, height=0.5, corner_radius=0.2, fill_color="#FFF0C0", fill_opacity=1, stroke_color="#E0B040")
        txt_txt = Text("Text", font_size=14, color=BLACK, font="sans-serif").move_to(txt_map)
        txt_grp = VGroup(txt_map, txt_txt)

        rep_map = RoundedRectangle(width=1.6, height=0.6, corner_radius=0.2, fill_color="#D2EEDB", fill_opacity=1, stroke_color="#A0CBA0")
        rep_txt = Text("Representations", font_size=14, color=BLACK, font="sans-serif").move_to(rep_map)
        rep_grp = VGroup(rep_map, rep_txt)

        img_map = RoundedRectangle(width=1.2, height=0.5, corner_radius=0.2, fill_color="#D3C1DF", fill_opacity=1, stroke_color="#A090B0")
        img_txt = Text("Images", font_size=14, color=BLACK, font="sans-serif").move_to(img_map)
        img_grp = VGroup(img_map, img_txt)

        cond_inputs = VGroup(sem_grp, txt_grp, rep_grp, img_grp).arrange(DOWN, buff=0.1).move_to(cond_bg.get_center() + UP * 1.0)
        txt_grp.shift(RIGHT * 0.5) # stagger slightly

        self.play(FadeIn(cond_inputs))

        # Tau_theta Encoder
        tau_enc = create_trapezoid("t", is_encoder=True)
        # Flip it to point left
        tau_enc.rotate(PI)
        tau_enc.move_to(cond_bg.get_bottom() + UP * 1.2)
        
        # Connect cond to tau
        path_c = Arrow(cond_inputs.get_bottom(), tau_enc.get_top() + RIGHT*0.2, buff=0, color="#A0A0A0", stroke_width=2)
        self.play(FadeIn(tau_enc), Create(path_c))

        # Cross attention arrows from tau_enc to QKV
        cross_arrows = VGroup()
        tau_out = tau_enc.get_left()
        for block in qkv_blocks:
            kv_bot = block[2].get_bottom()
            arr = Arrow(start=tau_out, end=kv_bot, buff=0, color=BLACK, stroke_width=2, max_tip_length_to_length_ratio=0.1)
            cross_arrows.add(arr)

        self.play(Create(cross_arrows))
        self.wait(2)

        # Phase 3: Generated Examples Showcase
        all_pipeline = VGroup(
            pixel_bg, pixel_text, latent_bg, latent_text, cond_bg, cond_text,
            pixel_group, diff_group, z_label, zT_label, arr_z1, arr_z2, arr_ez,
            unet_bg, unet_text, qkv_blocks, zT_bot, arr_zT_down, path_arrows, z_out,
            loop_arr, arr_zD, cond_inputs, tau_enc, path_c, cross_arrows
        )
        self.play(FadeOut(all_pipeline))

        # Example Images
        minion = ImageMobject("sd_minion.png")
        astronaut = ImageMobject("sd_astronaut.png")
        cyberpunk = ImageMobject("sd_cyberpunk.png")

        # Scale them
        for img in [minion, astronaut, cyberpunk]:
            img.height = 3.5
            
        examples_group = Group(minion, astronaut, cyberpunk).arrange(RIGHT, buff=0.5)
        examples_group.move_to(DOWN * 0.5)

        # Labels
        lbl_minion = Text("3D Minion Render", font_size=16, color=BLACK, font="sans-serif").next_to(minion, DOWN)
        lbl_astro = Text("Astronaut on Mars", font_size=16, color=BLACK, font="sans-serif").next_to(astronaut, DOWN)
        lbl_cyber = Text("Cyberpunk Street", font_size=16, color=BLACK, font="sans-serif").next_to(cyberpunk, DOWN)

        self.play(FadeIn(minion, shift=UP), FadeIn(lbl_minion))
        self.play(FadeIn(astronaut, shift=UP), FadeIn(lbl_astro))
        self.play(FadeIn(cyberpunk, shift=UP), FadeIn(lbl_cyber))
        self.wait(3)

        self.play(FadeOut(Group(banner, title_sd, subtitle, examples_group, lbl_minion, lbl_astro, lbl_cyber)))
        self.wait(1)

# Run this specific scene:
# manim -pql stable_diffusion_animation.py StableDiffusionScene
