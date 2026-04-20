import pygame
import math
import random

# --- INITIALIZATION ---
pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("QUANTUM REALITY")
clock = pygame.time.Clock()

# --- FONTS ---
font_large = pygame.font.SysFont("Times New Roman", 40, bold=True)
font_small = pygame.font.SysFont("Times New Roman", 20)
font_msg = pygame.font.SysFont("Consolas", 18)

# --- VISIBLE SPECTRUM ---
def wavelength_to_rgb(wavelength):

    if not wavelength or wavelength == ".":
        return (255, 0, 0) 
        
    try:
        w = float(wavelength)
    except ValueError:
        return (255, 0, 0) 
    
    w = float(wavelength)
    if 380 <= w <= 440: R, G, B = -(w - 440) / (440 - 380), 0.0, 1.0
    elif 440 <= w <= 490: R, G, B = 0.0, (w - 440) / (490 - 440), 1.0
    elif 490 <= w <= 510: R, G, B = 0.0, 1.0, -(w - 510) / (510 - 490)
    elif 510 <= w <= 580: R, G, B = (w - 510) / (580 - 510), 1.0, 0.0
    elif 580 <= w <= 645: R, G, B = 1.0, -(w - 645) / (645 - 580), 0.0
    elif 645 <= w <= 750: R, G, B = 1.0, 0.0, 0.0
    else: R, G, B = 1.0, 1.0, 1.0
    factor = 1.0
    if 380 <= w < 420: factor = 0.3 + 0.7 * (w - 380) / (420 - 380)
    elif 700 < w <= 750: factor = 0.3 + 0.7 * (750 - w) / (750 - 700)
    return (int(R * factor * 255), int(G * factor * 255), int(B * factor * 255))

