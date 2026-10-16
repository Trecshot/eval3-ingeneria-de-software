"""
Sistema de Gestión Comercial, Inventario y Distribución (DistriGest)
Firma Desarrolladora: Bomcode
Caso de Estudio: DistriSur Araucanía SpA - Inacap Sede Temuco
Evaluación 3: Prototipo Funcional en Python (Arquitectura Modular)
Controlador Principal de Aplicación
"""
import customtkinter as ctk
import theme as th
from views import (
    ClientesView,
    BodegaView,
    FacturacionView,
    ProveedoresView,
    ReportesView
)

# Inicialización de Parámetros Globales desde el módulo de estilos
ctk.set_appearance_mode(th.APPEARANCE_MODE)
ctk.set_default_color_theme(th.COLOR_THEME)


class DistriGestApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("DistriGest v1.0 - Prototipo Modular (DistriSur Araucanía SpA)")
        self.geometry("1280x760")
        self.minsize(1100, 680)
        
        # Repositorio Simulado en Memoria Local
        self.data_store = {
            "clientes": [
                {
                    "rut": "76.432.123-K",
                    "razon_social": "Supermercado La Araucana SpA",
                    "giro": "Supermercado",
                    "direccion": "Av. Alemania 0850",
                    "contacto": "Juan Morales - +56 9 8765 4321",
                    "zona": "Temuco Centro",
                    "vendedor": "Juan Pérez",
                    "cupo_credito": 15000000,
                    "mora": 0
                },
                {
                    "rut": "78.901.234-5",
                    "razon_social": "Minimarket Central Angol",
                    "giro": "Comercio Minorista",
                    "direccion": "Calle Prat 432",
                    "contacto": "Claudia Venegas - +56 9 1234 5678",
                    "zona": "Angol",
                    "vendedor": "María Soto",
                    "cupo_credito": 4000000,
                    "mora": 12
                },
            ],
            "stock": [
                {"sku": "ACE-001", "nombre": "Aceite Vegetal 1L", "lote": "L-2026-OCT-01", "vence": "2027-05-10", "ubicacion": "TEM-P01-E02", "cantidad": 450, "minimo": 100},
                {"sku": "HAR-002", "nombre": "Harina Selecta 1kg", "lote": "L-HAR-902", "vence": "2026-10-17", "ubicacion": "TEM-P03-E01", "cantidad": 20, "minimo": 80},
                {"sku": "ARR-003", "nombre": "Arroz Grano Largo 1kg", "lote": "L-AR-114", "vence": "2026-11-03", "ubicacion": "ANG-P01-E04", "cantidad": 280, "minimo": 150},
            ],
            "proveedores": [
                {"rut": "96.555.222-1", "razon": "Distribuidora Nacional de Alimentos S.A.", "plazo": "30 Días Fecha Factura", "desc": "3.0"},
                {"rut": "77.888.999-K", "razon": "Molinos Temuco Industrial", "plazo": "60 Días Fecha Factura", "desc": "5.0"}
            ]
        }
        
        # Arquitectura de Contenedores y Navegación
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=th.COLOR_SIDEBAR_BG)
        self.sidebar.pack(side="left", fill="y")
        
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color=th.COLOR_BG_MAIN)
        self.main_container.pack(side="right", fill="both", expand=True)
        
        self.lista_botones_menu = []
        self.botones_vistas = {}
        
        self._build_sidebar()
        
        # Instanciación Dinámica de Vistas Desacopladas
        self.views = {
            "clientes": ClientesView(self.main_container, self.data_store),
            "bodega": BodegaView(self.main_container, self.data_store),
            "facturacion": FacturacionView(self.main_container, self.data_store),
            "proveedores": ProveedoresView(self.main_container, self.data_store),
            "reportes": ReportesView(self.main_container, self.data_store),
        }
        
        self.mostrar_vista("clientes")

    def _build_sidebar(self):
        lbl_brand = ctk.CTkLabel(
            self.sidebar, 
            text="DistriGest", 
            font=ctk.CTkFont(family=th.FONT_FAMILY, size=22, weight="bold"),
            text_color=th.COLOR_TEXT_LIGHT
        )
        lbl_brand.pack(padx=20, pady=(25, 5), anchor="w")
        
        lbl_sub = ctk.CTkLabel(
            self.sidebar, 
            text="DistriSur Araucanía SpA", 
            font=ctk.CTkFont(size=th.FONT_SIZE_BODY),
            text_color=th.COLOR_TEXT_ACCENT
        )
        lbl_sub.pack(padx=20, pady=(0, 25), anchor="w")
        
        self.botones_vistas["clientes"] = self._btn_menu("Clientes (RF-01)", lambda: self.mostrar_vista("clientes"))
        self.botones_vistas["bodega"] = self._btn_menu("Inventario y Bodega (C)", lambda: self.mostrar_vista("bodega"))
        self.botones_vistas["facturacion"] = self._btn_menu("Facturación DTE (RF-17)", lambda: self.mostrar_vista("facturacion"))
        self.botones_vistas["proveedores"] = self._btn_menu("Proveedores (RF-20)", lambda: self.mostrar_vista("proveedores"))
        self.botones_vistas["reportes"] = self._btn_menu("Reportes y Comisiones (G)", lambda: self.mostrar_vista("reportes"))

    def _btn_menu(self, text, command):
        btn = ctk.CTkButton(
            self.sidebar, 
            text=text, 
            font=("Segoe UI", 12, "normal"),
            fg_color="transparent", 
            text_color=th.COLOR_TEXT_LIGHT,
            hover_color=th.COLOR_PRIMARY_HOVER,
            anchor="w",
            height=42,
            corner_radius=th.RADIUS_INPUT,
            command=command
        )
        btn.pack(fill="x", padx=12, pady=4)
        self.lista_botones_menu.append(btn)
        return btn

    def actualizar_estado_sidebar(self, boton_activo):
        for btn in self.lista_botones_menu:
            if btn == boton_activo:
                btn.configure(
                    fg_color=th.COLOR_SIDEBAR_ACTIVE,
                    font=("Segoe UI", 12, "bold")
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    font=("Segoe UI", 12, "normal")
                )

    def mostrar_vista(self, nombre_vista):
        for v in self.views.values():
            v.pack_forget()
        self.views[nombre_vista].pack(fill="both", expand=True)
        if nombre_vista in self.botones_vistas:
            self.actualizar_estado_sidebar(self.botones_vistas[nombre_vista])


if __name__ == "__main__":
    app = DistriGestApp()
    app.mainloop()