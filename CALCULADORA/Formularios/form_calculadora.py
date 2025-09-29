import tkinter as tk
from tkinter import font
import Util.util_ventana as util_ventana
from Config import constantes as cons


class FormularioCalculadora(tk.Tk):

    def __init__(self):
        super().__init__()
        self.historial = []  # Lista para almacenar operaciones
        self.memory = 0      # Memoria de la calculadora
        self.config_window()
        self.construir_widget()


    def config_window(self):
        # Configuración inicial de la ventana
        self.title('Python GUI Calculadora')
        self.configure(bg=cons.COLOR_DE_FONDO_DARK)
        self.attributes('-alpha', 0.96)
        w, h = 600, 600  # Espacio extra para historial
        util_ventana.centrar_ventana(self, w, h)

    def construir_widget(self):
        # Etiqueta de operación actual
        self.operation_label = tk.Label(
            self,
            text="",
            font=('Arial', 16),
            fg=cons.COLOR_DE_TEXTO_DARK,
            bg=cons.COLOR_DE_FONDO_DARK,
            justify='right'
        )
        self.operation_label.grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky="e")

        # Pantalla principal
        self.entry = tk.Entry(
            self,
            width=13,
            font=('Arial', 40),
            bd=1,
            fg=cons.COLOR_DE_TEXTO_DARK,
            bg=cons.COLOR_CAJA_TEXTO_DARK,
            justify='right'
        )
        self.entry.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        # ---- HISTORIAL ----
        historial_label = tk.Label(
            self,
            text="Historial",
            font=('Arial', 14, 'bold'),
            fg=cons.COLOR_DE_TEXTO_DARK,
            bg=cons.COLOR_DE_FONDO_DARK
        )
        historial_label.grid(row=0, column=4, padx=10, pady=5)

        self.historial_listbox = tk.Listbox(
            self,
            width=18,
            height=20,
            font=('Arial', 12),
            bg=cons.COLOR_CAJA_TEXTO_DARK,
            fg=cons.COLOR_DE_TEXTO_DARK
        )
        self.historial_listbox.grid(row=1, column=4, rowspan=6, padx=10, pady=10, sticky='n')

        tk.Button(
            self,
            text="Limpiar Historial",
            command=self.limpiar_historial,
            bg=cons.COLOR_BOTONES_ESPECIALES_DARK,
            fg=cons.COLOR_DE_TEXTO_DARK,
            relief=tk.FLAT,
            font=('Arial', 10, 'bold')
        ).grid(row=7, column=4, padx=10, pady=5)

        # ---- BOTONES DE MEMORIA ----
        roboto_font = font.Font(family="Roboto", size=16, weight='bold')
        memoria_botones = [
            ('MR', self.memory_recall),
            ('M+', self.memory_add),
            ('M-', self.memory_subtract),
            ('MC', self.memory_clear)
        ]

        col_mem = 0
        for text, command in memoria_botones:
            tk.Button(
                self,
                text=text,
                width=5,
                height=2,
                command=command,
                bg=cons.COLOR_BOTONES_ESPECIALES_DARK,
                fg=cons.COLOR_DE_TEXTO_DARK,
                font=roboto_font,
                relief=tk.FLAT
            ).grid(row=2, column=col_mem, pady=5)
            col_mem += 1

        # ---- BOTONES PRINCIPALES ----
        # Símbolos convencionales de calculadora:
        # ÷ para división, × para multiplicación, DEL para borrar, % para porcentaje
        buttons = [
            'C', '%', 'DEL', '÷',
            '7', '8', '9', '×',
            '4', '5', '6', '−',
            '1', '2', '3', '+',
            '0', '.', '=',
        ]

        row_val = 3  # Iniciamos en la fila debajo de los botones de memoria
        col_val = 0

        for button in buttons:
            if button in ['=', '×', '÷', '−', '+', 'C', 'DEL', '%']:
                color_fondo = cons.COLOR_BOTONES_ESPECIALES_DARK
                button_font = font.Font(size=16, weight='bold')
            else:
                color_fondo = cons.COLOR_BOTONES_DARK
                button_font = roboto_font

            if button == '=':
                tk.Button(
                    self,
                    text=button,
                    width=13,
                    height=2,
                    command=lambda b=button: self.on_button_click(b),
                    bg=color_fondo,
                    fg=cons.COLOR_DE_TEXTO_DARK,
                    relief=tk.FLAT,
                    font=button_font
                ).grid(row=row_val, column=col_val, columnspan=2, pady=5)
                col_val += 1
            else:
                tk.Button(
                    self,
                    text=button,
                    width=5,
                    height=2,
                    command=lambda b=button: self.on_button_click(b),
                    bg=color_fondo,
                    fg=cons.COLOR_DE_TEXTO_DARK,
                    relief=tk.FLAT,
                    font=button_font
                ).grid(row=row_val, column=col_val, pady=5)
                col_val += 1

            if col_val > 3:
                col_val = 0
                row_val += 1


    # ----------------- FUNCIONES DE LA CALCULADORA -----------------
    def on_button_click(self, value):
        if value == '=':
            try:
                # Convertir símbolos convencionales a operadores Python
                expression = self.entry.get()
                expression = expression.replace('×', '*').replace('÷', '/').replace('−', '-')
                result = eval(expression)
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))

                # Guardar en historial
                operation = f"{expression} = {result}"
                self.operation_label.config(text=operation)
                self.agregar_a_historial(operation)

            except Exception:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "Error")
                self.operation_label.config(text="")

        elif value == 'C':
            self.entry.delete(0, tk.END)
            self.operation_label.config(text="")

        elif value == 'DEL':  # Borrar (backspace)
            current_text = self.entry.get()
            if current_text:
                new_text = current_text[:-1]
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, new_text)
                self.operation_label.config(text=new_text + " ")
        
        elif value == '%':  # Botón de porcentaje
            self.calcular_porcentaje()
            
        else:
            current_text = self.entry.get()
            
            # Validación para evitar ceros a la izquierda en números decimales
            if value == '0' and current_text and current_text[-1] == '0':
                # Si el último carácter es 0 y estamos agregando otro 0, no permitirlo
                # a menos que sea después de un punto decimal
                if '.' not in current_text or current_text.split('.')[-1].startswith('0'):
                    return
            
            # Validación para evitar múltiples puntos decimales
            if value == '.' and '.' in current_text:
                # Buscar si ya hay un punto en el número actual
                # Dividir por operadores para verificar cada número individualmente
                operators = ['+', '−', '×', '÷']  # Usar los nuevos símboles
                last_operator_index = -1
                for op in operators:
                    if op in current_text:
                        last_op_index = current_text.rfind(op)
                        if last_op_index > last_operator_index:
                            last_operator_index = last_op_index
                
                if last_operator_index == -1:
                    # No hay operadores, verificar todo el texto
                    if '.' in current_text:
                        return
                else:
                    # Hay operadores, verificar solo el último número
                    last_number = current_text[last_operator_index + 1:]
                    if '.' in last_number:
                        return
            
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, current_text + value)

    def calcular_porcentaje(self):
        """Calcula el porcentaje del número actual o en operación"""
        try:
            current_text = self.entry.get()
            if not current_text:
                return
                
            # Convertir símbolos convencionales para el cálculo
            current_text_calc = current_text.replace('×', '*').replace('÷', '/').replace('−', '-')
            
            # Si hay una operación en curso (+, -, *, /)
            for operator in ['+', '−', '×', '÷']:
                if operator in current_text:
                    parts = current_text.split(operator)
                    if len(parts) == 2 and parts[1]:  # Asegurar que hay un segundo número
                        base = float(parts[0])
                        percentage_value = float(parts[1])
                        
                        # Calcular el porcentaje del primer número
                        percentage_amount = base * (percentage_value / 100)
                        
                        # Realizar la operación según el operador
                        if operator == '+':
                            final_result = base + percentage_amount
                        elif operator == '−':
                            final_result = base - percentage_amount
                        elif operator == '×':
                            final_result = base * percentage_amount
                        elif operator == '÷':
                            final_result = base / percentage_amount if percentage_amount != 0 else "Error"
                        
                        self.entry.delete(0, tk.END)
                        self.entry.insert(tk.END, str(final_result))
                        
                        # Guardar en historial
                        operation = f"{current_text}% = {final_result}"
                        self.operation_label.config(text=operation)
                        self.agregar_a_historial(operation)
                        return
            
            # Si no hay operador, simplemente calcular el porcentaje del número
            number = float(current_text_calc)
            result = number / 100
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(result))
            
            # Guardar en historial
            operation = f"{current_text}% = {result}"
            self.operation_label.config(text=operation)
            self.agregar_a_historial(operation)
                
        except ValueError:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Error")
            self.operation_label.config(text="Error en porcentaje")
        except ZeroDivisionError:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Error: División por cero")
            self.operation_label.config(text="Error: División por cero")

    # ----------------- FUNCIONES DEL HISTORIAL -----------------
    def agregar_a_historial(self, texto):
        self.historial.append(texto)
        self.historial_listbox.insert(tk.END, texto)

    def limpiar_historial(self):
        self.historial.clear()
        self.historial_listbox.delete(0, tk.END)

    # ----------------- FUNCIONES DE MEMORIA -----------------
    def memory_add(self):
        """Suma el valor actual de la pantalla a la memoria y la muestra."""
        try:
            value = float(self.entry.get())
            self.memory += value
            self.operation_label.config(text=f"M+ (Memoria = {self.memory})")
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(self.memory))
        except ValueError:
            self.operation_label.config(text="Error M+")

    def memory_subtract(self):
        """Resta el valor actual de la pantalla de la memoria y la muestra."""
        try:
            value = float(self.entry.get())
            self.memory -= value
            self.operation_label.config(text=f"M- (Memoria = {self.memory})")
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(self.memory))
        except ValueError:
            self.operation_label.config(text="Error M-")

    def memory_clear(self):
        """Limpia la memoria y actualiza la pantalla."""
        self.memory = 0
        self.operation_label.config(text="Memoria borrada")
        self.entry.delete(0, tk.END)

    def memory_recall(self):
        """Muestra el valor actual almacenado en memoria en la pantalla."""
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, str(self.memory))
        self.operation_label.config(text=f"MR (Memoria = {self.memory})")