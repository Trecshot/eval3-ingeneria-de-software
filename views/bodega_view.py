"""
Módulo de Vista de Bodega e Inventario (views/bodega_view.py)
Requerimientos Cubiertos: RF-08 (Recepción O/C), RF-10 (Control Stock), RF-11 (Alertas FEFO)
"""
import customtkinter as ctk
from tkinter import messagebox
import theme as th


class BodegaView(ctk.CTkFrame):
    def __init__(self, master, data_store):
        super().__init__(master, fg_color=th.COLOR_BACKGROUND)
        self.data_store = data_store
        
        self.tabs = ctk.CTkTabview(self, fg_color=th.COLOR_PANEL)
        self.tabs.pack(fill="both", expand=True, padx=25, pady=15)
        
        self.tab_rec = self.tabs.add("Recepción contra O/C (RF-08)")
        self.tab_stock = self.tabs.add("Control de Stock Físico (RF-10)")
        self.tab_alertas = self.tabs.add("Centro de Alertas FEFO (RF-11)")
        
        self._setup_recepcion()
        self._setup_stock()
        self._setup_alertas()

    def _setup_recepcion(self):
        frame = self.tab_rec
        lbl = ctk.CTkLabel(
            frame, 
            text="Recepción de Mercaderías contra Orden de Compra", 
            font=ctk.CTkFont(family=th.FONT_FAMILY, size=th.FONT_SIZE_SUBTITLE, weight="bold")
        )
        lbl.pack(anchor="w", padx=15, pady=(10, 5))
        
        f_top = ctk.CTkFrame(frame, fg_color="transparent")
        f_top.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(f_top, text="Orden de Compra:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=5)
        self.cb_oc = ctk.CTkComboBox(
            f_top, 
            values=["OC-2026-8901 (Distribuidora del Sur)", "OC-2026-8902 (Molinos Temuco)", "OC-2026-8903 (Lácteos Araucanía)"],
            width=260
        )
        self.cb_oc.grid(row=0, column=1, padx=10, sticky="w")
        
        ctk.CTkLabel(f_top, text="Bodega Destino:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, sticky="w", padx=5)
        self.cb_bodega_rec = ctk.CTkComboBox(
            f_top, 
            values=["Temuco - Centro Principal (4.500 m²)", "Angol - Bodega Regional (800 m²)"],
            width=260
        )
        self.cb_bodega_rec.grid(row=0, column=3, padx=10, sticky="w")

        f_item = ctk.CTkFrame(frame, fg_color=th.COLOR_CARD_BG, corner_radius=8)
        f_item.pack(fill="x", padx=15, pady=10)
        
        self.in_sku = self._mini_campo(f_item, "Producto / SKU:", 0, "AR-001 - Aceite Vegetal 1L")
        self.in_cant_oc = self._mini_campo(f_item, "Cant. Comprada:", 1, "500")
        self.in_cant_rec = self._mini_campo(f_item, "Cant. Recibida:", 2, "480")
        self.in_lote = self._mini_campo(f_item, "Código Lote:", 3, "L-2026-OCT-09")
        self.in_venc = self._mini_campo(f_item, "Fecha Vencimiento:", 4, "2027-04-15")
        
        btn_ingreso = ctk.CTkButton(
            frame, 
            text="Confirmar Recepción y Calcular Diferencias", 
            fg_color=th.COLOR_PRIMARY, 
            hover_color=th.COLOR_SECONDARY, 
            command=self._procesar_recepcion
        )
        btn_ingreso.pack(padx=15, pady=10, anchor="e")
        
        self.lbl_resultado_rec = ctk.CTkLabel(frame, text="Estado: En espera de recepción transaccional.", font=ctk.CTkFont(size=th.FONT_SIZE_BODY, slant="italic"))
        self.lbl_resultado_rec.pack(anchor="w", padx=15, pady=5)

    def _mini_campo(self, parent, label, col, default_val):
        lbl = ctk.CTkLabel(parent, text=label, font=ctk.CTkFont(size=th.FONT_SIZE_CAPTION, weight="bold"))
        lbl.grid(row=0, column=col, padx=8, pady=(8, 2), sticky="w")
        entry = ctk.CTkEntry(parent, width=170)
        entry.insert(0, default_val)
        entry.grid(row=1, column=col, padx=8, pady=(0, 10))
        return entry

    def _procesar_recepcion(self):
        try:
            esp = int(self.in_cant_oc.get())
            rec = int(self.in_cant_rec.get())
            dif = rec - esp
            lote = self.in_lote.get()
            prod = self.in_sku.get()
            
            estado_dif = f"DIFERENCIA: {dif} unidades"
            if dif < 0:
                color_msg = th.COLOR_DANGER
                estado_dif += " (Faltante detectado - Notificación a Adquisiciones)"
            elif dif > 0:
                color_msg = th.COLOR_WARNING
                estado_dif += " (Excedente no regularizado)"
            else:
                color_msg = th.COLOR_SUCCESS
                estado_dif += " (Conforme al 100%)"
                
            self.lbl_resultado_rec.configure(
                text=f"Recepción procesada: {prod} | Lote: {lote} | {estado_dif}",
                text_color=color_msg
            )
            messagebox.showinfo("Recepción Finalizada", f"Mercadería asentada en sistema.\nLote: {lote}\n{estado_dif}")
        except ValueError:
            messagebox.showerror("Error", "Las cantidades de recepción deben corresponder a números enteros.")

    def _setup_stock(self):
        frame = self.tab_stock
        lbl = ctk.CTkLabel(
            frame, 
            text="Control de Stock por Producto, Lote y Ubicación Física", 
            font=ctk.CTkFont(family=th.FONT_FAMILY, size=th.FONT_SIZE_SUBTITLE, weight="bold")
        )
        lbl.pack(anchor="w", padx=15, pady=(10, 10))
        
        self.scroll_stock = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        self.scroll_stock.pack(fill="both", expand=True, padx=15, pady=10)
        
        for item in self.data_store["stock"]:
            card = ctk.CTkFrame(self.scroll_stock, fg_color=th.COLOR_BACKGROUND, border_width=1, border_color=th.COLOR_BORDER)
            card.pack(fill="x", pady=4, padx=5)
            
            txt_izq = f"[{item['sku']}] {item['nombre']}  |  Lote: {item['lote']}  |  Vence: {item['vence']}"
            txt_der = f"Ubicación: {item['ubicacion']}  |  Stock Físico: {item['cantidad']} un. (Umbral Mínimo: {item['minimo']})"
            
            ctk.CTkLabel(card, text=txt_izq, font=ctk.CTkFont(size=th.FONT_SIZE_BODY, weight="bold"), text_color=th.COLOR_TEXT_MAIN).pack(anchor="w", padx=10, pady=(6, 1))
            ctk.CTkLabel(card, text=txt_der, font=ctk.CTkFont(size=th.FONT_SIZE_CAPTION), text_color=th.COLOR_TEXT_MUTED).pack(anchor="w", padx=10, pady=(1, 6))

    def _setup_alertas(self):
        frame = self.tab_alertas
        lbl = ctk.CTkLabel(
            frame, 
            text="Tablero de Alertas Críticas de Inventario (Regla FEFO)", 
            font=ctk.CTkFont(family=th.FONT_FAMILY, size=th.FONT_SIZE_SUBTITLE, weight="bold")
        )
        lbl.pack(anchor="w", padx=15, pady=(10, 10))
        
        kpi_frame = ctk.CTkFrame(frame, fg_color="transparent")
        kpi_frame.pack(fill="x", padx=15, pady=5)
        
        self._card_kpi(kpi_frame, "Quiebres de Stock", "1 Lote", th.COLOR_DANGER, 0)
        self._card_kpi(kpi_frame, "Próximos a Vencer (< 30 días)", "2 Lotes", th.COLOR_WARNING, 1)
        self._card_kpi(kpi_frame, "Mermas Mitigadas", "2.8% Anual", th.COLOR_SUCCESS, 2)
        
        scroll_alert = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        scroll_alert.pack(fill="both", expand=True, padx=15, pady=15)
        
        alertas = [
            ("CRÍTICO", "Harina Selecta 1kg (L-HAR-902) vencimiento en 8 días. Despachar de inmediato según política FEFO.", th.COLOR_DANGER),
            ("ADVERTENCIA", "Leche Entera 1L (L-LEC-310) alcanza 40 unidades (Umbral mínimo: 50 unidades). Generar O/C.", th.COLOR_WARNING),
            ("ADVERTENCIA", "Arroz Grano Largo (L-AR-114) próximo a cumplir 25 días para expirar en Bodega Angol.", th.COLOR_WARNING),
        ]
        
        for nivel, msg, col in alertas:
            c = ctk.CTkFrame(scroll_alert, fg_color=th.COLOR_PANEL, border_width=2, border_color=col)
            c.pack(fill="x", pady=6, padx=5)
            ctk.CTkLabel(c, text=f"[{nivel}] {msg}", font=ctk.CTkFont(size=th.FONT_SIZE_BODY, weight="bold"), text_color=col).pack(anchor="w", padx=15, pady=12)

    def _card_kpi(self, parent, title, val, color, col):
        card = ctk.CTkFrame(parent, fg_color=th.COLOR_PANEL, corner_radius=10, border_width=1, border_color="#CBD5E1")
        card.grid(row=0, column=col, padx=10, pady=5, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=th.FONT_SIZE_BODY, weight="bold"), text_color=th.COLOR_TEXT_MUTED).pack(padx=15, pady=(10, 2))
        ctk.CTkLabel(card, text=val, font=ctk.CTkFont(size=22, weight="bold"), text_color=color).pack(padx=15, pady=(2, 10))
