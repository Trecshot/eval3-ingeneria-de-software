"""
Módulo de Configuración Visual y Tokens de Diseño (theme.py)
Proyecto: DistriGest - DistriSur Araucanía SpA
Estándar de Accesibilidad: WCAG 2.1 Nivel AA
Firma Desarrolladora: Bomcode
"""

# Configuración del Motor Gráfico CustomTkinter
APPEARANCE_MODE = "Light"
COLOR_THEME = "blue"

# ==============================================================================
# 1. PALETA CROMÁTICA INSTITUCIONAL Y SEMÁNTICA (CONFORMIDAD WCAG AA)
# ==============================================================================
COLOR_PRIMARY = "#1E3A8A"        # Azul Petróleo (Acciones primarias / Barra de títulos)
COLOR_PRIMARY_HOVER = "#1D4ED8"  # Estado hover para botones principales
COLOR_SIDEBAR_BG = "#172554"     # Fondo menú lateral (Azul profundo)
COLOR_SIDEBAR_ACTIVE = "#2563EB" # Indicador de módulo activo
COLOR_BG_MAIN = "#F8FAFC"        # Fondo neutro claro de trabajo
COLOR_CARD_BG = "#FFFFFF"        # Fondo de tarjetas y paneles
COLOR_BORDER = "#E2E8F0"         # Bordes sutiles de delimitación
COLOR_BORDER_FOCUS = "#3B82F6"   # Borde activo de campos de texto

# Tipografías y Colores de Texto
COLOR_TEXT_MAIN = "#0F172A"      # Títulos y datos prioritarios (Alto contraste)
COLOR_TEXT_MUTED = "#64748B"     # Metadatos secundarios, etiquetas auxiliares
COLOR_SUCCESS = "#15803D"        # Estados aprobados / Cupos financieros

FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_SUBTITLE = ("Segoe UI", 14, "bold")
FONT_LABEL = ("Segoe UI", 12, "bold")
FONT_BODY = ("Segoe UI", 12)
FONT_CAPTION = ("Segoe UI", 11)
FONT_BADGE = ("Segoe UI", 10, "bold")

# Geometría y Dimensiones Estándar
RADIUS_CARD = 8
RADIUS_INPUT = 6
HEIGHT_INPUT = 34
HEIGHT_BUTTON = 38

# ==============================================================================
# 2. TOKENS DE COMPATIBILIDAD CON VISTAS MODULARES EXISTENTES
# ==============================================================================
COLOR_SECONDARY = "#3B82F6"
COLOR_HOVER_PRIMARY = COLOR_PRIMARY_HOVER
COLOR_BACKGROUND = COLOR_BG_MAIN
COLOR_PANEL = COLOR_CARD_BG
COLOR_TEXT_LIGHT = "#FFFFFF"
COLOR_TEXT_ACCENT = "#93C5FD"
COLOR_WARNING = "#B45309"
COLOR_DANGER = "#B91C1C"

FONT_FAMILY = "Segoe UI"
FONT_SIZE_TITLE = 18
FONT_SIZE_SUBTITLE = 14
FONT_SIZE_SECTION = 14
FONT_SIZE_BODY = 12
FONT_SIZE_CAPTION = 11