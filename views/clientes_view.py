"""
Módulo de Vista de Clientes (views/clientes_view.py)
Requerimiento Cubierto: RF-01 (Ficha Técnica y Gestión Comercial de Clientes)
Estándar: WCAG 2.1 Nivel AA y Reglas de Proximidad / Usabilidad
"""

import customtkinter as ctk
from tkinter import messagebox
from theme import *


def validar_rut_chileno(rut_str: str) -> bool:
    """Valida el dígito verificador módulo 11 de un RUT nacional chileno."""
    rut_limpio = rut_str.replace(".", "").replace("-", "").strip().upper()
    if len(rut_limpio) < 2:
        return False
    cuerpo = rut_limpio[:-1]
    dv = rut_limpio[-1]
    if not cuerpo.isdigit():
        return False
    
    suma = 0
    multiplo = 2
    for c in reversed(cuerpo):
        suma += int(c) * multiplo
        multiplo = 2 if multiplo == 7 else multiplo + 1
        
    esperado_num = 11 - (suma % 11)
    if esperado_num == 11:
        esperado_dv = '0'
    elif esperado_num == 10:
        esperado_dv = 'K'
    else:
        esperado_dv = str(esperado_num)
        
    return dv == esperado_dv


class FormularioFichaCliente(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self._construir_interfaz()

    def _crear_campo(self, contenedor, etiqueta, placeholder, row):
        """Genera un bloque de entrada estandarizado con alta legibilidad."""
        lbl = ctk.CTkLabel(
            contenedor, 
            text=etiqueta, 
            font=FONT_LABEL, 
            text_color=COLOR_TEXT_MAIN, 
            anchor="w"
        )
        lbl.grid(row=row, column=0, sticky="w", pady=(6, 2), padx=12)

        entry = ctk.CTkEntry(
            contenedor,
            placeholder_text=placeholder,
            height=HEIGHT_INPUT,
            corner_radius=RADIUS_INPUT,
            border_width=1,
            border_color=COLOR_BORDER,
            fg_color=COLOR_CARD_BG,
            text_color=COLOR_TEXT_MAIN,
            font=FONT_BODY
        )
        entry.grid(row=row+1, column=0, sticky="ew", pady=(0, 4), padx=12)
        return entry

    def _construir_interfaz(self):
        self.grid_columnconfigure(0, weight=1)

        # Título de Sección con línea separadora
        lbl_sec = ctk.CTkLabel(self, text="Ficha Técnica del Cliente", font=FONT_SUBTITLE, text_color=COLOR_TEXT_MAIN)
        lbl_sec.grid(row=0, column=0, sticky="w", pady=(0, 8))

        # Contenedor del Formulario
        form_frame = ctk.CTkFrame(self, fg_color=COLOR_CARD_BG, corner_radius=RADIUS_CARD, border_width=1, border_color=COLOR_BORDER)
        form_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 16), pady=(0, 10))
        form_frame.grid_columnconfigure(0, weight=1)

        # Campos según RF-01
        self.entry_rut = self._crear_campo(form_frame, "RUT (ej: 76.432.123-K):", "Ingrese RUT con formato y guión", 0)
        self.entry_razon = self._crear_campo(form_frame, "Razón Social:", "Nombre comercial o razón social", 2)
        self.entry_giro = self._crear_campo(form_frame, "Giro Comercial:", "Rubro formal SII", 4)
        self.entry_dir = self._crear_campo(form_frame, "Dirección de Despacho:", "Calle, número y comuna", 6)
        self.entry_contacto = self._crear_campo(form_frame, "Contacto / Teléfono:", "Nombre y teléfono directo", 8)

        # Selector: Zona Geográfica
        lbl_zona = ctk.CTkLabel(form_frame, text="Zona Geográfica:", font=FONT_LABEL, text_color=COLOR_TEXT_MAIN, anchor="w")
        lbl_zona.grid(row=10, column=0, sticky="w", pady=(6, 2), padx=12)
        self.opt_zona = ctk.CTkOptionMenu(
            form_frame,
            values=["Temuco Centro", "Padre Las Casas", "Angol", "Villarrica / Pucón"],
            height=HEIGHT_INPUT,
            corner_radius=RADIUS_INPUT,
            fg_color=COLOR_BG_MAIN,
            button_color=COLOR_BORDER,
            text_color=COLOR_TEXT_MAIN,
            font=FONT_BODY
        )
        self.opt_zona.grid(row=11, column=0, sticky="ew", pady=(0, 6), padx=12)

        # Selector: Vendedor Asignado
        lbl_vend = ctk.CTkLabel(form_frame, text="Vendedor Asignado:", font=FONT_LABEL, text_color=COLOR_TEXT_MAIN, anchor="w")
        lbl_vend.grid(row=12, column=0, sticky="w", pady=(6, 2), padx=12)
        self.opt_vendedor = ctk.CTkOptionMenu(
            form_frame,
            values=["Juan Pérez (Zona Centro)", "María Soto (Zona Norte)", "Carlos Henríquez (Zona Lacustre)"],
            height=HEIGHT_INPUT,
            corner_radius=RADIUS_INPUT,
            fg_color=COLOR_BG_MAIN,
            button_color=COLOR_BORDER,
            text_color=COLOR_TEXT_MAIN,
            font=FONT_BODY
        )
        self.opt_vendedor.grid(row=13, column=0, sticky="ew", pady=(0, 6), padx=12)

        # Campo: Cupo de Crédito
        self.entry_credito = self._crear_campo(form_frame, "Cupo de Crédito Máximo ($ CLP):", "5000000", 14)

        # Botón de Acción Principal (Call to Action)
        self.btn_guardar = ctk.CTkButton(
            self,
            text="Guardar Cliente",
            command=self.controller.guardar_cliente,
            height=HEIGHT_BUTTON,
            corner_radius=RADIUS_INPUT,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            font=("Segoe UI", 13, "bold")
        )
        self.btn_guardar.grid(row=2, column=0, sticky="ew", padx=(0, 16), pady=(8, 0))