# --- GLOBAL PHYSICS CONSTANTS ---
state = "MENU" 
gap_size = 50.0   # For Slit
energy = 100.0    # For Tunneling
V0 = 250.0        # Barrier Height
ball_x = 350      # Particle position

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# --- MAIN LOOP ---
running = True
while running:
    screen.fill((15, 15, 25)) 
    
    # GRAB INPUTS
    events = pygame.event.get()
    mx, my = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
        
        # Scroll Wheel for Slit
        if event.type == pygame.MOUSEBUTTONDOWN and state == "DIFFRACTION":
            if event.button == 4: gap_size = min(150, gap_size + 2)
            if event.button == 5: gap_size = max(5, gap_size - 2)

    # --- STATE: MAIN MENU ---
    if state == "MENU":
        draw_text("QUANTUM REALITY", font_large, (0, 255, 200), 290, 100)
        draw_text("Press [1] for Single Slit (The Wave)", font_small, (255, 255, 255), 330, 250)
        draw_text("Press [2] for Quantum Well (Tunneling)", font_small, (255, 255, 255), 330, 300)
        draw_text("Press [3] for Compton Effect (The Particle)", font_small, (255, 255, 255), 330, 350)
        
        if keys[pygame.K_1]: state = "DIFFRACTION"
        if keys[pygame.K_2]: state = "TUNNEL"
        if keys[pygame.K_3]: state = "COMPTON"

    # ----------------------------------------------- STATE: SINGLE SLIT DIFFRACTION -------------------------------------------
    elif state == "DIFFRACTION":
        draw_text("Single Slit Diffraction", font_large, (255, 255, 255), 300, 40)

        # --- SETUP ---
        if 's_init' not in locals():
            s_init = True
            s_slit_width = "0.04"
            s_wavelength = "650"
            s_distance = "1000"
            s_angle_input = "0.5"
            s_active_box = None

        current_color = wavelength_to_rgb(s_wavelength)

        # --- PHYSICS CALCULATIONS ---
        try:
            a = float(s_slit_width) * 1e-3
            lam = float(s_wavelength) * 1e-9
            L = float(s_distance) * 1e-3
            theta_deg = float(s_angle_input)
            
            theta_rad = math.radians(theta_deg)
            y_mm = (L * math.tan(theta_rad)) * 1000
            
            beta_val = (math.pi * a * math.sin(theta_rad)) / lam
            if abs(beta_val) < 1e-9: current_intensity = 1.0
            else: current_intensity = (math.sin(beta_val) / beta_val)**2
        except: 
            y_mm, current_intensity = 0, 1.0

        # --- RENDERING THE SLIT ---
        slit_x = 100
        slit_center_y = HEIGHT // 2
        
        try: 
            vis_a = float(s_slit_width) * 500 
        except: 
            vis_a = 10
            
        vis_a = max(2, min(vis_a, 150)) 

        plate_length = 120 
        gap_half = vis_a // 2

        pygame.draw.rect(screen, (80, 80, 80), (
            slit_x - 10, 
            slit_center_y - gap_half - plate_length, 
            20, 
            plate_length
        ))

        pygame.draw.rect(screen, (80, 80, 80), (
            slit_x - 10, 
            slit_center_y + gap_half, 
            20, 
            plate_length
        ))
        
        draw_text("Slit", font_small, (200, 200, 200), slit_x - 15, slit_center_y - gap_half - plate_length - 25)

        # --- RENDERING PATTERN ---
        for screen_y in range(-200, 200):
            angle_at_pixel = math.atan(screen_y / 3500) 
            b = (math.pi * a * math.sin(angle_at_pixel)) / lam
            
            if abs(b) < 1e-9: intensity_at_pixel = 1.0
            else: intensity_at_pixel = (math.sin(b) / b)**2
            
            # --- 3x Amplification for SCREEN VIEW ---
            screen_boost = 3.0
            faded_rgb = (
                min(int(current_color[0] * intensity_at_pixel * screen_boost), 255),
                min(int(current_color[1] * intensity_at_pixel * screen_boost), 255),
                min(int(current_color[2] * intensity_at_pixel * screen_boost), 255)
            )
            
            # Screen View 
            pygame.draw.line(screen, faded_rgb, (WIDTH - 500, HEIGHT//2 + screen_y), (WIDTH - 430, HEIGHT//2 + screen_y), 1)
            
            # Intensity Graph 
            graph_x = WIDTH - 400 + (intensity_at_pixel * 250)
            pygame.draw.circle(screen, current_color, (int(graph_x), HEIGHT//2 + screen_y), 1)

        draw_text("Screen", font_small, (200, 200, 200), WIDTH - 490, HEIGHT//2 - 230)
        draw_text("Intensity Graph", font_small, (200, 200, 200), WIDTH - 350, HEIGHT//2 - 230)

        # --- UI & INTERACTION ---
        ui_y = 620
        draw_text(f"Target y: {y_mm:.2f} mm", font_small, (255, 255, 255), 650, ui_y - 40)
        draw_text(f"Intensity: {current_intensity*100:.2f}%", font_small, current_color, 650, ui_y - 15)

        boxes = [
            {"l": "Slit Width (mm)", "v": s_slit_width, "id": "a", "r": pygame.Rect(50, ui_y, 130, 35)},
            {"l": "Wavelength (nm)", "v": s_wavelength, "id": "w", "r": pygame.Rect(200, ui_y, 130, 35)},
            {"l": "Distance L (mm)", "v": s_distance, "id": "L", "r": pygame.Rect(350, ui_y, 130, 35)},
            {"l": "Input Angle (°)", "v": s_angle_input, "id": "theta", "r": pygame.Rect(500, ui_y, 130, 35)}
        ]

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                s_active_box = None
                for b in boxes:
                    if b["r"].collidepoint(event.pos): s_active_box = b["id"]
            if event.type == pygame.KEYDOWN and s_active_box:
                if event.key == pygame.K_BACKSPACE:
                    if s_active_box == "a": s_slit_width = s_slit_width[:-1]
                    elif s_active_box == "w": s_wavelength = s_wavelength[:-1]
                    elif s_active_box == "L": s_distance = s_distance[:-1]
                    elif s_active_box == "theta": s_angle_input = s_angle_input[:-1]
                elif event.unicode in "0123456789.":
                    if s_active_box == "a": s_slit_width += event.unicode
                    elif s_active_box == "w": s_wavelength += event.unicode
                    elif s_active_box == "L": s_distance += event.unicode
                    elif s_active_box == "theta": s_angle_input += event.unicode

        for b in boxes:
            pygame.draw.rect(screen, (40, 40, 50), b["r"], border_radius=5)
            draw_text(b["l"], font_small, (180, 180, 180), b["r"].x, b["r"].y - 25)
            draw_text(b["v"] + ("|" if s_active_box == b["id"] else ""), font_small, (255, 255, 255), b["r"].x + 5, b["r"].y + 8)

    # ------------------------------------------- STATE: TUNNELING ---------------------------------------------------
    elif state == "TUNNEL":
        draw_text(" Quantum Tunneling ", font_large, (0, 255, 255), 325, 40)
        draw_text(f"Press spacebar to observe", font_small, (255, 255, 255), 400, 100)

        # --- SETUP ---
        if 't_init' not in locals():
            t_init = True
            t_barrier_height = "25.0" 
            t_particle_energy = "12.0" 
            t_active_box = None
            t_tunnel_count = 0
            t_attempts = 0
            t_ball_x = 250
            t_is_frozen = False 

        # --- THE PHYSICS ---
        try:
            v_val = float(t_barrier_height) if t_barrier_height else 1.0
            e_val = float(t_particle_energy) if t_particle_energy else 0.5

            L = 50.0 
            
            if e_val >= v_val:
                # If energy is greater than or equal to barrier, probability is 100%
                prob = 1.0 
                gamma = 0
            else:
                gamma = math.sqrt(v_val - e_val) * 0.05 
                prob = math.exp(-2 * gamma * L) 
                
        except: prob = 0

        # --- RENDERING PHYSICS VIEW ---
        sim_y = 500
        well_x = 400
        barrier_end = well_x + L
        ball_y = sim_y - (e_val * 10) # Ball tied to Energy E

        # Potential Barrier
        pts = [(100, sim_y), (well_x, sim_y), (well_x, sim_y - v_val*10), 
               (barrier_end, sim_y - v_val*10), (barrier_end, sim_y), (WIDTH-100, sim_y)]
        pygame.draw.lines(screen, (255, 255, 255), False, pts, 3)

        # Norm Squared Wavefunction 
        points = []
        for x in range(100, WIDTH - 100):
            if x < well_x:
                h = (math.sin(x * 0.1)**2) * 60 
            elif x < barrier_end:
                h = 60 * math.exp(-2 * gamma * (x - well_x)) 
            else:
                transmission_const = 60 * math.exp(-2 * gamma * L)
                visual_boost = 5 if transmission_const > 0.1 else 0
                total_amp = transmission_const + visual_boost
                h = (math.sin(x * 0.1 )**2) * total_amp
                h = max(h, 3)
            points.append((x, ball_y - h))

        if len(points) > 2:
            pygame.draw.lines(screen, (0, 255, 255), False, points, 2)
            surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            poly = [(100, ball_y)] + points + [(WIDTH-100, ball_y)]
            pygame.draw.polygon(surf, (0, 255, 255, 40), poly)
            screen.blit(surf, (0,0))

        # The Particle (The Ball)
        pygame.draw.circle(screen, (255, 255, 0), (int(t_ball_x), int(ball_y - 5)), 12)

        # --- BUTTONS & UI ---
        
        reset_btn_rect = pygame.Rect(WIDTH - 305, 215, 130, 40)
        continue_btn_rect = pygame.Rect(WIDTH - 160, 215, 130, 40)
        if t_is_frozen:
            pygame.draw.rect(screen, (200, 50, 50), reset_btn_rect, border_radius=5)
            draw_text("RESET SIM", font_small, (255, 255, 255), reset_btn_rect.x + 15, 225)

            pygame.draw.rect(screen, (50, 200, 50), continue_btn_rect, border_radius=5)
            draw_text("CONTINUE", font_small, (255, 255, 255), continue_btn_rect.x + 15, 225)

        # Observe & Inputs
        ui_y = 620
        observe_btn = pygame.Rect(450, ui_y, 140, 35)
        
        # Disable Observe button visually if frozen
        obs_color = (0, 150, 150) if not t_is_frozen else (60, 60, 60)
        pygame.draw.rect(screen, obs_color, observe_btn, border_radius=5)
        draw_text("OBSERVE", font_small, (255, 255, 255), 480, ui_y + 8)

        boxes = [
            {"l": "V0 (Barrier) MeV", "v": t_barrier_height, "id": "v0", "r": pygame.Rect(100, ui_y, 130, 35)},
            {"l": "E (Particle) MeV", "v": t_particle_energy, "id": "e", "r": pygame.Rect(260, ui_y, 130, 35)}
        ]

       # --- INTERACTION LOGIC ---
        
        # MONITOR FOR CHANGES 
        if 'last_v' not in locals(): last_v, last_e = t_barrier_height, t_particle_energy
        
        if t_barrier_height != last_v or t_particle_energy != last_e:
            t_ball_x = 250
            t_is_frozen = False
            last_v, last_e = t_barrier_height, t_particle_energy # Update the tracker

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Observe via Mouse
                if observe_btn.collidepoint(event.pos) and not t_is_frozen:
                    t_attempts += 1
                    if random.random() < prob:
                        t_ball_x = random.uniform(barrier_end + 30, WIDTH - 150)
                        t_tunnel_count += 1
                        t_is_frozen = True
                    else:
                        t_ball_x = random.uniform(150, well_x - 30)
                
                # Manual Continue/Reset
                if t_is_frozen:
                    if continue_btn_rect.collidepoint(event.pos):
                        t_ball_x = 250
                        t_is_frozen = False
                    if reset_btn_rect.collidepoint(event.pos):
                        t_ball_x = 250
                        t_attempts = 0
                        t_tunnel_count = 0
                        t_is_frozen = False

                # Box selection
                t_active_box = None
                for b in boxes:
                    if b["r"].collidepoint(event.pos): t_active_box = b["id"]

            if event.type == pygame.KEYDOWN:
                # Observe via Spacebar
                if event.key == pygame.K_SPACE and not t_is_frozen:
                    t_attempts += 1
                    if random.random() < prob:
                        t_ball_x = random.uniform(barrier_end + 30, WIDTH - 150)
                        t_tunnel_count += 1
                        t_is_frozen = True
                    else:
                        t_ball_x = random.uniform(150, well_x - 30)

                # Text Input
                elif t_active_box:
                    if event.key == pygame.K_BACKSPACE:
                        if t_active_box == "v0": t_barrier_height = t_barrier_height[:-1]
                        else: t_particle_energy = t_particle_energy[:-1]
                    elif event.unicode in "0123456789.":
                        if t_active_box == "v0": t_barrier_height += event.unicode
                        else: t_particle_energy += event.unicode

        # Render UI Elements
        for b in boxes:
            pygame.draw.rect(screen, (30, 30, 40), b["r"])
            draw_text(b["l"], font_small, (200, 200, 200), b["r"].x, b["r"].y - 25)
            draw_text(b["v"] + ("|" if t_active_box == b["id"] else ""), font_small, (255,255,255), b["r"].x+5, b["r"].y+8)

        # --- STATS ---
        stats_x = WIDTH - 280
        draw_text(f"Observations: {t_attempts}", font_small, (255, 255, 255), stats_x, 560)
        draw_text(f"Tunnel Events: {t_tunnel_count}", font_small, (255, 255, 0), stats_x, 590)
        draw_text(f"Tunnel Prob: {prob*100:.2f}%", font_small, (0, 255, 200), stats_x, 620)

        if t_is_frozen:
            draw_text("TUNNELING DETECTED ", font_large, (255, 50, 50), 100, 130)
        

    # -------------------------------------------------- STATE: COMPTON ---------------------------------------------------------
    elif state == "COMPTON":
        draw_text("Compton Effect", font_large, (255, 200, 0), 375, 50)
        draw_text("Δλ = λ_c(1 - cosθ) ", font_msg, (200, 200, 200), 425, 100)

        # --- SETUP AND INITIALIZATION ---
        sim_y = 450 
        if 'c_stage' not in locals(): 
            c_stage = "IDLE"
            c_angle_str = "50"
            c_lambda_str = "500" # Initial wavelength in nm 
            c_input_active = None 
            c_photon_pos = [0.0, 0.0]
            c_electron_pos = [0.0, 0.0]
            c_color = (0, 255, 0)
            c_collision_frame = 0
            c_photon_trail = [] 
            c_electron_trail = []
            c_res_delta = 0.0
            c_res_phi = 0.0

        # --- REAL-TIME COLOR MAPPING ---
        if c_stage in ["IDLE", "APPROACHING"]:
            try:
                c_color = wavelength_to_rgb(c_lambda_str)
            except:
                c_color = (200, 200, 200)

        # --- UI: INPUT BOXES ---
        angle_rect = pygame.Rect(50, 150, 120, 40)
        pygame.draw.rect(screen, (80, 80, 100) if c_input_active == "angle" else (40, 40, 50), angle_rect)
        pygame.draw.rect(screen, (0, 255, 200), angle_rect, 2)
        draw_text(c_angle_str + ("|" if c_input_active == "angle" else ""), font_msg, (255, 255, 255), 60, 160)
        draw_text("Angle θ (0-180):", font_small, (255, 255, 255), 50, 120)

        lam_rect = pygame.Rect(200, 150, 120, 40)
        pygame.draw.rect(screen, (80, 80, 100) if c_input_active == "lam" else (40, 40, 50), lam_rect)
        pygame.draw.rect(screen, (0, 255, 200), lam_rect, 2)
        draw_text(c_lambda_str + ("|" if c_input_active == "lam" else ""), font_msg, (255, 255, 255), 210, 160)
        draw_text("Initial λ (nm):", font_small, (255, 255, 255), 200, 120)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if angle_rect.collidepoint(event.pos): c_input_active = "angle"
                elif lam_rect.collidepoint(event.pos): c_input_active = "lam"
                else: c_input_active = None
            if event.type == pygame.KEYDOWN and c_input_active:
                if event.key == pygame.K_BACKSPACE:
                    if c_input_active == "angle": c_angle_str = c_angle_str[:-1]
                    else: c_lambda_str = c_lambda_str[:-1]
                elif event.unicode in "0123456789.":
                    if c_input_active == "angle": c_angle_str += event.unicode
                    else: c_lambda_str += event.unicode

        run_btn = pygame.Rect(50, 210, 120, 45)
        pygame.draw.rect(screen, (0, 150, 100), run_btn, border_radius=8)
        draw_text("COLLIDE", font_small, (255, 255, 255), 75, 222)

        if click[0] and run_btn.collidepoint(mx, my):
            try:
                theta_deg = float(c_angle_str)
                lam_in_nm = float(c_lambda_str)
                theta_rad = math.radians(theta_deg)
                
                # --- PHYSICS ---
                h_mc = 0.00243 
                c_res_delta = h_mc * (1 - math.cos(theta_rad))
                
                # --- VISUAL BOOST ---
                #
                visual_shift = (theta_deg / 180) * 40  # Shifts up to 40nm redder
                lam_visual = lam_in_nm + visual_shift
                c_final_color = wavelength_to_rgb(str(lam_visual))
                # --- VISUAL BOOST ---
                # Multiply the real physics delta by a large factor (e.g., 25000) 
                # This scales the tiny nm shift into a visible hue change on the 400-700nm scale
                hue_shift = c_res_delta * 25000 
                lam_visual = lam_in_nm + hue_shift
                c_final_color = wavelength_to_rgb(str(lam_visual))
                # --- RECOIL MATH ---
                alpha = h_mc / lam_in_nm
                phi_rad = math.atan(math.sin(theta_rad) / ((1 + alpha) * (1 - math.cos(theta_rad))))
                c_res_phi = math.degrees(phi_rad)

                # --- RESET VECTORS ---
                c_stage = "APPROACHING"
                c_collision_frame = 0
                c_photon_pos = [-50.0, sim_y - 80]
                c_electron_pos = [float(WIDTH//2), sim_y - 80]
                c_photon_trail = [] 
                c_electron_trail = []
                c_recoil_vec = [math.cos(phi_rad) * 5, math.sin(phi_rad) * 5]
                c_scatter_vec = [math.cos(-theta_rad) * 9, math.sin(-theta_rad) * 9]
            except: pass

        # Atom Visuals
        center = (WIDTH//2, sim_y)
        pygame.draw.circle(screen, (220, 50, 50), center, 20) 
        pygame.draw.circle(screen, (100, 100, 100), center, 80, 1) 
        
        # --- PHYSICS ---
        if c_stage == "APPROACHING":
            c_photon_pos[0] += 14 
            if c_photon_pos[0] >= WIDTH//2: 
                c_stage = "SCATTERING"
                c_color = c_final_color 

        elif c_stage == "SCATTERING":
            if c_collision_frame % 3 == 0:
                c_photon_trail.append((int(c_photon_pos[0]), int(c_photon_pos[1])))
                c_electron_trail.append((int(c_electron_pos[0]), int(c_electron_pos[1])))

            c_photon_pos[0] += c_scatter_vec[0]
            c_photon_pos[1] += c_scatter_vec[1]
            c_electron_pos[0] += c_recoil_vec[0]
            c_electron_pos[1] += c_recoil_vec[1]
            
            c_collision_frame += 1
            if c_collision_frame > 40:
                c_stage = "DONE"

        # --- RENDER ---
        for p in c_photon_trail: pygame.draw.circle(screen, c_color, p, 2)
        for e in c_electron_trail: pygame.draw.circle(screen, (255, 255, 255), e, 2)

        pygame.draw.circle(screen, (255, 255, 0), (int(c_electron_pos[0]), int(c_electron_pos[1])), 10)
        px, py = int(c_photon_pos[0]), int(c_photon_pos[1])
        pygame.draw.circle(screen, c_color, (px, py), 12)
        
        # Wave Tail
        freq = 0.05
        for i in range(1, 7):
            off = i * 10
            wy = py + math.sin((px - off) * freq + pygame.time.get_ticks() * 0.015) * 12
            pygame.draw.circle(screen, c_color, (px - off, int(wy)), 3)

        if c_stage == "DONE":
            draw_text("SCATTERING FROZEN", font_msg, (0, 255, 0), WIDTH//2 - 80, sim_y + 110)
            draw_text(f"Shift Δλ: {c_res_delta:.6f} nm", font_small, (255, 255, 255), 50, 300)
            draw_text(f"Recoil φ: {c_res_phi:.2f}°", font_small, (255, 255, 0), 50, 330)

    # Back to menu logic
    if keys[pygame.K_m]: state = "MENU"
    if state != "MENU":
        draw_text("Press [M] for Menu", font_small, (100, 100, 100), 20, 20)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()