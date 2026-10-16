"""
Módulo de Vista de Reportes e Indicadores (views/reportes_view.py)
Requerimientos Cubiertos: RF-23 (Ventas Multidimensionales), RF-25 (Liquidación de Comisiones)
"""
import customtkinter as ctk
import theme as th


class ReportesView(ctk.CTkFrame):
    def __init__(self, master, data_store):
        super().__init__(master, fg_color=th.COLOR_BACKGROUND)
        self.data_store = data_store
        
        self.tabs = ctk.CTkTabview(self, fg_color=th.COLOR_PANEL)
        self.tabs.pack(fill="both", expand=True, padx=25, pady=15)
        
        self.tab_ventas = self.tabs.add("Reporte Multidimensional de Ventas (RF-23)")
        self.tab_comisiones = self.tabs.add("Liquidación de Comisiones de Vendedores (RF-25)")
        
        self._setup_ventas()
        self._setup_comisiones()

    def _setup_ventas(self):
        f = self.tab_ventas
        lbl = ctk.CTkLabel(
            f, 
            text="Panel Analítico de Ventas por Dimensiones Geográficas", 
            font=ctk.CTkFont(family=th.FONT_FAMILY, size=th.FONT_SIZE_SUBTITLE, weight="bold")
        )
        lbl.pack(anchor="w", padx=15, pady=(10, 10))
        
        f_filtros = ctk.CTkFrame(f, fg_color=th.COLOR_CARD_BG, corner_radius=8)
        f_filtros.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(f_filtros, text="Zona:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=8, pady=8)
        cb_z = ctk.CTkComboBox(f_filtros, values=["Todas las Zonas", "Temuco Centro", "Padre Las Casas", "Angol"], width=160)
        cb_z.grid(row=0, column=1, padx=5, pady=8)
        
        ctk.CTkLabel(f_filtros, text="Vendedor:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, padx=8, pady=8)
        cb_v = ctk.CTkComboBox(f_filtros, values=["Todos los Vendedores", "Juan Pérez", "María Soto", "Carlos Lagos"], width=180)
        cb_v.grid(row=0, column=3, padx=5, pady=8)
        
        btn_filtrar = ctk.CTkButton(f_filtros, text="Aplicar Filtros", fg_color=th.COLOR_PRIMARY, hover_color=th.COLOR_SECONDARY, width=120)
        btn_filtrar.grid(row=0, column=4, padx=15, pady=8)
        
        scroll_rep = ctk.CTkScrollableFrame(f, fg_color="transparent")
        scroll_rep.pack(fill="both", expand=True, padx=15, pady=10)
        
        ventas_demo = [
            ("2026-10-08", "Supermercado La Araucana", "Temuco Centro", "Juan Pérez", "Aceite Vegetal 1L", 150, "$ 270.000"),
            ("2026-10-08", "Minimarket Angol", "Angol", "María Soto", "Harina Selecta 1kg", 300, "$ 285.000"),
            ("2026-10-09", "Comercial Padre Las Casas", "Padre Las Casas", "Carlos Lagos", "Arroz Grano Largo", 200, "$ 260.000"),
        ]
        
        for fecha, cli, zona, vend, prod, cant, tot in ventas_demo:
            card = ctk.CTkFrame(scroll_rep, fg_color=th.COLOR_BACKGROUND, border_width=1, border_color=th.COLOR_BORDER)
            card.pack(fill="x", pady=4, padx=5)
            linea1 = f"Fecha: {fecha}  |  Cliente: {cli}  |  Zona: {zona}  |  Vendedor: {vend}"
            linea2 = f"Producto: {prod}  |  Cantidad: {cant} un.  |  TOTAL VENTA: {tot} CLP"
            ctk.CTkLabel(card, text=linea1, font=ctk.CTkFont(size=th.FONT_SIZE_BODY, weight="bold"), text_color=th.COLOR_TEXT_MAIN).pack(anchor="w", padx=10, pady=(6, 1))
            ctk.CTkLabel(card, text=linea2, font=ctk.CTkFont(size=th.FONT_SIZE_CAPTION), text_color=th.COLOR_PRIMARY).pack(anchor="w", padx=10, pady=(1, 6))

    def _setup_comisiones(self):
        f = self.tab_comisiones
        lbl = ctk.CTkLabel(
            f, 
            text="Cálculo Algorítmico de Comisiones Cruzadas con Cobranza Efectiva", 
            font=ctk.CTkFont(family=th.FONT_FAMILY, size=th.FONT_SIZE_SUBTITLE, weight="bold")
        )
        lbl.pack(anchor="w", padx=15, pady=(10, 5))
        
        desc = ctk.CTkLabel(f, text="Regla de Negocio: 3.0% base sobre facturación, ajustado por retorno de cobranza (< 47 días).", font=ctk.CTkFont(size=th.FONT_SIZE_BODY, slant="italic"))
        desc.pack(anchor="w", padx=15, pady=(0, 10))
        
        scroll_com = ctk.CTkScrollableFrame(f, fg_color="transparent")
        scroll_com.pack(fill="both", expand=True, padx=15, pady=5)
        
        vendedores = [
            ("VEND-01", "Juan Pérez", "$ 18.500.000", "$ 17.200.000 (93%)", "3.0%", "$ 516.000"),
            ("VEND-02", "María Soto", "$ 22.100.000", "$ 21.000.000 (95%)", "3.0%", "$ 630.000"),
            ("VEND-03", "Carlos Lagos", "$ 14.200.000", "$ 11.500.000 (81%)", "2.5%*", "$ 287.500"),
        ]
        
        for vid, nom, fact, cobr, tasa, total_com in vendedores:
            c = ctk.CTkFrame(scroll_com, fg_color=th.COLOR_BACKGROUND, border_width=1, border_color="#CBD5E1")
            c.pack(fill="x", pady=6, padx=5)
            
            t1 = f"[{vid}] {nom}  |  Facturación Mensual: {fact}  |  Cobranza Efectiva: {cobr}"
            t2 = f"Tasa Aplicada: {tasa}  |  COMISIÓN A LIQUIDAR: {total_com} CLP"
            
            ctk.CTkLabel(c, text=t1, font=ctk.CTkFont(size=th.FONT_SIZE_BODY, weight="bold"), text_color=th.COLOR_TEXT_MAIN).pack(anchor="w", padx=12, pady=(8, 2))
            ctk.CTkLabel(c, text=t2, font=ctk.CTkFont(size=th.FONT_SIZE_BODY, weight="bold"), text_color=th.COLOR_SUCCESS).pack(anchor="w", padx=12, pady=(2, 8))