class TarjetaCliente(ctk.CTkFrame):
    """Componente tipo Card para visualizar clientes sin truncamiento de texto."""
    def __init__(self, parent, cliente_data):
        super().__init__(
            parent,
            fg_color=COLOR_CARD_BG,
            corner_radius=RADIUS_CARD,
            border_width=1,
            border_color=COLOR_BORDER
        )
        self.data = cliente_data
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self._armar_card()

    def _armar_card(self):
        # Fila 1: Razón Social (Izquierda) + Badge de Zona (Derecha)
        nombre_texto = self.data.get("razon_social") or self.data.get("razon", "")
        lbl_nombre = ctk.CTkLabel(
            self,
            text=nombre_texto,
            font=FONT_LABEL,
            text_color=COLOR_TEXT_MAIN,
            anchor="w"
        )
        lbl_nombre.grid(row=0, column=0, sticky="w", padx=(12, 4), pady=(8, 2))

        zona_texto = self.data.get("zona", "Temuco Centro")
        badge_zona = ctk.CTkLabel(
            self,
            text=f"  {zona_texto}  ",
            font=FONT_BADGE,
            text_color="#1E40AF",
            fg_color="#DBEAFE",
            corner_radius=4
        )
        badge_zona.grid(row=0, column=1, sticky="e", padx=(4, 12), pady=(8, 2))

        # Fila 2: Metadatos secundarios (RUT y Vendedor)
        rut_val = self.data.get("rut", "")
        vendedor_val = self.data.get("vendedor", "")
        meta_texto = f"RUT: {rut_val}  •  Vendedor: {vendedor_val}"
        lbl_meta = ctk.CTkLabel(
            self,
            text=meta_texto,
            font=FONT_CAPTION,
            text_color=COLOR_TEXT_MUTED,
            anchor="w"
        )
        lbl_meta.grid(row=1, column=0, columnspan=2, sticky="w", padx=12, pady=(0, 4))

        # Fila 3: Indicador Financiero Destacado (Cupo de Crédito)
        cupo_raw = self.data.get("cupo_credito") if self.data.get("cupo_credito") is not None else self.data.get("cupo", 0)
        try:
            cupo_num = int(cupo_raw)
        except (ValueError, TypeError):
            cupo_num = 0
        cupo_formateado = f"${cupo_num:,}".replace(",", ".")
        lbl_cupo = ctk.CTkLabel(
            self,
            text=f"Cupo Autorizado: {cupo_formateado} CLP",
            font=("Segoe UI", 11, "bold"),
            text_color=COLOR_SUCCESS,
            anchor="w"
        )
        lbl_cupo.grid(row=2, column=0, columnspan=2, sticky="w", padx=12, pady=(0, 8))


