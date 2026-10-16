"""
Sistema de Gestión Comercial, Inventario y Distribución (DistriGest)
Firma Desarrolladora: Bomcode
Caso de Estudio: DistriSur Araucanía SpA - Inacap Sede Temuco
Evaluación N° 3: Prototipo Funcional en Python (Arquitectura Modular)
Requerimientos Cubiertos: RF-01, RF-08, RF-10, RF-11, RF-17, RF-20, RF-23, RF-25
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import theme as th
from views.clientes_view import (
    ClientesView,
    FormularioFichaCliente,
    TarjetaCliente,
    validar_rut_chileno
)


# ==============================================================================
# 2. MÓDULO C: INVENTARIO Y BODEGA (RF-08, RF-10, RF-11)
# ==============================================================================
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
        lbl = ctk.CTkLabel(frame, text="Recepción de Mercaderías contra Orden de Compra", font=ctk.CTkFont(family=th.FONT_FAMILY, size=th.FONT_SIZE_SUBTITLE, weight="bold"))
        lbl.pack(anchor="w", padx=15, pady=(10, 5))
        
        f_top = ctk.CTkFrame(frame, fg_color="transparent")
        f_top.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(f_top, text="Orden de Compra:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=5)
        self.cb_oc = ctk.CTkComboBox(f_top, values=["OC-2026-8901 (Distribuidora del Sur)", "OC-2026-8902 (Molinos Temuco)", "OC-2026-8903 (Lácteos Araucanía)"])
        self.cb_oc.grid(row=0, column=1, padx=10, sticky="w")
        
        ctk.CTkLabel(f_top, text="Bodega Destino:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, sticky="w", padx=5)
        self.cb_bodega_rec = ctk.CTkComboBox(f_top, values=["Temuco - Centro Principal (4.500 m²)", "Angol - Bodega Regional (800 m²)"])
        self.cb_bodega_rec.grid(row=0, column=3, padx=10, sticky="w")

        f_item = ctk.CTkFrame(frame, fg_color=th.COLOR_CARD_BG, corner_radius=8)
        f_item.pack(fill="x", padx=15, pady=10)
        
        self.in_sku = self._mini_campo(f_item, "Producto / SKU:", 0, "AR-001 - Aceite Vegetal 1L")
        self.in_cant_oc = self._mini_campo(f_item, "Cant. Comprada:", 1, "500")
        self.in_cant_rec = self._mini_campo(f_item, "Cant. Recibida:", 2, "480")
        self.in_lote = self._mini_campo(f_item, "Código Lote:", 3, "L-2026-OCT-09")
        self.in_venc = self._mini_campo(f_item, "Fecha Vencimiento:", 4, "2027-04-15")
        
        btn_ingreso = ctk.CTkButton(frame, text="Confirmar Recepción y Calcular Diferencias", fg_color=th.COLOR_PRIMARY, hover_color=th.COLOR_SECONDARY, command=self._procesar_recepcion)
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
        lbl = ctk.CTkLabel(frame, text="Control de Stock por Producto, Lote y Ubicación Física", font=ctk.CTkFont(family=th.FONT_FAMILY, size=th.FONT_SIZE_SUBTITLE, weight="bold"))
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
        lbl = ctk.CTkLabel(frame, text="Tablero de Alertas Críticas de Inventario (Regla FEFO)", font=ctk.CTkFont(family=th.FONT_FAMILY, size=th.FONT_SIZE_SUBTITLE, weight="bold"))
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


# ==============================================================================
# 3. MÓDULO E: FACTURACIÓN Y COBRANZA (RF-17)
# ==============================================================================
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
        self.cb_pedidos = ctk.CTkComboBox(f_top, values=["PED-00109 - Supermercado La Araucana ($1.450.000)", "PED-00110 - Minimarket Central ($380.000)"], width=320)
        self.cb_pedidos.grid(row=0, column=3, padx=10, sticky="w")
        
        detalle_box = ctk.CTkFrame(panel, fg_color=th.COLOR_BACKGROUND, corner_radius=8)
        detalle_box.pack(fill="x", padx=25, pady=15)
        
        ctk.CTkLabel(detalle_box, text="Detalle de Líneas de Facturación Tributaria", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
        ctk.CTkLabel(detalle_box, text="1. 100x Aceite Vegetal 1L  |  P.Unit: $1.800  |  Subtotal: $180.000\n2. 50x Harina Selecta 1kg  |  P.Unit: $950    |  Subtotal: $47.500", justify="left").pack(anchor="w", padx=15, pady=(0, 10))
        
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
        
        # Validación de RNF: Diálogo modal con acción explícita
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


# ==============================================================================
# 4. MÓDULO F: COMPRAS Y PROVEEDORES (RF-20)
# ==============================================================================
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
        
        btn_reg = ctk.CTkButton(f_izq, text="Registrar Proveedor", fg_color=th.COLOR_PRIMARY, hover_color=th.COLOR_SECONDARY, command=self._registrar_proveedor)
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


# ==============================================================================
# 5. MÓDULO G: REPORTES E INDICADORES (RF-23, RF-25)
# ==============================================================================
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
        lbl = ctk.CTkLabel(f, text="Panel Analítico de Ventas por Dimensiones Geográficas", font=ctk.CTkFont(family=th.FONT_FAMILY, size=th.FONT_SIZE_SUBTITLE, weight="bold"))
        lbl.pack(anchor="w", padx=15, pady=(10, 10))
        
        f_filtros = ctk.CTkFrame(f, fg_color=th.COLOR_CARD_BG, corner_radius=8)
        f_filtros.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(f_filtros, text="Zona:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=8, pady=8)
        cb_z = ctk.CTkComboBox(f_filtros, values=["Todas las Zonas", "Temuco Centro", "Padre Las Casas", "Angol"])
        cb_z.grid(row=0, column=1, padx=5, pady=8)
        
        ctk.CTkLabel(f_filtros, text="Vendedor:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, padx=8, pady=8)
        cb_v = ctk.CTkComboBox(f_filtros, values=["Todos los Vendedores", "Juan Pérez", "María Soto", "Carlos Lagos"])
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
        lbl = ctk.CTkLabel(f, text="Cálculo Algorítmico de Comisiones Cruzadas con Cobranza Efectiva", font=ctk.CTkFont(family=th.FONT_FAMILY, size=th.FONT_SIZE_SUBTITLE, weight="bold"))
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


# ==============================================================================
# VENTANA CONTROLADORA PRINCIPAL
# ==============================================================================
class DistriGestApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("DistriGest v1.0 - Prototipo Modular (DistriSur Araucanía SpA)")
        self.geometry("1280x760")
        self.minsize(1100, 680)
        
        # Repositorio Simulado en Memoria
        self.data_store = {
            "clientes": [
                {
                    "rut": "76.432.123-K",
                    "razon_social": "Supermercado La Araucana SpA",
                    "razon": "Supermercado La Araucana SpA",
                    "giro": "Supermercado",
                    "direccion": "Av. Alemania 0850",
                    "contacto": "Juan Morales - +56 9 8765 4321",
                    "zona": "Temuco Centro",
                    "vendedor": "Juan Pérez",
                    "cupo_credito": 15000000,
                    "cupo": 15000000,
                    "mora": 0
                },
                {
                    "rut": "78.901.234-5",
                    "razon_social": "Minimarket Central Angol",
                    "razon": "Minimarket Central Angol",
                    "giro": "Comercio Minorista",
                    "direccion": "Calle Prat 432",
                    "contacto": "Claudia Venegas - +56 9 1234 5678",
                    "zona": "Angol",
                    "vendedor": "María Soto",
                    "cupo_credito": 4000000,
                    "cupo": 4000000,
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
        
        # Arquitectura de Navegación: Barra Lateral y Contenedor
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=th.COLOR_SIDEBAR_BG)
        self.sidebar.pack(side="left", fill="y")
        
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color=th.COLOR_BG_MAIN)
        self.main_container.pack(side="right", fill="both", expand=True)
        
        self.lista_botones_menu = []
        self.botones_vistas = {}
        
        self._build_sidebar()
        
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