#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║           PHYSICS PLAYGROUND - Simulador de Físicas          ║
║  Arrastra objetos, láncalos y observa la física en acción!  ║
╚══════════════════════════════════════════════════════════════╝
"""

import pygame
import sys
import math
import time

# ─────────────────────────── INIT ───────────────────────────
pygame.init()

WIDTH, HEIGHT = 1280, 780
FPS = 60
DT = 1.0 / FPS         # Render/frame step (seconds)
FIXED_DT = 1.0 / 240.0  # Fixed physics step: framerate-independent, stable drag integration

# Ground material (hard floor): rigid and nearly elastic, like concrete/tile.
# The energy actually lost in a bounce comes mostly from the OBJECT, so the
# floor itself keeps a high restitution and the per-object e does the limiting.
FLOOR_RESTITUTION = 0.90   # coefficient of restitution e of the floor material
FLOOR_STIFFNESS = 200000.0  # very rigid -> the object's elasticity rules the bounce
FLOOR_CONTACT_TIME = 0.010  # s, short -> high peak force (rigid ground)
FLOOR_FRICTION = 0.80      # tangential velocity retained per bounce

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Playground — Simulador de Física I")

# ─────────────────────────── COLORS ─────────────────────────
BG           = (18, 18, 24)
PANEL_BG     = (26, 26, 36)
PANEL_BORDER = (50, 50, 70)
ACCENT       = (0, 200, 255)
ACCENT2      = (255, 100, 60)
ACCENT3      = (100, 255, 140)
WHITE        = (240, 240, 245)
GRAY         = (130, 130, 150)
DIM          = (70, 70, 90)
DARK         = (35, 35, 50)
YELLOW       = (255, 220, 60)
RED          = (255, 70, 70)
GREEN        = (70, 255, 120)
ORANGE       = (255, 160, 40)
PURPLE       = (180, 100, 255)
PINK         = (255, 100, 200)
CYAN         = (0, 220, 255)
SLIME_GREEN  = (50, 200, 80)
SLIME_BLUE   = (60, 120, 255)
SLIME_PURPLE = (160, 60, 220)
TRAMPOLINE   = (255, 60, 100)

# ─────────────────────────── FONTS ──────────────────────────
font_sm   = pygame.font.SysFont("consolas", 13)
font_md   = pygame.font.SysFont("consolas", 15, bold=True)
font_lg   = pygame.font.SysFont("consolas", 18, bold=True)
font_xl   = pygame.font.SysFont("consolas", 22, bold=True)
font_title = pygame.font.SysFont("consolas", 11)

# ─────────────────────────── PIXEL SCALE ────────────────────
# 1 meter = 80 pixels
PPM = 80.0  # pixels per meter

# Newton mode: separate, smaller scale (motion spans many meters horizontally)
NEWTON_PPM = 20.0        # pixels per meter for the Newton-mode sim area
NEWTON_G = 9.8            # m/s², matches Avance 1 document
NEWTON_ARROW_SCALE = 3.5  # px per Newton, for DCL vectors


def m_to_px(m):
    return m * PPM


def px_to_m(px):
    return px / PPM


def draw_arrow(surf, start, end, color, width=3, head=8):
    """Draw a line with a small triangular arrowhead from start to end (px coords)."""
    sx, sy = start
    ex, ey = end
    if math.hypot(ex - sx, ey - sy) < 1e-3:
        return
    pygame.draw.line(surf, color, start, end, width)
    ang = math.atan2(ey - sy, ex - sx)
    for da in (math.pi * 0.82, -math.pi * 0.82):
        hx = ex + head * math.cos(ang + da)
        hy = ey + head * math.sin(ang + da)
        pygame.draw.line(surf, color, (ex, ey), (hx, hy), width)


# ─────────────────── VECTOR ICONS (no emoji -- fonts render those as
# broken tofu boxes on most Windows setups; small procedural glyphs drawn
# with pygame primitives always render correctly and look more deliberate) ──

def draw_icon(surf, kind, cx, cy, size, color):
    """Draw a small vector icon centered at (cx, cy). `size` is the icon's
    half-extent in pixels. Supported kinds: play, pause, reset, ball, force,
    section (small accent square used before section headers)."""
    if kind == "play":
        pts = [(cx - size * 0.5, cy - size), (cx - size * 0.5, cy + size), (cx + size, cy)]
        pygame.draw.polygon(surf, color, pts)
    elif kind == "pause":
        bw = max(2, size // 2)
        pygame.draw.rect(surf, color, (cx - size, cy - size, bw, size * 2), border_radius=1)
        pygame.draw.rect(surf, color, (cx + size - bw, cy - size, bw, size * 2), border_radius=1)
    elif kind == "reset":
        rect = pygame.Rect(0, 0, size * 2, size * 2)
        rect.center = (cx, cy)
        pygame.draw.arc(surf, color, rect, math.radians(35), math.radians(320), max(2, size // 3))
        ang = math.radians(35)
        tip = (cx + size * math.cos(ang), cy - size * math.sin(ang))
        for da in (0.55, -0.55):
            hx = tip[0] + size * 0.55 * math.cos(ang + math.pi / 2 + da)
            hy = tip[1] - size * 0.55 * math.sin(ang + math.pi / 2 + da)
            pygame.draw.line(surf, color, tip, (hx, hy), max(2, size // 3))
    elif kind == "ball":
        pygame.draw.circle(surf, color, (cx, cy), size)
        pygame.draw.circle(surf, tuple(min(255, v + 70) for v in color), (cx - size * 0.35, cy - size * 0.35), max(1, size * 0.35))
    elif kind == "force":
        draw_arrow(surf, (cx - size, cy + size * 0.6), (cx + size, cy - size * 0.6), color, width=max(2, size // 3), head=size * 0.6)
    elif kind == "section":
        pygame.draw.rect(surf, color, (cx - size * 0.35, cy - size, size * 0.7, size * 2), border_radius=2)


def draw_section_header(surf, text, x, y, color, font=None):
    """Small colored accent bar + label -- the professional-dashboard-style
    replacement for the old emoji-prefixed section titles."""
    font = font or font_lg
    draw_icon(surf, "section", x + 4, y + 9, 7, color)
    txt = font.render(text, True, color)
    surf.blit(txt, (x + 16, y))


def combined_restitution(e_obj, k_obj, e_surf, k_surf):
    """Coefficient of restitution for a contact between two deformable bodies.

    Object and surface act like two springs in series. For the same contact
    force the softer (more compliant, lower-stiffness) body deforms more, so it
    stores — and dominates the return of — more of the energy. Each body gives
    back e_i² of the energy it stored, and the stored energy splits in
    proportion to compliance (1/k). Hence:
      • a rigid floor (k huge)  -> e ≈ e_obj   (object rules the bounce)
      • a soft trampoline (k low) -> e ≈ e_surf (surface rules it, any object)
    """
    w_obj = k_surf / (k_obj + k_surf)   # object deforms more when the surface is stiff
    w_surf = k_obj / (k_obj + k_surf)
    energy_ratio = w_obj * e_obj * e_obj + w_surf * e_surf * e_surf
    return math.sqrt(max(0.0, energy_ratio))


# ─────────────────────────── OBJECT DEFINITIONS ─────────────
OBJECT_DEFS = [
    {
        "name": "Pluma",
        "mass": 0.003,        # kg
        "restitution": 0.05,  # e (material elasticity vs a rigid surface)
        "stiffness": 50.0,    # contact stiffness (relative): very soft
        "radius": 12,         # px
        "drag_coeff": 1.2,    # Cd
        "cross_area": 0.005,  # m²  (large for its mass)
        "color": (255, 255, 220),
        "icon_shape": "feather",
    },
    {
        "name": "Pelota Ping-Pong",
        "mass": 0.0027,
        "restitution": 0.90,
        "stiffness": 800.0,   # thin celluloid shell, fairly compliant but elastic
        "radius": 14,
        "drag_coeff": 0.47,
        "cross_area": 0.00126,
        "color": (255, 200, 50),
        "icon_shape": "circle",
    },
    {
        "name": "Pelota Tenis",
        "mass": 0.058,
        "restitution": 0.80,
        "stiffness": 1500.0,  # rubber/felt
        "radius": 16,
        "drag_coeff": 0.55,
        "cross_area": 0.0034,
        "color": (200, 255, 50),
        "icon_shape": "circle",
    },
    {
        "name": "Pelota Béisbol",
        "mass": 0.145,
        "restitution": 0.55,
        "stiffness": 4000.0,  # hard cork/leather
        "radius": 17,
        "drag_coeff": 0.35,
        "cross_area": 0.0042,
        "color": (240, 240, 240),
        "icon_shape": "circle",
    },
    {
        "name": "Roca",
        "mass": 2.0,
        "restitution": 0.20,
        "stiffness": 20000.0,  # stone, very stiff
        "radius": 20,
        "drag_coeff": 0.80,
        "cross_area": 0.008,
        "color": (140, 130, 120),
        "icon_shape": "rock",
    },
    {
        "name": "Bola Boliche",
        "mass": 6.35,
        "restitution": 0.18,
        "stiffness": 30000.0,  # hard resin
        "radius": 24,
        "drag_coeff": 0.47,
        "cross_area": 0.0366,
        "color": (40, 40, 60),
        "icon_shape": "circle",
    },
    {
        "name": "Bola de Hierro",
        "mass": 15.0,
        "restitution": 0.45,
        "stiffness": 100000.0,  # steel, extremely stiff
        "radius": 22,
        "drag_coeff": 0.47,
        "cross_area": 0.0201,
        "color": (100, 100, 110),
        "icon_shape": "circle",
    },
    {
        "name": "Hoja de Papel",
        "mass": 0.005,
        "restitution": 0.02,
        "stiffness": 30.0,    # floppy sheet, extremely soft
        "radius": 14,
        "drag_coeff": 2.0,
        "cross_area": 0.06,
        "color": (245, 245, 250),
        "icon_shape": "square",
    },
]

# ─────────────────────────── SURFACE DEFINITIONS ────────────
SURFACE_DEFS = [
    {
        "name": "Trampolín",
        "restitution": 0.92,
        "stiffness": 300.0,     # soft spring: surface rules the bounce (any object flies)
        "contact_time": 0.150,  # s, springy: long contact -> low peak force
        "friction": 0.95,
        "color": TRAMPOLINE,
        "color2": (200, 40, 80),
        "desc": "e=0.92",
    },
    {
        "name": "Slime Suave",
        "restitution": 0.35,
        "stiffness": 150.0,  # very soft and dissipative
        "contact_time": 0.120,
        "friction": 0.70,  # sticky
        "color": SLIME_GREEN,
        "color2": (30, 150, 60),
        "desc": "e=0.35",
    },
    {
        "name": "Slime Medio",
        "restitution": 0.55,
        "stiffness": 400.0,
        "contact_time": 0.090,
        "friction": 0.78,
        "color": SLIME_BLUE,
        "color2": (40, 80, 200),
        "desc": "e=0.55",
    },
    {
        "name": "Slime Duro",
        "restitution": 0.75,
        "stiffness": 1200.0,
        "contact_time": 0.060,
        "friction": 0.85,
        "color": SLIME_PURPLE,
        "color2": (120, 40, 180),
        "desc": "e=0.75",
    },
]

# ═══════════════════════════ CLASSES ═════════════════════════


class PhysicsParams:
    """Global tunable physics parameters."""
    def __init__(self):
        self.gravity = 9.81       # m/s²
        self.air_density = 1.225  # kg/m³
        self.air_enabled = True
        self.trail_enabled = True
        self.slow_motion = 1.0    # time multiplier

    def reset(self):
        self.__init__()


class NewtonState:
    """State + physics for the 'Fuerza Newton' mode: F=ma, friction, MRU/MRUA.

    Independent of pygame -- pure data and math, so it can be reasoned about
    (and tested) without the rendering loop.
    """

    HIST_WINDOW = 20.0  # seconds of history kept for the time-plot

    def __init__(self):
        # User-adjustable parameters (persist across reset)
        self.mass = 2.0          # kg
        self.mu_k = 0.20         # dimensionless
        self.friction_on = False
        self.dim_mode = "1D"     # "1D" | "2D"
        self.fa_mag = 10.0       # N
        self.fa_angle_deg = 0.0  # degrees, only meaningful in 2D
        self.fa_sign = 1         # +1 / -1, used for direction in 1D mode

        self.running = False
        self.show_ideal = True
        self._reset_kinematics()

    def _reset_kinematics(self):
        self.x = 0.0
        self.y = 0.0
        self.vx = 0.0
        self.vy = 0.0
        self.t = 0.0
        self.t_hist = [0.0]
        self.x_hist = [0.0]
        self.trace_world = [(0.0, 0.0)]  # world-space (x, y) points, meters
        # Snapshot baseline for ideal MRU/MRUA comparison curves
        self.x0 = 0.0
        self.v0x = 0.0
        self.a0x = 0.0
        self._recompute_derived()
        self.a0x = self.ax

    def reset(self):
        self.running = False
        self._reset_kinematics()

    def start(self):
        """(Re-)snapshot the MRU/MRUA baseline and begin/resume the run."""
        self.x0 = self.x
        self.v0x = self.vx
        self.t_hist = [self.t]
        self.x_hist = [self.x]
        self._recompute_derived()
        self.a0x = self.ax
        self.running = True

    def pause(self):
        self.running = False

    def set_dim_mode(self, mode):
        if mode == self.dim_mode:
            return
        self.dim_mode = mode
        if mode == "1D":
            self.y = 0.0
            self.vy = 0.0
        self.t_hist = [self.t]
        self.x_hist = [self.x]
        self.trace_world = [(self.x, self.y)]
        self.x0 = self.x
        self.v0x = self.vx
        self._recompute_derived()
        self.a0x = self.ax

    def applied_force_vector(self):
        if self.dim_mode == "1D":
            return (self.fa_mag * self.fa_sign, 0.0)
        rad = math.radians(self.fa_angle_deg)
        return (self.fa_mag * math.cos(rad), self.fa_mag * math.sin(rad))

    def _recompute_derived(self):
        """Recompute Fa/W/N/fk/net/a for the CURRENT state (used for the DCL
        and readouts even while paused, so sliders have live visual feedback)."""
        fax, fay = self.applied_force_vector()
        self.fa_vec = (fax, fay)
        self.w = self.mass * NEWTON_G
        self.n = self.w

        speed = math.hypot(self.vx, self.vy)
        if self.friction_on and speed > 1e-6:
            fk_mag = self.mu_k * self.n
            self.fk_vec = (-self.vx / speed * fk_mag, -self.vy / speed * fk_mag)
        else:
            self.fk_vec = (0.0, 0.0)

        net_x = fax + self.fk_vec[0]
        net_y = fay + self.fk_vec[1]
        if self.dim_mode == "1D":
            net_y = 0.0
        self.net_force = (net_x, net_y)
        self.ax = net_x / self.mass
        self.ay = net_y / self.mass

    def step(self, dt):
        if not self.running:
            return
        self._recompute_derived()

        prev_vx, prev_vy = self.vx, self.vy
        new_vx = self.vx + self.ax * dt
        new_vy = self.vy + self.ay * dt

        # Anti-overshoot clamp: pure kinetic friction (no applied force) must
        # not reverse the velocity's sign in a single Euler step -- that would
        # make the object oscillate instead of coming to rest.
        if self.friction_on and abs(self.fa_vec[0]) < 1e-6 and abs(self.fa_vec[1]) < 1e-6:
            if prev_vx * new_vx < 0:
                new_vx = 0.0
            if prev_vy * new_vy < 0:
                new_vy = 0.0

        self.x += self.vx * dt
        self.y += self.vy * dt if self.dim_mode == "2D" else 0.0
        self.vx = new_vx
        self.vy = new_vy if self.dim_mode == "2D" else 0.0
        self.t += dt

        self.t_hist.append(self.t)
        self.x_hist.append(self.x)
        while self.t_hist and self.t - self.t_hist[0] > self.HIST_WINDOW:
            self.t_hist.pop(0)
            self.x_hist.pop(0)

        self.trace_world.append((self.x, self.y))
        if len(self.trace_world) > 1000:
            self.trace_world.pop(0)

    def ideal_mru(self, t):
        return self.x0 + self.v0x * (t - self.t_hist[0]) if self.t_hist else self.x0

    def ideal_mrua(self, t):
        t0 = self.t_hist[0] if self.t_hist else 0.0
        dt = t - t0
        return self.x0 + self.v0x * dt + 0.5 * self.a0x * dt * dt


class Slider:
    """A horizontal slider widget."""
    def __init__(self, x, y, w, label, min_val, max_val, value, fmt="{:.2f}", color=ACCENT):
        self.rect = pygame.Rect(x, y, w, 30)
        self.label = label
        self.min_val = min_val
        self.max_val = max_val
        self.value = value
        self.fmt = fmt
        self.color = color
        self.dragging = False
        # Extra vertical gap below the label so text never touches the track
        self.track_y = y + 23
        self.track_rect = pygame.Rect(x, self.track_y - 4, w, 8)

    def handle_ratio(self):
        return (self.value - self.min_val) / (self.max_val - self.min_val)

    def handle_x(self):
        return self.rect.x + int(self.handle_ratio() * self.rect.w)

    def draw(self, surf):
        # Label
        txt = font_title.render(f"{self.label}: {self.fmt.format(self.value)}", True, GRAY)
        surf.blit(txt, (self.rect.x, self.rect.y))
        # Track bg
        pygame.draw.rect(surf, DARK, self.track_rect, border_radius=4)
        # Filled portion
        fill_w = int(self.handle_ratio() * self.rect.w)
        if fill_w > 0:
            fill_rect = pygame.Rect(self.rect.x, self.track_y - 4, fill_w, 8)
            pygame.draw.rect(surf, self.color, fill_rect, border_radius=4)
        # Handle
        hx = self.handle_x()
        pygame.draw.circle(surf, WHITE, (hx, self.track_y), 7)
        pygame.draw.circle(surf, self.color, (hx, self.track_y), 5)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            hx = self.handle_x()
            if abs(event.pos[0] - hx) < 14 and abs(event.pos[1] - self.track_y) < 14:
                self.dragging = True
                return True
            if self.track_rect.inflate(6, 12).collidepoint(event.pos):
                self.dragging = True
                self._update_from_mouse(event.pos[0])
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._update_from_mouse(event.pos[0])
            return True
        return False

    def _update_from_mouse(self, mx):
        ratio = (mx - self.rect.x) / self.rect.w
        ratio = max(0.0, min(1.0, ratio))
        self.value = self.min_val + ratio * (self.max_val - self.min_val)


class ToggleButton:
    """Simple toggle."""
    def __init__(self, x, y, w, label, state=True, color=ACCENT3):
        self.rect = pygame.Rect(x, y, w, 26)
        self.label = label
        self.state = state
        self.color = color
        self.hovered = False

    def draw(self, surf):
        base = self.color if self.state else (44, 44, 58)
        c = tuple(min(255, v + 22) for v in base) if self.hovered else base
        pygame.draw.rect(surf, c, self.rect, border_radius=6)
        border_c = tuple(min(255, v + 40) for v in c) if self.state else PANEL_BORDER
        pygame.draw.rect(surf, border_c, self.rect, 1, border_radius=6)
        # Small ON/OFF status dot for a clearer at-a-glance state
        dot_c = BG if self.state else DIM
        pygame.draw.circle(surf, dot_c, (self.rect.x + 12, self.rect.centery), 3)
        tag = "ON" if self.state else "OFF"
        txt = font_title.render(f"{self.label}: {tag}", True, BG if self.state else GRAY)
        tr = txt.get_rect(midleft=(self.rect.x + 20, self.rect.centery))
        surf.blit(txt, tr)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.state = not self.state
                return True
        return False


class Button:
    """Simple clickable button, optionally with a small vector icon."""
    def __init__(self, x, y, w, h, label, color=ACCENT2, icon=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.label = label
        self.color = color
        self.icon = icon
        self.hovered = False

    def draw(self, surf):
        c = tuple(min(255, v + 28) for v in self.color) if self.hovered else self.color
        pygame.draw.rect(surf, c, self.rect, border_radius=6)
        border_c = tuple(min(255, v + 45) for v in c)
        pygame.draw.rect(surf, border_c, self.rect, 1, border_radius=6)

        font = font_md
        txt = font.render(self.label, True, WHITE)
        # Fall back to the smaller font if the label would overflow the
        # button at the normal size -- keeps custom labels safe by construction.
        if txt.get_width() > self.rect.w - 16:
            font = font_title
            txt = font.render(self.label, True, WHITE)

        if self.icon:
            icon_size = max(5, self.rect.h // 6)
            gap = 6
            total_w = icon_size * 2 + gap + txt.get_width()
            if total_w > self.rect.w - 8:
                icon_size = max(4, icon_size - 2)
                total_w = icon_size * 2 + gap + txt.get_width()
            start_x = self.rect.centerx - total_w // 2
            draw_icon(surf, self.icon, start_x + icon_size, self.rect.centery, icon_size, WHITE)
            tr = txt.get_rect(midleft=(start_x + icon_size * 2 + gap, self.rect.centery))
        else:
            tr = txt.get_rect(center=self.rect.center)
        surf.blit(txt, tr)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class Surface:
    """A bouncing surface placed in the sim area."""
    def __init__(self, x, y, w, h, surf_def):
        self.rect = pygame.Rect(x, y, w, h)
        self.defn = surf_def
        self.restitution = surf_def["restitution"]
        self.stiffness = surf_def.get("stiffness", 1000.0)
        self.contact_time = surf_def.get("contact_time", 0.05)
        self.friction = surf_def.get("friction", 0.90)
        self.color = surf_def["color"]
        self.color2 = surf_def["color2"]
        self.name = surf_def["name"]
        self.dragging = False
        self.drag_offset = (0, 0)
        # Animation
        self.compress = 0.0  # 0..1 compression visual

    def draw(self, surf):
        comp_px = int(self.compress * 8)
        r = self.rect.copy()
        r.y += comp_px
        r.height -= comp_px
        # Body
        pygame.draw.rect(surf, self.color2, r, border_radius=6)
        inner = r.inflate(-4, -4)
        pygame.draw.rect(surf, self.color, inner, border_radius=4)
        # Squish lines
        for i in range(3):
            ly = r.y + 6 + i * (r.height // 4)
            pygame.draw.line(surf, self.color2, (r.x + 10, ly), (r.x + r.width - 10, ly), 2)
        # Label
        txt = font_title.render(f"{self.name} ({self.defn['desc']})", True, WHITE)
        tr = txt.get_rect(centerx=r.centerx, top=r.top - 14)
        surf.blit(txt, tr)
        # Decay compression
        self.compress *= 0.9

    def top_y(self):
        return self.rect.y


class PhysObject:
    """A physics object that falls and bounces."""
    def __init__(self, defn, x, y):
        self.defn = defn
        self.name = defn["name"]
        self.mass = defn["mass"]
        self.restitution = defn.get("restitution", 0.5)  # material elasticity
        self.stiffness = defn.get("stiffness", 5000.0)    # contact stiffness (relative)
        self.radius = defn["radius"]
        self.drag_coeff = defn["drag_coeff"]
        self.cross_area = defn["cross_area"]
        self.color = defn["color"]
        self.icon_shape = defn["icon_shape"]
        # Physics state (SI units: meters, m/s, etc.)
        self.x = px_to_m(x)
        self.y = px_to_m(y)
        self.vx = 0.0
        self.vy = 0.0
        self.ax = 0.0
        self.ay = 0.0
        # Tracking
        self.max_velocity = 0.0
        self.max_impact_force = 0.0
        self.bounce_count = 0
        self.kinetic_energy = 0.0
        self.potential_energy = 0.0
        self.drag_force = 0.0
        self.gravity_force = 0.0
        self.height_dropped = 0.0
        self.initial_y = y
        self.air_time = 0.0
        self.is_resting = False
        self.rest_timer = 0.0
        # Trail
        self.trail = []
        self.trail_timer = 0
        # Selection
        self.selected = False
        self.held = False
        self.held_vx = 0.0
        self.held_vy = 0.0
        self.prev_mx = 0
        self.prev_my = 0

    def px_pos(self):
        return (int(m_to_px(self.x)), int(m_to_px(self.y)))

    def speed(self):
        return math.hypot(self.vx, self.vy)

    def _register_impact(self, impact_speed, restitution, contact_time):
        # Framerate-independent impact force from impulse-momentum theorem.
        # The collision reverses normal velocity from -v to +e*v, so the change
        # in speed is v*(1+e). Average force = impulse / contact time. This is a
        # real, physical estimate that does NOT depend on the render FPS.
        dv = impact_speed * (1.0 + restitution)
        f_avg = self.mass * dv / max(contact_time, 1e-4)
        if f_avg > self.max_impact_force:
            self.max_impact_force = f_avg

    def update(self, params, surfaces, dt):
        if self.held or self.is_resting:
            return

        # Gravity
        g = params.gravity
        self.gravity_force = self.mass * g
        self.ay = g

        # Air resistance: F_drag = 0.5 * rho * v² * Cd * A
        self.drag_force = 0.0
        if params.air_enabled:
            speed = self.speed()
            if speed > 0.001:
                rho = params.air_density
                f_drag = 0.5 * rho * speed * speed * self.drag_coeff * self.cross_area
                self.drag_force = f_drag
                # Drag opposes velocity
                drag_ax = -(self.vx / speed) * (f_drag / self.mass)
                drag_ay = -(self.vy / speed) * (f_drag / self.mass)
                self.ax += drag_ax
                self.ay += drag_ay

        # Integration (semi-implicit Euler)
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Update tracking
        spd = self.speed()
        if spd > self.max_velocity:
            self.max_velocity = spd
        self.kinetic_energy = 0.5 * self.mass * spd * spd

        # Potential energy relative to lowest surface
        floor_y_m = px_to_m(HEIGHT - 40)
        h = max(0, floor_y_m - self.y)
        self.potential_energy = self.mass * g * h
        self.height_dropped = max(self.height_dropped, self.y - px_to_m(self.initial_y))
        self.air_time += dt

        # Reset acceleration for next frame
        self.ax = 0.0
        self.ay = 0.0

        # ── COLLISION WITH SURFACES ──
        px, py = self.px_pos()
        for s in surfaces:
            sr = s.rect
            if (px + self.radius > sr.x and px - self.radius < sr.x + sr.width):
                obj_bottom = py + self.radius
                surface_top = sr.y
                if obj_bottom >= surface_top and py - self.radius < sr.y + sr.height:
                    if self.vy > 0:  # falling down
                        # Combined coefficient of restitution for THIS pair of
                        # materials, weighted by contact stiffness: a rigid
                        # surface lets the object rule the bounce, a soft/springy
                        # surface rules it regardless of the object.
                        e = combined_restitution(self.restitution, self.stiffness,
                                                 s.restitution, s.stiffness)
                        # Impact!
                        impact_speed = abs(self.vy)
                        self._register_impact(impact_speed, e, s.contact_time)

                        # Bounce with restitution (normal) + tangential friction
                        self.vy = -self.vy * e
                        self.vx *= s.friction
                        # Position correction
                        self.y = px_to_m(surface_top - self.radius)
                        self.bounce_count += 1

                        # Surface compression visual
                        s.compress = min(1.0, impact_speed / 15.0)

                        # Check resting
                        if abs(self.vy) < 0.15:
                            self.vy = 0
                            self.vx *= 0.85
                            self.rest_timer += dt
                            if self.rest_timer > 0.3:
                                self.is_resting = True
                        else:
                            self.rest_timer = 0

        # ── FLOOR ──
        floor_px = HEIGHT - 20
        if m_to_px(self.y) + self.radius >= floor_px:
            if self.vy > 0:
                e = combined_restitution(self.restitution, self.stiffness,
                                         FLOOR_RESTITUTION, FLOOR_STIFFNESS)
                impact_speed = abs(self.vy)
                self._register_impact(impact_speed, e, FLOOR_CONTACT_TIME)
                self.vy = -self.vy * e
                self.vx *= FLOOR_FRICTION
                self.y = px_to_m(floor_px - self.radius)
                self.bounce_count += 1
                if abs(self.vy) < 0.15:
                    self.vy = 0
                    self.vx *= 0.8
                    self.rest_timer += dt
                    if self.rest_timer > 0.3:
                        self.is_resting = True

        # ── WALLS ──
        sim_left = 200
        sim_right = WIDTH - 280
        if m_to_px(self.x) - self.radius < sim_left:
            self.x = px_to_m(sim_left + self.radius)
            self.vx = abs(self.vx) * 0.5
        if m_to_px(self.x) + self.radius > sim_right:
            self.x = px_to_m(sim_right - self.radius)
            self.vx = -abs(self.vx) * 0.5

        # ── CEILING ──
        if m_to_px(self.y) - self.radius < 10:
            self.y = px_to_m(10 + self.radius)
            self.vy = abs(self.vy) * 0.3

        # Trail (time-based so it is independent of the fixed-step count)
        self.trail_timer += dt
        if self.trail_timer >= 0.016:
            self.trail_timer = 0.0
            self.trail.append((int(m_to_px(self.x)), int(m_to_px(self.y)), spd))
            if len(self.trail) > 120:
                self.trail.pop(0)

    def draw(self, surf, params, show_trail=True):
        px, py = self.px_pos()

        # Trail
        if show_trail and params.trail_enabled and len(self.trail) > 1:
            for i in range(1, len(self.trail)):
                alpha = i / len(self.trail)
                c = tuple(int(v * alpha * 0.4) for v in self.color)
                t = max(1, int(alpha * 3))
                pygame.draw.line(surf, c, (self.trail[i - 1][0], self.trail[i - 1][1]),
                                 (self.trail[i][0], self.trail[i][1]), t)

        # Glow when selected
        if self.selected:
            pygame.draw.circle(surf, (*ACCENT, 60), (px, py), self.radius + 8)

        # Shape
        r = self.radius
        if self.icon_shape == "feather":
            points = [
                (px, py - r),
                (px + r, py + r // 2),
                (px, py + r),
                (px - r // 2, py + r // 3),
            ]
            pygame.draw.polygon(surf, self.color, points)
            pygame.draw.line(surf, (200, 180, 100), (px, py - r), (px, py + r), 2)
        elif self.icon_shape == "rock":
            points = [
                (px - r, py + r // 2),
                (px - r + 5, py - r + 3),
                (px + 4, py - r),
                (px + r, py - r // 3),
                (px + r - 2, py + r - 3),
                (px - 3, py + r),
            ]
            pygame.draw.polygon(surf, self.color, points)
            pygame.draw.polygon(surf, tuple(max(0, v - 30) for v in self.color), points, 2)
            # Texture lines
            pygame.draw.line(surf, tuple(max(0, v - 20) for v in self.color),
                             (px - 5, py - 3), (px + 6, py + 2), 1)
        elif self.icon_shape == "square":
            rect = pygame.Rect(px - r, py - r + 4, r * 2, r * 2 - 6)
            pygame.draw.rect(surf, self.color, rect, border_radius=2)
            pygame.draw.rect(surf, (200, 200, 210), rect, 1, border_radius=2)
            # Lines on paper
            for i in range(3):
                ly = rect.y + 5 + i * 6
                pygame.draw.line(surf, (180, 180, 200), (rect.x + 4, ly), (rect.x + rect.w - 4, ly), 1)
        else:  # circle
            pygame.draw.circle(surf, self.color, (px, py), r)
            highlight = tuple(min(255, v + 60) for v in self.color)
            pygame.draw.circle(surf, highlight, (px - r // 3, py - r // 3), r // 3)
            pygame.draw.circle(surf, tuple(max(0, v - 40) for v in self.color), (px, py), r, 2)

        # Velocity arrow
        if not self.held and not self.is_resting and self.speed() > 0.3:
            arrow_scale = 4.0
            ax = px + int(self.vx * arrow_scale)
            ay = py + int(self.vy * arrow_scale)
            pygame.draw.line(surf, YELLOW, (px, py), (ax, ay), 2)


# ═══════════════════════════ GAME ═══════════════════════════


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.params = PhysicsParams()
        self.objects = []
        self.surfaces = []
        self.selected_obj = None
        self.dragging_new = None
        self.dragging_new_def = None
        self.dragging_surface = None
        self.dragging_surface_from_menu = None
        self.running = True
        self.accumulator = 0.0  # leftover sim-time for the fixed-step integrator

        # ── SETUP DEFAULT SURFACES ──
        cx = 200 + (WIDTH - 480) // 2
        self.surfaces.append(Surface(cx - 180, HEIGHT - 100, 160, 30, SURFACE_DEFS[0]))
        self.surfaces.append(Surface(cx + 20, HEIGHT - 100, 160, 30, SURFACE_DEFS[1]))

        # ── UI WIDGETS ──
        px = WIDTH - 268
        py_start = 426  # leaves clearance below the "PARÁMETROS" section header
        sp = 46

        self.sl_gravity = Slider(px, py_start, 240, "Gravedad (m/s²)", 0.0, 30.0, 9.81, "{:.2f}", ACCENT)
        self.sl_air_density = Slider(px, py_start + sp, 240, "Densidad aire (kg/m³)", 0.0, 5.0, 1.225, "{:.3f}", CYAN)
        self.sl_slow = Slider(px, py_start + sp * 2, 240, "Velocidad sim.", 0.1, 2.0, 1.0, "{:.1f}x", ORANGE)

        self.tg_air = ToggleButton(px, py_start + sp * 3 + 6, 115, "Aire", True, ACCENT3)
        self.tg_trail = ToggleButton(px + 125, py_start + sp * 3 + 6, 115, "Estela", True, PURPLE)

        self.btn_clear = Button(px, py_start + sp * 3 + 40, 115, 26, "Limpiar", RED)
        self.btn_reset = Button(px + 125, py_start + sp * 3 + 40, 115, 26, "Reset", DIM)

        self.sliders = [self.sl_gravity, self.sl_air_density, self.sl_slow]
        self.toggles = [self.tg_air, self.tg_trail]
        self.buttons = [self.btn_clear, self.btn_reset]

        # Height ruler data
        self.ruler_visible = True

        # ── MODE TABS ──
        self.app_mode = "bounce"  # "bounce" | "newton"
        self.btn_tab_bounce = Button(204, 4, 140, 26, "REBOTE", ACCENT, icon="ball")
        self.btn_tab_newton = Button(352, 4, 190, 26, "FUERZA NEWTON", DIM, icon="force")

        self._init_newton_ui()

    def _init_newton_ui(self):
        self.newton = NewtonState()

        npx = WIDTH - 268   # right-panel readouts start here (Newton mode)
        lpx = 10            # left sidebar controls
        py0 = 70
        sp = 46

        self.n_sl_mass = Slider(lpx, py0, 176, "Masa (kg)", 0.5, 20.0, 2.0, "{:.1f}", ACCENT)
        self.n_sl_fa = Slider(lpx, py0 + sp, 176, "Fuerza aplicada Fa (N)", 0.0, 100.0, 10.0, "{:.1f}", ACCENT2)
        self.n_sl_angle = Slider(lpx, py0 + sp * 2, 176, "Ángulo Fa (°) [2D]", -180.0, 180.0, 0.0, "{:.0f}", CYAN)
        self.n_sl_mu = Slider(lpx, py0 + sp * 3, 176, "μk (fricción)", 0.0, 1.0, 0.20, "{:.2f}", ORANGE)

        self.n_tg_friction = ToggleButton(lpx, py0 + sp * 4, 176, "Fricción", False, YELLOW)

        self.n_btn_dim1d = Button(lpx, py0 + sp * 5 + 4, 84, 26, "1D", ACCENT)
        self.n_btn_dim2d = Button(lpx + 92, py0 + sp * 5 + 4, 84, 26, "2D", DIM)

        self.n_btn_dir_left = Button(lpx, py0 + sp * 6 + 4, 84, 26, "◄ -x", DIM)
        self.n_btn_dir_right = Button(lpx + 92, py0 + sp * 6 + 4, 84, 26, "+x ►", ACCENT)

        self.n_btn_start = Button(lpx, py0 + sp * 7 + 8, 84, 32, "INICIAR", ACCENT3, icon="play")
        self.n_btn_reset = Button(lpx + 92, py0 + sp * 7 + 8, 84, 32, "RESET", RED, icon="reset")

        self.n_tg_ideal = ToggleButton(lpx, py0 + sp * 8 + 12, 176, "Curvas ideales", True, PURPLE)

        self.n_sliders = [self.n_sl_mass, self.n_sl_fa, self.n_sl_angle, self.n_sl_mu]
        self.n_toggles = [self.n_tg_friction, self.n_tg_ideal]
        self.n_buttons = [
            self.n_btn_dim1d, self.n_btn_dim2d,
            self.n_btn_dir_left, self.n_btn_dir_right,
            self.n_btn_start, self.n_btn_reset,
        ]

        # Sim-area layout (center panel, between the two sidebars)
        self.n_sim_rect = pygame.Rect(200, 40, WIDTH - 476, 430)
        self.n_plot_rect = pygame.Rect(200, 490, WIDTH - 476, 260)
        self.n_readout_x = npx

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)  # cap
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()
        sys.exit()

    # ─────────── EVENTS ───────────

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
                return
            # Mode tabs are always clickable regardless of active mode
            if self.btn_tab_bounce.handle_event(event):
                self.app_mode = "bounce"
            if self.btn_tab_newton.handle_event(event):
                self.app_mode = "newton"

        if self.app_mode == "bounce":
            self._handle_events_bounce(events)
        else:
            self._handle_events_newton(events)

    def _handle_events_bounce(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    if self.selected_obj and self.selected_obj in self.objects:
                        self.objects.remove(self.selected_obj)
                        self.selected_obj = None
                if event.key == pygame.K_c:
                    self.objects.clear()
                    self.selected_obj = None

            # Sliders / toggles / buttons
            for s in self.sliders:
                if s.handle_event(event):
                    continue
            for t in self.toggles:
                t.handle_event(event)
            if self.btn_clear.handle_event(event):
                self.objects.clear()
                self.selected_obj = None
            if self.btn_reset.handle_event(event):
                self.params.reset()
                self.sl_gravity.value = self.params.gravity
                self.sl_air_density.value = self.params.air_density
                self.sl_slow.value = self.params.slow_motion
                self.tg_air.state = True
                self.tg_trail.state = True

            # Mouse events for drag & drop
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                # Check if clicking on existing object
                handled = False

                # Check surface menu (bottom left panel area)
                for i, sdef in enumerate(SURFACE_DEFS):
                    bx = 10
                    by = 560 + i * 44
                    brect = pygame.Rect(bx, by, 180, 38)
                    if brect.collidepoint(mx, my):
                        # Start dragging a new surface
                        new_s = Surface(mx - 80, my - 15, 160, 30, sdef)
                        self.dragging_surface_from_menu = new_s
                        handled = True
                        break

                if not handled:
                    # Check surfaces for dragging
                    for s in self.surfaces:
                        if s.rect.collidepoint(mx, my):
                            s.dragging = True
                            s.drag_offset = (mx - s.rect.x, my - s.rect.y)
                            self.dragging_surface = s
                            handled = True
                            break

                if not handled:
                    # Check object menu
                    for i, odef in enumerate(OBJECT_DEFS):
                        bx = 10
                        by = 70 + i * 56
                        brect = pygame.Rect(bx, by, 180, 50)
                        if brect.collidepoint(mx, my):
                            self.dragging_new_def = odef
                            self.dragging_new = (mx, my)
                            handled = True
                            break

                if not handled:
                    # Check existing objects
                    for obj in reversed(self.objects):
                        px_o, py_o = obj.px_pos()
                        if math.hypot(mx - px_o, my - py_o) < obj.radius + 5:
                            obj.held = True
                            obj.is_resting = False
                            obj.rest_timer = 0
                            obj.vx = 0
                            obj.vy = 0
                            obj.prev_mx = mx
                            obj.prev_my = my
                            if self.selected_obj:
                                self.selected_obj.selected = False
                            self.selected_obj = obj
                            obj.selected = True
                            handled = True
                            break

                if not handled:
                    if self.selected_obj:
                        self.selected_obj.selected = False
                        self.selected_obj = None

            elif event.type == pygame.MOUSEMOTION:
                mx, my = event.pos
                if self.dragging_new:
                    self.dragging_new = (mx, my)
                if self.dragging_surface_from_menu:
                    self.dragging_surface_from_menu.rect.x = mx - 80
                    self.dragging_surface_from_menu.rect.y = my - 15
                if self.dragging_surface:
                    s = self.dragging_surface
                    s.rect.x = mx - s.drag_offset[0]
                    s.rect.y = my - s.drag_offset[1]
                # Update held objects
                for obj in self.objects:
                    if obj.held:
                        obj.held_vx = (mx - obj.prev_mx) / max(0.016, DT) * 0.02
                        obj.held_vy = (my - obj.prev_my) / max(0.016, DT) * 0.02
                        obj.x = px_to_m(mx)
                        obj.y = px_to_m(my)
                        obj.prev_mx = mx
                        obj.prev_my = my

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mx, my = event.pos
                # Release new object from menu
                if self.dragging_new and self.dragging_new_def:
                    if mx > 200:  # dropped in sim area
                        obj = PhysObject(self.dragging_new_def, mx, my)
                        obj.initial_y = my
                        self.objects.append(obj)
                        if self.selected_obj:
                            self.selected_obj.selected = False
                        self.selected_obj = obj
                        obj.selected = True
                    self.dragging_new = None
                    self.dragging_new_def = None

                # Release surface from menu
                if self.dragging_surface_from_menu:
                    s = self.dragging_surface_from_menu
                    if s.rect.x > 190:
                        self.surfaces.append(s)
                    self.dragging_surface_from_menu = None

                if self.dragging_surface:
                    s = self.dragging_surface
                    s.dragging = False
                    # Remove if dragged back to menu
                    if s.rect.x < 190:
                        if s in self.surfaces:
                            self.surfaces.remove(s)
                    self.dragging_surface = None

                # Release held objects
                for obj in self.objects:
                    if obj.held:
                        obj.vx = obj.held_vx
                        obj.vy = obj.held_vy
                        obj.held = False
                        obj.trail.clear()
                        obj.max_velocity = 0
                        obj.max_impact_force = 0
                        obj.bounce_count = 0
                        obj.height_dropped = 0
                        obj.air_time = 0
                        obj.initial_y = m_to_px(obj.y)
                        obj.is_resting = False
                        obj.rest_timer = 0

            # Right-click to delete surfaces
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                mx, my = event.pos
                for s in self.surfaces[:]:
                    if s.rect.collidepoint(mx, my):
                        self.surfaces.remove(s)
                        break

    # ─────────── UPDATE ───────────

    def update(self, dt):
        if self.app_mode == "bounce":
            self.update_bounce(dt)
        else:
            self.update_newton(dt)

    def update_bounce(self, dt):
        self.params.gravity = self.sl_gravity.value
        self.params.air_density = self.sl_air_density.value
        self.params.slow_motion = self.sl_slow.value
        self.params.air_enabled = self.tg_air.state
        self.params.trail_enabled = self.tg_trail.state

        # Fixed-timestep integration with an accumulator. Slow-motion just feeds
        # less simulated time per frame, so physics stays identical at any FPS.
        self.accumulator += dt * self.params.slow_motion
        self.accumulator = min(self.accumulator, 0.25)  # avoid spiral of death
        while self.accumulator >= FIXED_DT:
            for obj in self.objects:
                obj.update(self.params, self.surfaces, FIXED_DT)
            self.accumulator -= FIXED_DT

    # ─────────── DRAW ─────────────

    def draw(self):
        if self.app_mode == "bounce":
            self.draw_bounce()
        else:
            self.draw_newton()
        self._draw_tabs()
        pygame.display.flip()

    def _draw_tabs(self):
        # Small header pinned in the top-left corner of the central sim area
        # (x=198..WIDTH-276) so it never overlaps the left/right panels or the
        # existing top-center object counter text.
        self.btn_tab_bounce.color = ACCENT if self.app_mode == "bounce" else DIM
        self.btn_tab_newton.color = ACCENT2 if self.app_mode == "newton" else DIM
        self.btn_tab_bounce.draw(screen)
        self.btn_tab_newton.draw(screen)

    def draw_bounce(self):
        screen.fill(BG)

        # ── LEFT PANEL ──
        left_panel = pygame.Rect(0, 0, 196, HEIGHT)
        pygame.draw.rect(screen, PANEL_BG, left_panel)
        pygame.draw.line(screen, PANEL_BORDER, (196, 0), (196, HEIGHT), 2)

        # Title
        draw_section_header(screen, "OBJETOS", 14, 14, ACCENT)
        txt2 = font_title.render("Arrastra al área →", True, DIM)
        screen.blit(txt2, (14, 38))

        # Object menu items
        for i, odef in enumerate(OBJECT_DEFS):
            bx, by = 10, 70 + i * 56
            brect = pygame.Rect(bx, by, 180, 50)
            hovered = brect.collidepoint(pygame.mouse.get_pos())
            bc = (40, 40, 55) if hovered else (32, 32, 44)
            pygame.draw.rect(screen, bc, brect, border_radius=6)
            pygame.draw.rect(screen, PANEL_BORDER, brect, 1, border_radius=6)

            # Mini icon
            cx, cy = bx + 20, by + 25
            r = 10
            pygame.draw.circle(screen, odef["color"], (cx, cy), r)

            # Text
            name_txt = font_md.render(odef["name"], True, WHITE)
            screen.blit(name_txt, (bx + 38, by + 6))
            info = f"{odef['mass']}kg  Cd={odef['drag_coeff']}"
            info_txt = font_title.render(info, True, GRAY)
            screen.blit(info_txt, (bx + 38, by + 24))
            area_txt = font_title.render(f"A={odef['cross_area']}m²  e={odef['restitution']}", True, DIM)
            screen.blit(area_txt, (bx + 38, by + 36))

        # ── SURFACE MENU ──
        draw_section_header(screen, "SUPERFICIES", 14, 528, ACCENT2)
        txt_s2 = font_title.render("Arrastra / Clic der. borrar", True, DIM)
        screen.blit(txt_s2, (14, 548))

        for i, sdef in enumerate(SURFACE_DEFS):
            bx, by = 10, 568 + i * 44
            brect = pygame.Rect(bx, by, 180, 38)
            hovered = brect.collidepoint(pygame.mouse.get_pos())
            bc = sdef["color2"] if hovered else (32, 32, 44)
            pygame.draw.rect(screen, bc, brect, border_radius=6)
            pygame.draw.rect(screen, sdef["color"], brect, 2, border_radius=6)
            t = font_md.render(sdef["name"], True, sdef["color"])
            screen.blit(t, (bx + 10, by + 4))
            t2 = font_title.render(f"e={sdef['restitution']}  k={sdef['stiffness']:.0f} (blando)", True, GRAY)
            screen.blit(t2, (bx + 10, by + 22))

        # ── RIGHT PANEL ──
        rpx = WIDTH - 276
        right_panel = pygame.Rect(rpx, 0, 276, HEIGHT)
        pygame.draw.rect(screen, PANEL_BG, right_panel)
        pygame.draw.line(screen, PANEL_BORDER, (rpx, 0), (rpx, HEIGHT), 2)

        # Physics data
        dx = rpx + 10
        dy = 14
        draw_section_header(screen, "DATOS EN VIVO", dx, dy, ACCENT3)
        dy += 28

        obj = self.selected_obj
        if obj and obj in self.objects:
            # Object info header
            pygame.draw.rect(screen, DARK, (dx, dy, 256, 24), border_radius=4)
            screen.blit(font_md.render(f"{obj.name} ({obj.mass}kg)", True, YELLOW), (dx + 8, dy + 4))
            dy += 32

            data_lines = [
                ("Posición X", f"{obj.x:.3f} m", WHITE),
                ("Posición Y", f"{obj.y:.3f} m", WHITE),
                ("Vel. X", f"{obj.vx:.3f} m/s", CYAN),
                ("Vel. Y", f"{obj.vy:.3f} m/s", CYAN),
                ("Rapidez", f"{obj.speed():.3f} m/s", ACCENT),
                ("Rapidez máx.", f"{obj.max_velocity:.3f} m/s", ORANGE),
                ("─" * 28, "", DIM),
                ("Energía cinética", f"{obj.kinetic_energy:.4f} J", GREEN),
                ("Energía potencial", f"{obj.potential_energy:.4f} J", GREEN),
                ("E. total (aprox)", f"{obj.kinetic_energy + obj.potential_energy:.4f} J", ACCENT3),
                ("─" * 28, "", DIM),
                ("F. gravedad", f"{obj.gravity_force:.4f} N", YELLOW),
                ("F. arrastre", f"{obj.drag_force:.6f} N", PINK),
                ("F. impacto máx.", f"{obj.max_impact_force:.2f} N", RED),
                ("─" * 28, "", DIM),
                ("Rebotes", f"{obj.bounce_count}", PURPLE),
                ("Altura caída", f"{obj.height_dropped:.3f} m", ORANGE),
                ("Tiempo en aire", f"{obj.air_time:.2f} s", CYAN),
                ("Estado", "Reposo" if obj.is_resting else "En movimiento", GREEN if not obj.is_resting else DIM),
            ]
            for label, value, color in data_lines:
                if value == "":
                    pygame.draw.line(screen, DIM, (dx, dy + 6), (dx + 256, dy + 6), 1)
                    dy += 13
                else:
                    lt = font_title.render(label, True, GRAY)
                    vt = font_title.render(value, True, color)
                    screen.blit(lt, (dx + 2, dy))
                    screen.blit(vt, (dx + 256 - vt.get_width(), dy))
                    dy += 16

            # Terminal velocity estimate
            dy += 4
            if obj.drag_coeff > 0 and obj.cross_area > 0 and self.params.air_enabled:
                v_term = math.sqrt(
                    (2 * obj.mass * self.params.gravity) /
                    (self.params.air_density * obj.drag_coeff * obj.cross_area)
                )
                pygame.draw.rect(screen, (30, 50, 40), (dx, dy, 256, 18), border_radius=3)
                tt = font_title.render(f"Vel. terminal teórica: {v_term:.2f} m/s", True, ACCENT3)
                screen.blit(tt, (dx + 4, dy + 3))
                dy += 24
        else:
            screen.blit(font_sm.render("Selecciona un objeto", True, DIM), (dx, dy + 4))
            screen.blit(font_sm.render("para ver sus datos.", True, DIM), (dx, dy + 22))
            dy += 60

        # ── SLIDERS / CONTROLS ──
        dy = 392
        pygame.draw.line(screen, PANEL_BORDER, (rpx + 10, dy - 8), (rpx + 266, dy - 8), 1)
        draw_section_header(screen, "PARÁMETROS", rpx + 10, dy - 4, ORANGE)

        for s in self.sliders:
            s.draw(screen)
        for t in self.toggles:
            t.draw(screen)
        for b in self.buttons:
            b.draw(screen)

        # Key hints
        hy = HEIGHT - 66
        pygame.draw.rect(screen, DARK, (rpx + 8, hy, 260, 58), border_radius=5)
        hints = [
            "DEL: borrar objeto seleccionado",
            "C: limpiar todos los objetos",
            "ESC: salir",
        ]
        for i, h in enumerate(hints):
            screen.blit(font_title.render(h, True, DIM), (rpx + 14, hy + 5 + i * 17))

        # ── SIMULATION AREA ──
        sim_rect = pygame.Rect(198, 0, WIDTH - 474, HEIGHT)
        # Grid
        for gx in range(200, WIDTH - 276, 40):
            pygame.draw.line(screen, (24, 24, 32), (gx, 0), (gx, HEIGHT), 1)
        for gy in range(0, HEIGHT, 40):
            pygame.draw.line(screen, (24, 24, 32), (200, gy), (WIDTH - 276, gy), 1)

        # Floor
        floor_y = HEIGHT - 20
        pygame.draw.rect(screen, (40, 40, 50), (200, floor_y, WIDTH - 476, 20))
        pygame.draw.line(screen, DIM, (200, floor_y), (WIDTH - 276, floor_y), 2)
        # Floor label
        ft = font_title.render("Suelo rígido (e=0.90)", True, DIM)
        screen.blit(ft, (202, floor_y + 3))

        # ── HEIGHT RULER ──
        if self.ruler_visible:
            rx = 204
            pygame.draw.line(screen, DIM, (rx, 10), (rx, floor_y), 1)
            for py_r in range(10, floor_y, 40):
                h_m = px_to_m(floor_y - py_r)
                pygame.draw.line(screen, DIM, (rx, py_r), (rx + 8, py_r), 1)
                if int(h_m * 10) % 5 == 0 or py_r % 80 == 10:
                    ht = font_title.render(f"{h_m:.1f}m", True, DIM)
                    screen.blit(ht, (rx + 10, py_r - 6))

        # ── DRAW SURFACES ──
        for s in self.surfaces:
            s.draw(screen)

        # ── DRAW OBJECTS ──
        for o in self.objects:
            o.draw(screen, self.params)

        # ── DRAGGING PREVIEW ──
        if self.dragging_new and self.dragging_new_def:
            mx, my = self.dragging_new
            d = self.dragging_new_def
            # Ghost object
            r = d["radius"]
            ghost_surf = pygame.Surface((r * 2 + 4, r * 2 + 4), pygame.SRCALPHA)
            pygame.draw.circle(ghost_surf, (*d["color"], 150), (r + 2, r + 2), r)
            screen.blit(ghost_surf, (mx - r - 2, my - r - 2))
            # Height info
            if mx > 200:
                h_m = px_to_m(HEIGHT - 20 - my)
                ht = font_md.render(f"Altura: {h_m:.2f} m", True, YELLOW)
                screen.blit(ht, (mx + 16, my - 8))
                # Theoretical impact speed (no air)
                if h_m > 0:
                    v_impact = math.sqrt(2 * self.params.gravity * h_m)
                    vt = font_title.render(f"v impacto (sin aire): {v_impact:.2f} m/s", True, CYAN)
                    screen.blit(vt, (mx + 16, my + 10))

        # Dragging surface preview
        if self.dragging_surface_from_menu:
            s = self.dragging_surface_from_menu
            s.draw(screen)

        # ── HELD OBJECT HEIGHT ──
        for o in self.objects:
            if o.held:
                px_o, py_o = o.px_pos()
                h_m = px_to_m(HEIGHT - 20 - py_o)
                ht = font_md.render(f"h = {h_m:.2f} m", True, YELLOW)
                screen.blit(ht, (px_o + o.radius + 8, py_o - 8))

        # ── OBJECT COUNT ──
        count_txt = font_title.render(f"Objetos: {len(self.objects)} | Superficies: {len(self.surfaces)}", True, DIM)
        screen.blit(count_txt, (WIDTH // 2 - count_txt.get_width() // 2, 4))

        # ── TITLE BAR ──
        title_txt = font_xl.render("PHYSICS PLAYGROUND", True, ACCENT)
        screen.blit(title_txt, (WIDTH // 2 - title_txt.get_width() // 2, HEIGHT - 17))

    # ═══════════════ NEWTON MODE (fuerza, masa, aceleración) ═══════════════

    def _handle_events_newton(self, events):
        for event in events:
            for s in self.n_sliders:
                if s.handle_event(event):
                    break
            for t in self.n_toggles:
                t.handle_event(event)

            if self.n_btn_dim1d.handle_event(event):
                self.newton.set_dim_mode("1D")
            if self.n_btn_dim2d.handle_event(event):
                self.newton.set_dim_mode("2D")
            if self.n_btn_dir_left.handle_event(event):
                self.newton.fa_sign = -1
            if self.n_btn_dir_right.handle_event(event):
                self.newton.fa_sign = 1
            if self.n_btn_start.handle_event(event):
                if self.newton.running:
                    self.newton.pause()
                else:
                    self.newton.start()
            if self.n_btn_reset.handle_event(event):
                self.newton.reset()

    def update_newton(self, dt):
        ns = self.newton
        ns.mass = self.n_sl_mass.value
        ns.fa_mag = self.n_sl_fa.value
        ns.fa_angle_deg = self.n_sl_angle.value
        ns.mu_k = self.n_sl_mu.value
        ns.friction_on = self.n_tg_friction.state
        ns.show_ideal = self.n_tg_ideal.state
        ns.step(dt)

        self.n_btn_dim1d.color = ACCENT if ns.dim_mode == "1D" else DIM
        self.n_btn_dim2d.color = ACCENT if ns.dim_mode == "2D" else DIM
        self.n_btn_dir_left.color = ACCENT if ns.fa_sign < 0 else DIM
        self.n_btn_dir_right.color = ACCENT if ns.fa_sign > 0 else DIM
        self.n_btn_start.label = "PAUSAR" if ns.running else "INICIAR"
        self.n_btn_start.icon = "pause" if ns.running else "play"
        self.n_btn_start.color = ORANGE if ns.running else ACCENT3

    def _n_world_to_screen(self, wx, wy):
        cx, cy = self.n_sim_rect.center
        sx = cx + (wx - self.newton.x) * NEWTON_PPM
        sy = cy - (wy - self.newton.y) * NEWTON_PPM
        return int(sx), int(sy)

    def draw_newton(self):
        screen.fill(BG)
        ns = self.newton

        # ── LEFT PANEL (controls) ──
        left_panel = pygame.Rect(0, 0, 196, HEIGHT)
        pygame.draw.rect(screen, PANEL_BG, left_panel)
        pygame.draw.line(screen, PANEL_BORDER, (196, 0), (196, HEIGHT), 2)
        draw_section_header(screen, "CONTROLES", 14, 34, ACCENT2)

        for s in self.n_sliders:
            s.draw(screen)
        for t in self.n_toggles:
            t.draw(screen)
        for b in self.n_buttons:
            b.draw(screen)

        screen.blit(font_title.render("Modo dimensional:", True, GRAY), (10, self.n_btn_dim1d.rect.y - 14))
        screen.blit(font_title.render("Dirección Fa (modo 1D):", True, GRAY), (10, self.n_btn_dir_left.rect.y - 14))

        # ── RIGHT PANEL (readouts) ──
        rpx = WIDTH - 276
        right_panel = pygame.Rect(rpx, 0, 276, HEIGHT)
        pygame.draw.rect(screen, PANEL_BG, right_panel)
        pygame.draw.line(screen, PANEL_BORDER, (rpx, 0), (rpx, HEIGHT), 2)

        dx = rpx + 10
        dy = 34
        draw_section_header(screen, "DATOS EN VIVO", dx, dy, ACCENT3)
        dy += 30

        fa_mag = math.hypot(*ns.fa_vec)
        fk_mag = math.hypot(*ns.fk_vec)
        net_mag = math.hypot(*ns.net_force)
        a_mag = math.hypot(ns.ax, ns.ay)
        v_mag = math.hypot(ns.vx, ns.vy)

        data_lines = [
            ("Modo", ns.dim_mode, WHITE),
            ("Estado", "Corriendo" if ns.running else "Pausado", GREEN if ns.running else DIM),
            ("─" * 28, "", DIM),
            ("Fuerza aplicada Fa", f"{fa_mag:.2f} N", ACCENT2),
            ("Peso W", f"{ns.w:.2f} N", GREEN),
            ("Normal N", f"{ns.n:.2f} N", PURPLE),
            ("Fricción fk", f"{fk_mag:.2f} N", RED if ns.friction_on else DIM),
            ("Fuerza neta ∑F", f"{net_mag:.2f} N", YELLOW),
            ("─" * 28, "", DIM),
            ("Aceleración a", f"{a_mag:.3f} m/s²", CYAN),
            ("Velocidad v", f"{v_mag:.3f} m/s", ACCENT),
            ("Posición x", f"{ns.x:.3f} m", WHITE),
        ]
        if ns.dim_mode == "2D":
            data_lines.append(("Posición y", f"{ns.y:.3f} m", WHITE))
        data_lines.append(("Tiempo t", f"{ns.t:.2f} s", GRAY))

        for label, value, color in data_lines:
            if value == "":
                pygame.draw.line(screen, DIM, (dx, dy + 6), (dx + 256, dy + 6), 1)
                dy += 13
            else:
                lt = font_title.render(label, True, GRAY)
                vt = font_title.render(value, True, color)
                screen.blit(lt, (dx + 2, dy))
                screen.blit(vt, (dx + 256 - vt.get_width(), dy))
                dy += 16

        if ns.friction_on and fa_mag > 1e-6:
            # Kinetic friction (fk = μk·N) is constant, not speed-dependent,
            # so there is no asymptotic terminal velocity here -- the object
            # either accelerates at a constant rate, decelerates to rest, or
            # (if Fa exactly equals fk) moves at constant velocity (MRU).
            fk_const = ns.mu_k * ns.n
            dy += 6
            pygame.draw.rect(screen, (30, 40, 50), (dx, dy, 256, 18), border_radius=3)
            if fa_mag > fk_const + 1e-6:
                note = f"Fa>fk: acelera cte. a={(fa_mag - fk_const) / ns.mass:.2f} m/s²"
            elif fa_mag < fk_const - 1e-6:
                note = "Fa<fk: desacelera hasta detenerse"
            else:
                note = "Fa=fk: equilibrio → MRU"
            tt = font_title.render(note, True, ACCENT3)
            screen.blit(tt, (dx + 4, dy + 3))

        # ── SIM AREA ──
        sim = self.n_sim_rect
        pygame.draw.rect(screen, (16, 16, 22), sim)
        pygame.draw.rect(screen, PANEL_BORDER, sim, 1)
        for gx in range(sim.x, sim.right, 40):
            pygame.draw.line(screen, (24, 24, 32), (gx, sim.y), (gx, sim.bottom), 1)
        for gy in range(sim.y, sim.bottom, 40):
            pygame.draw.line(screen, (24, 24, 32), (sim.x, gy), (sim.right, gy), 1)

        cx, cy = sim.center
        if ns.dim_mode == "1D":
            pygame.draw.line(screen, DIM, (sim.x, cy), (sim.right, cy), 2)

        if len(ns.trace_world) >= 2:
            pts = [self._n_world_to_screen(wx, wy) for wx, wy in ns.trace_world]
            pygame.draw.lines(screen, (60, 140, 255), False, pts, 2)

        obj_rect = pygame.Rect(0, 0, 26, 26)
        obj_rect.center = (cx, cy)
        pygame.draw.rect(screen, YELLOW, obj_rect, border_radius=4)
        pygame.draw.rect(screen, WHITE, obj_rect, 2, border_radius=4)

        # ── FREE-BODY DIAGRAM (DCL) ──
        MAX_ARROW_PX = 130

        def arrow_end(vec):
            vxv, vyv = vec
            mag = math.hypot(vxv, vyv)
            if mag < 1e-6:
                return None
            length = min(mag * NEWTON_ARROW_SCALE, MAX_ARROW_PX)
            ux, uy = vxv / mag, vyv / mag
            return (cx + ux * length, cy - uy * length)

        end = arrow_end(ns.fa_vec)
        if end:
            draw_arrow(screen, (cx, cy), end, ACCENT2, 3)
        end = arrow_end((0.0, -ns.w))
        if end:
            draw_arrow(screen, (cx, cy), end, GREEN, 2)
        end = arrow_end((0.0, ns.n))
        if end:
            draw_arrow(screen, (cx, cy), end, PURPLE, 2)
        if ns.friction_on:
            end = arrow_end(ns.fk_vec)
            if end:
                draw_arrow(screen, (cx, cy), end, RED, 3)

        legend = [("Fa aplicada", ACCENT2), ("Peso W", GREEN), ("Normal N", PURPLE), ("Fricción fk", RED)]
        lx, ly = sim.x + 8, sim.y + 8
        for i, (lbl, col) in enumerate(legend):
            pygame.draw.line(screen, col, (lx, ly + i * 16 + 6), (lx + 18, ly + i * 16 + 6), 3)
            screen.blit(font_title.render(lbl, True, col), (lx + 24, ly + i * 16))

        self._draw_newton_time_plot()

    def _draw_newton_time_plot(self):
        ns = self.newton
        rect = self.n_plot_rect
        pygame.draw.rect(screen, PANEL_BG, rect)
        pygame.draw.rect(screen, PANEL_BORDER, rect, 1)
        title = font_md.render("Posición x vs. tiempo — Simulado vs. MRU/MRUA ideal", True, WHITE)
        screen.blit(title, (rect.x + 8, rect.y + 6))

        th, xh = ns.t_hist, ns.x_hist
        if len(th) < 2 or (th[-1] - th[0]) < 1e-6:
            return

        mru_vals = [ns.ideal_mru(t) for t in th] if ns.show_ideal else []
        mrua_vals = [ns.ideal_mrua(t) for t in th] if ns.show_ideal else []
        all_vals = xh + mru_vals + mrua_vals
        y_min, y_max = min(all_vals), max(all_vals)
        if y_max - y_min < 1e-6:
            y_min, y_max = y_min - 1.0, y_max + 1.0
        pad = (y_max - y_min) * 0.1
        y_min -= pad
        y_max += pad
        t_min, t_max = th[0], th[-1]

        plot_area = rect.inflate(-24, -56)
        plot_area.top = rect.top + 32

        def to_px(t, x):
            px_ = plot_area.x + (t - t_min) / (t_max - t_min) * plot_area.w
            py_ = plot_area.bottom - (x - y_min) / (y_max - y_min) * plot_area.h
            return (px_, py_)

        pygame.draw.line(screen, GRAY, (plot_area.x, plot_area.bottom), (plot_area.right, plot_area.bottom), 1)
        pygame.draw.line(screen, GRAY, (plot_area.x, plot_area.top), (plot_area.x, plot_area.bottom), 1)
        screen.blit(font_title.render("t (s)", True, GRAY), (plot_area.right - 30, plot_area.bottom + 4))
        screen.blit(font_title.render("x (m)", True, GRAY), (plot_area.x + 2, plot_area.top - 14))

        sim_pts = [to_px(t, x) for t, x in zip(th, xh)]
        pygame.draw.lines(screen, ACCENT, False, sim_pts, 2)

        if ns.show_ideal:
            pygame.draw.lines(screen, GREEN, False, [to_px(t, x) for t, x in zip(th, mru_vals)], 1)
            pygame.draw.lines(screen, ORANGE, False, [to_px(t, x) for t, x in zip(th, mrua_vals)], 1)

        legend = [("Simulado", ACCENT), ("MRU ideal", GREEN), ("MRUA ideal", ORANGE)]
        lx = rect.right - 190
        ly = rect.y + 8
        for i, (lbl, col) in enumerate(legend):
            pygame.draw.line(screen, col, (lx, ly + i * 16 + 6), (lx + 18, ly + i * 16 + 6), 3)
            screen.blit(font_title.render(lbl, True, col), (lx + 24, ly + i * 16))


# ═══════════════════════════ MAIN ═══════════════════════════

if __name__ == "__main__":
    game = Game()
    game.run()