class ClientesView(ctk.CTkFrame):
    """Vista Principal del Módulo de Clientes (RF-01)."""
    def __init__(self, master, data_store):
        super().__init__(master, fg_color=COLOR_BG_MAIN)
        self.data_store = data_store
        
        # Cabecera de la Vista
        header = ctk.CTkLabel(
            self, 
            text="Módulo A: Gestión Integral de Clientes (RF-01)", 
            font=FONT_TITLE,
            text_color=COLOR_TEXT_MAIN
        )
        header.pack(anchor="w", padx=25, pady=(20, 10))
        
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=25, pady=10)
        
        # Panel Izquierdo: Formulario Ficha Técnica
        self.formulario = FormularioFichaCliente(content, self)
        self.formulario.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=0)
        
        # Panel Derecho: Nómina de Clientes Activos
        list_container = ctk.CTkFrame(content, fg_color="transparent")
        list_container.pack(side="right", fill="both", expand=True, padx=(10, 0), pady=0)
        
        lbl_list_title = ctk.CTkLabel(
            list_container, 
            text="Nómina de Clientes Activos (DistriSur)", 
            font=FONT_SUBTITLE, 
            text_color=COLOR_TEXT_MAIN
        )
        lbl_list_title.pack(anchor="w", pady=(0, 8))
        
        list_frame = ctk.CTkFrame(
            list_container, 
            fg_color=COLOR_CARD_BG, 
            corner_radius=RADIUS_CARD, 
            border_width=1, 
            border_color=COLOR_BORDER
        )
        list_frame.pack(fill="both", expand=True)
        
        self.scroll_clientes = ctk.CTkScrollableFrame(list_frame, fg_color="transparent")
        self.scroll_clientes.pack(fill="both", expand=True, padx=12, pady=10)
        self.refrescar_lista()

    def guardar_cliente(self):
        rut = self.formulario.entry_rut.get().strip()
        razon = self.formulario.entry_razon.get().strip()
        if not rut or not razon:
            messagebox.showwarning("Atención", "RUT y Razón Social son campos mandatorios.")
            return
        if not validar_rut_chileno(rut):
            messagebox.showerror("Error de Formato", f"El RUT '{rut}' no cumple la validación Módulo 11.")
            return
            
        credito_raw = self.formulario.entry_credito.get().replace("$", "").replace(".", "").strip()
        try:
            cupo_num = int(credito_raw) if credito_raw else 5000000
        except ValueError:
            cupo_num = 5000000

        cliente_nuevo = {
            "rut": rut,
            "razon_social": razon,
            "razon": razon,
            "giro": self.formulario.entry_giro.get().strip() or "Distribución General",
            "direccion": self.formulario.entry_dir.get().strip() or "Av. Caupolicán 1020",
            "contacto": self.formulario.entry_contacto.get().strip() or "Sin contacto registrado",
            "zona": self.formulario.opt_zona.get(),
            "vendedor": self.formulario.opt_vendedor.get(),
            "cupo_credito": cupo_num,
            "cupo": cupo_num,
            "mora": 0
        }
        self.data_store["clientes"].append(cliente_nuevo)
        messagebox.showinfo("Registro Exitoso", f"Cliente {razon} incorporado al maestro comercial.")
        self.refrescar_lista()

    def refrescar_lista(self):
        for widget in self.scroll_clientes.winfo_children():
            widget.destroy()
            
        for c in self.data_store["clientes"]:
            card = TarjetaCliente(self.scroll_clientes, c)
            card.pack(fill="x", pady=4, padx=5)

    # Métodos alias para compatibilidad interna
    _guardar_cliente = guardar_cliente
    _refrescar_lista = refrescar_lista
