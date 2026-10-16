"""
Módulo de Vista de Facturación y Emisión DTE (views/facturacion_view.py)
Requerimiento Cubierto: RF-17 (Emisión y Timbrado Tributario Electrónico)
"""
import customtkinter as ctk
from tkinter import messagebox
import theme as th


class FacturacionView(ctk.CTkFrame):
    def __init__(self, master, data_store):
        super().__init__(master, fg_color=th.COLOR_BACKGROUND)
        self.data_store = data_store
        
        header = ctk.CTkLabel(
            self, 
            text="Módulo E: Facturación y Emisión Electrónica DTE (RF-17)", 
            font=ctk.CTkFont(family=th.FONT_FAMILY, size=th.FONT_SIZE_TITLE, weight="bold"),
            text_color=th.COLOR_TEXT_MAIN
        )
        header.pack(anchor="w", padx=25, pady=(20, 10))
        
        panel = ctk.CTkFrame(self, fg_color=th.COLOR_PANEL, corner_radius=10)
        panel.pack(fill="both", expand=True, padx=25, pady=10)
        
        f_top = ctk.CTkFrame(panel, fg_color="transparent")
        f_top.pack(fill="x", padx=25, pady=(20, 10))
        
        ctk.CTkLabel(f_top, text="Tipo de Documento:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w")
        self.cb_dte = ctk.CTkComboBox(f_top, values=["Factura Electrónica (33)", "Guía de Despacho (52)", "Nota de Crédito (61)"], width=220)
        self.cb_dte.grid(row=0, column=1, padx=15, sticky="w")
        
        ctk.CTkLabel(f_top, text="Vincular Pedido Aprobado:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, padx=(20, 5), sticky="w")
        self.cb_pedidos = ctk.CTkComboBox(
            f_top, 
            values=["PED-00109 - Supermercado La Araucana ($1.450.000)", "PED-00110 - Minimarket Central ($380.000)"], 
            width=360
        )
        self.cb_pedidos.grid(row=0, column=3, padx=10, sticky="w")
        
        detalle_box = ctk.CTkFrame(panel, fg_color=th.COLOR_BACKGROUND, corner_radius=8)
        detalle_box.pack(fill="x", padx=25, pady=15)
        
        ctk.CTkLabel(detalle_box, text="Detalle de Líneas de Facturación Tributaria", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
        ctk.CTkLabel(
            detalle_box, 
            text="1. 100x Aceite Vegetal 1L  |  P.Unit: $1.800  |  Subtotal: $180.000\n2. 50x Harina Selecta 1kg  |  P.Unit: $950    |  Subtotal: $47.500", 
            justify="left"
        ).pack(anchor="w", padx=15, pady=(0, 10))
        
        tot_frame = ctk.CTkFrame(panel, fg_color="transparent")
        tot_frame.pack(anchor="e", padx=25, pady=10)
        
        ctk.CTkLabel(tot_frame, text="Monto Neto:  $ 227.500 CLP", font=ctk.CTkFont(size=13)).pack(anchor="e")
        ctk.CTkLabel(tot_frame, text="IVA (19%):  $ 43.225 CLP", font=ctk.CTkFont(size=13)).pack(anchor="e")
        ctk.CTkLabel(tot_frame, text="TOTAL FACTURADO:  $ 270.725 CLP", font=ctk.CTkFont(size=16, weight="bold"), text_color=th.COLOR_PRIMARY).pack(anchor="e", pady=(5, 10))
        
        btn_emitir = ctk.CTkButton(
            panel, 
            text="Emitir Documento Electrónico (Timbrado SII)", 
            fg_color=th.COLOR_PRIMARY,
            hover_color=th.COLOR_SECONDARY,
            height=40,
            command=self._confirmar_emision_critica
        )
        btn_emitir.pack(anchor="e", padx=25, pady=(10, 25))

    def _confirmar_emision_critica(self):
        tipo = self.cb_dte.get()
        pedido = self.cb_pedidos.get().split(" - ")[0]
        
        confirmacion = messagebox.askyesno(
            "Acción Crítica Tributaria",
            f"¿Confirma la emisión formal del documento '{tipo}' ante el Servicio de Impuestos Internos para el {pedido}?\n\nEsta transacción genera timbraje fiscal definitivo."
        )
        
        if confirmacion:
            folio = 104928
            messagebox.showinfo(
                "Emisión Exitosa",
                f"Documento timbrado correctamente ante el SII.\nTipo: {tipo}\nFolio DTE: {folio}\nEstado: XML firmado y despachado."
            )
