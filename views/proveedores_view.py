"""
Módulo de Vista de Proveedores y Compras (views/proveedores_view.py)
Requerimiento Cubierto: RF-20 (Mantenedor de Proveedores y Condiciones Comerciales)
"""
import customtkinter as ctk
from tkinter import messagebox
import theme as th


class ProveedoresView(ctk.CTkFrame):
    def __init__(self, master, data_store):
        super().__init__(master, fg_color=th.COLOR_BACKGROUND)
        self.data_store = data_store
        
        header = ctk.CTkLabel(
            self, 
            text="Módulo F: Registro de Proveedores y Condiciones Comerciales (RF-20)", 
            font=ctk.CTkFont(family=th.FONT_FAMILY, size=th.FONT_SIZE_TITLE, weight="bold"),
            text_color=th.COLOR_TEXT_MAIN
        )
        header.pack(anchor="w", padx=25, pady=(20, 10))
        
        content = ctk.CTkFrame(self, fg_color=th.COLOR_PANEL, corner_radius=10)
        content.pack(fill="both", expand=True, padx=25, pady=10)
        
        f_izq = ctk.CTkFrame(content, fg_color="transparent")
        f_izq.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        lbl_p = ctk.CTkLabel(f_izq, text="Ficha Comercial de Proveedor", font=ctk.CTkFont(family=th.FONT_FAMILY, size=th.FONT_SIZE_SUBTITLE, weight="bold"))
        lbl_p.pack(anchor="w", pady=(0, 10))
        
        self.e_prv_rut = self._crear_campo(f_izq, "RUT Proveedor (ej: 96.555.222-1):")
        self.e_prv_razon = self._crear_campo(f_izq, "Razón Social Proveedor:")
        self.e_prv_contacto = self._crear_campo(f_izq, "Contacto Comercial / Teléfono:")
        
        lbl_plazo = ctk.CTkLabel(f_izq, text="Plazo de Crédito Comercial:", font=ctk.CTkFont(weight="bold"))
        lbl_plazo.pack(anchor="w", pady=(5, 2))
        self.cb_plazo = ctk.CTkComboBox(f_izq, values=["Contado Inmediato", "30 Días Fecha Factura", "60 Días Fecha Factura", "90 Días"])
        self.cb_plazo.pack(fill="x", pady=(0, 8))
        
        self.e_prv_desc = self._crear_campo(f_izq, "Descuento por Pronto Pago (%):")
        self.e_prv_desc.insert(0, "3.5")
        
        btn_reg = ctk.CTkButton(
            f_izq, 
            text="Registrar Proveedor", 
            fg_color=th.COLOR_PRIMARY, 
            hover_color=th.COLOR_SECONDARY, 
            command=self._registrar_proveedor
        )
        btn_reg.pack(fill="x", pady=15)
        
        f_der = ctk.CTkFrame(content, fg_color="transparent")
        f_der.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(f_der, text="Proveedores Habilitados para Compras", font=ctk.CTkFont(family=th.FONT_FAMILY, size=th.FONT_SIZE_SUBTITLE, weight="bold")).pack(anchor="w", pady=(0, 10))
        self.scroll_prv = ctk.CTkScrollableFrame(f_der, fg_color=th.COLOR_BACKGROUND)
        self.scroll_prv.pack(fill="both", expand=True)
        self._refrescar_proveedores()

    def _crear_campo(self, parent, text):
        ctk.CTkLabel(parent, text=text, font=ctk.CTkFont(size=th.FONT_SIZE_BODY, weight="bold")).pack(anchor="w", pady=(4, 2))
        e = ctk.CTkEntry(parent)
        e.pack(fill="x", pady=(0, 6))
        return e

    def _registrar_proveedor(self):
        rut = self.e_prv_rut.get().strip()
        razon = self.e_prv_razon.get().strip()
        if not rut or not razon:
            messagebox.showwarning("Atención", "RUT y Razón Social de proveedor son requeridos.")
            return
        prv = {
            "rut": rut,
            "razon": razon,
            "plazo": self.cb_plazo.get(),
            "desc": self.e_prv_desc.get().strip() or "0"
        }
        self.data_store["proveedores"].append(prv)
        messagebox.showinfo("Registro Exitoso", f"Condiciones de abastecimiento registradas para {razon}.")
        self._refrescar_proveedores()

    def _refrescar_proveedores(self):
        for w in self.scroll_prv.winfo_children():
            w.destroy()
        for p in self.data_store["proveedores"]:
            c = ctk.CTkFrame(self.scroll_prv, fg_color=th.COLOR_PANEL, border_width=1, border_color=th.COLOR_BORDER)
            c.pack(fill="x", pady=4, padx=5)
            ctk.CTkLabel(c, text=f"{p['razon']}  |  RUT: {p['rut']}", font=ctk.CTkFont(weight="bold"), text_color=th.COLOR_TEXT_MAIN).pack(anchor="w", padx=10, pady=(5, 1))
            ctk.CTkLabel(c, text=f"Condición: {p['plazo']}  |  Desc. Pronto Pago: {p['desc']}%", font=ctk.CTkFont(size=th.FONT_SIZE_CAPTION), text_color=th.COLOR_TEXT_MUTED).pack(anchor="w", padx=10, pady=(1, 5))
